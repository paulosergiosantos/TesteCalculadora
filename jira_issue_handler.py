import sys
import requests
import json
import logging
import http
import datetime

from utils import GeneralUtils
from send_email import SendEmail
from jira_constants import JIRA_AUTH, JIRA_ACCEPT, JIRA_CONTENT
from jira_constants import JIRA_ISSUE_URL, JIRA_ISSUELINK_URL, JIRA_ISSUE_TRANSITION_URL, JIRA_ISSUE_GET_SUMMARY_URL
from jira_constants import JIRA_TESTEXEC_ADD_TEST_URL
from jira_constants import JIRA_TESTRUN_GET_ID_URL, JIRA_TESTRUN_ADD_DEFECT_URL, JIRA_TESTRUN_ADD_ATTACHMENT_URL, JIRA_TESTRUN_CHANGE_STATUS_URL
from jira_constants import JIRA_ISSUE_ADD_WATCHER_URL, JIRA_BUG_LINK_URL, EMAIL_TO_NOTIFICATION, EMAIL_CC_NOTIFICATION
from jira_constants import PROJECT_POC_KEY, ISSUE_BUG_NAME, ISSUE_TESTEXEC_NAME, ISSUE_TESTEXEC_KEY, ISSUELINKTYPE_BLOCKS_BY
from jira_constants import TEST_STATUS_IN_PROGRESS_ID, TEST_STATUS_RETESTING_ID, TEST_STATUS_DONE_ID
from jira_constants import TEST_RESOLUTION_TESTED
from jira_constants import TESTRUN_STATUS_EXECUTING, TESTRUN_STATUS_PASS, TESTRUN_STATUS_FAIL, TESTRUN_STATUS_TODO
from jira_constants import TESTEXEC_STATUS_IN_PROGRESS, TESTEXEC_STATUS_DONE
from jira_constants import COMPONENT_APP_NAME, AFFECTED_VERSION_NAME
from jira_constants import CASO_TESTE_KEYS
from jira_constants import CT_TANGENTE, CT_TANGENTE_90

class Project:
    key = None
    def __init__(self, key):
        self.key = key

class IssueType:
    name = None
    def __init__(self, name):
        self.name = name

class Assignee:
    name = None
    def __init__(self, name):
        self.name = name

class Component:
    name = None
    def __init__(self, name):
        self.name = name

class Version:
    name: None
    def __init__(self, name):
        self.name = name

class CustomField:
    value = None
    def __init__(self, value):
        self.value = value

class Fields:
    project = None
    issuetype = None
    summary = None
    description = None
    assignee = None
    def __init__(self, project, issuetype, summary, description, assignee):
        self.project = project
        self.issuetype = issuetype
        self.summary = summary
        self.description = description
        self.assignee = assignee
 
class FieldsTestExec(Fields):
    components = None
    versions: None
    def __init__(self, project, issuetype, summary, description, assignee, components, versions):
        Fields.__init__(self, project, issuetype, summary, description, assignee)
        self.components = components
        self.versions = versions

class IssueData:
    fields = None
    def __init__(self, fields):
        self.fields = fields

class WardIssue:
    key: None
    def __init__(self, key):
        self.key = key

class IssueLinkType:
    name: None
    def __init__(self, name):
        self.name = name

class IssueLink:
    type: None
    inwardIssue: None
    outwardIssue: None
    def __init__(self, type, inwardIssue, outwardIssue):
        self.type = type
        self.inwardIssue = inwardIssue
        self.outwardIssue = outwardIssue

class Transition():
    id: None
    def __init__(self, id):
        self.id = id

class IssueTransition():
    transition: None
    def __init__(self, transition):
        self.transition = transition

class Resolution():
    name: None
    def __init__(self, name):
        self.name = name

class FieldResolution():
    resolution: None
    def __init__(self, resolution):
        self.resolution = resolution

class IssueTransitionResolution():
    transition: None
    fields: None
    def __init__(self, transition, fieldResolution):
        self.transition = transition
        self.fields = fieldResolution

class TestExecAddTest():
    add: None
    def __init__(self, tests):
        self.add = tests
 
class TestRunAttachment():
    filename: None
    contentType: None
    data: None
    def __init__(self, filename, contentType, data):
        self.filename = filename
        self.contentType = contentType
        self.data = data

class Response:
    STATUS_OK = "OK"
    STATUS_ERROR = "ERROR"

    status: None
    key: None
    description: None
    def __init__(self, status, key, description=""):
        self.status = status
        self.key = key
        self.description = description

class JiraIssueInfo:
    key: None
    summary: None

    def __init__(self, key, summary):
        self.key = key
        self.summary = summary

    def __str__(self):
        return ": ".join((self.key, self.summary))

def obj_to_dict(obj):
       return obj.__dict__

def enable_log(enable=False):
    if enable:
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

class JiraIssueHandler():
    http_headers = None
    sendEmail = SendEmail()
    utils = GeneralUtils()

    def __init__(self):
        self.http_headers = {**JIRA_AUTH, **JIRA_CONTENT, **JIRA_ACCEPT}

    def createIssueFields(self, project, issuetype, summary, description, assignee, components=[], versions=[]):
        if (len(components) == 0):
            return Fields(project, issuetype, summary, description, assignee)
        else:
            return FieldsTestExec(project, issuetype, summary, description, assignee, components, versions)

    def createIssue(self, project, issuetype, summary, description, assignee, components=[], versions=[]):
        fields = self.createIssueFields(project, issuetype, summary, description, assignee, components, versions)
        issueData = IssueData(fields)
        post_url = JIRA_ISSUE_URL
        post_data = json.dumps(issueData.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        response_content = response.json()
        print("{} na criacao da issue: {}".format(self.utils.codeToStr(response.status_code, 201), response_content))
        return Response(
            Response.STATUS_OK if response.status_code == 201 else Response.STATUS_ERROR, 
            response_content['key'] if response.status_code == 201 else str(response.status_code),
            response_content)

    def createIssueWithRawData(self, projectKey, issuetypeName, summary, description, assigneeName, component="", version=""):
        project = Project(projectKey)
        issuetype = IssueType(issuetypeName)
        assignee = Assignee(assigneeName)
        components = list()
        versions = list()
        if (component):
            components.append(Component(component))
        if (version):
            versions.append(Version(version))

        return self.createIssue(project, issuetype, summary, description, assignee, components, versions)

    def createIssueLink(self, issueLinkType, inwardIssue, outwardIssue):
        issueLink = IssueLink(issueLinkType, inwardIssue, outwardIssue)
        post_url = JIRA_ISSUELINK_URL
        post_data = json.dumps(issueLink.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("{} na criacao do link {} entre {} e {}".format(self.utils.codeToStr(response.status_code, 201), issueLinkType, inwardIssue, outwardIssue))
    
    def getIssueSummary(self, issueKey):
        get_url = JIRA_ISSUE_GET_SUMMARY_URL.format(issueKey)
        response = requests.get(get_url, headers = self.http_headers)
        print("Status Code:", response.status_code)
        issueSummary = ""
        if (response.status_code == 200):
            response_content = response.json()
            issueSummary = response_content['fields']['summary']
        print("Summary da issue(%s): %s" % (issueKey, issueSummary))        
        return issueSummary

    def createIssueLinkWithRawData(self, typeName, inIssueKey, outIssueKey):
        issueLinkType = IssueLinkType(typeName)
        inwardIssue = WardIssue(inIssueKey)
        outwardIssue = WardIssue(outIssueKey)
        self.createIssueLink(issueLinkType, inwardIssue, outwardIssue)    

    def changeIssueTransition(self, issueKey, transitionId, resolutionName=""):
        transition = Transition(transitionId)
        issueTransitionData = IssueTransition(transition)

        if (resolutionName):
            resolution = Resolution(resolutionName)
            fields = FieldResolution(resolution)
            issueTransitionData = IssueTransitionResolution(transition, fields)

        post_url = JIRA_ISSUE_TRANSITION_URL.format(issueKey)
        post_data = json.dumps(issueTransitionData.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("{} na alteracao do status da issue {} para {}".format(self.utils.codeToStr(response.status_code, 204), issueKey, transitionId))

    def createIssueTestExec(self, projectKey, summaryPrefix, assigneeName):
        dateTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        summary ="{} - {}".format(summaryPrefix, dateTime)
        testExecIssue = self.createIssueWithRawData(projectKey, ISSUE_TESTEXEC_NAME, summary, summary, assigneeName, COMPONENT_APP_NAME, AFFECTED_VERSION_NAME)
        return testExecIssue.key

    def addTestToTestExec(self, testExecIssueKey, tests):
        testExecAddTest = TestExecAddTest(tests)
        post_url = JIRA_TESTEXEC_ADD_TEST_URL.format(testExecIssueKey)
        post_data = json.dumps(testExecAddTest.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("{} na adição dos Tests {} para o Test Exec {}".format(self.utils.codeToStr(response.status_code,200), str(tests), testExecIssueKey))

    def initIssueTestExec(self, issueTestExecKey, casoDeTesteKeys):
        self.addTestToTestExec(issueTestExecKey, casoDeTesteKeys)
        self.changeIssueTransition(issueTestExecKey, TESTEXEC_STATUS_IN_PROGRESS)
        for key in casoDeTesteKeys:
            self.changeIssueTransition(key, TEST_STATUS_RETESTING_ID)
            testRunId = self.getTestRunId(issueTestExecKey, key)
            self.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_TODO)

    def finishIssueTestExec(self, issueTestExecKey, resolution=""):
        self.changeIssueTransition(issueTestExecKey, TESTEXEC_STATUS_DONE, resolution)

    def initIssueTestRun(self, issueTestExecKey, issueTestKey):
        self.changeIssueTransition(issueTestKey, TEST_STATUS_IN_PROGRESS_ID)
        testRunId = self.getTestRunId(issueTestExecKey, issueTestKey)
        self.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_EXECUTING)

    def addDefectToTestRun(self, testRunIssueId, issueBugKey):
        issueBugKeyArr = [issueBugKey]
        post_url = JIRA_TESTRUN_ADD_DEFECT_URL.format(testRunIssueId)
        post_data = json.dumps(issueBugKeyArr)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("{} na adição do bug {} para o test run {}".format(self.utils.codeToStr(response.status_code, 200), issueBugKey, testRunIssueId))

    def addAttachmentToTestRun(self, testRunIssueId, data, filename, contentType="image/png"):
        testRunAttachment = TestRunAttachment(filename, contentType, data)
        post_url = JIRA_TESTRUN_ADD_ATTACHMENT_URL.format(testRunIssueId)
        post_data = json.dumps(testRunAttachment.__dict__, default = obj_to_dict)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("{} na adição da evidencia {} para o test run {}".format(self.utils.codeToStr(response.status_code, 200), filename, testRunIssueId))

    def addAttachmentToTestExecAndTest(self, issueTestExecKey, issueTestKey, data, filename, contentType="image/png"):
        testRunId = self.getTestRunId(issueTestExecKey, issueTestKey)
        self.addAttachmentToTestRun(testRunId, data, filename, contentType)

    def getTestRunId(self, testExecIssueKey, testIssueKey):
        get_url = JIRA_TESTRUN_GET_ID_URL.format(testExecIssueKey, testIssueKey)
        response = requests.get(get_url, headers = self.http_headers)
        print("Status Code:", response.status_code)
        testRunId = 0
        if (response.status_code == 200):
            response_content = response.json()
            testRunId = response_content['id']
        print("Id da TestExecutionKey(%s) e TestIssueKey(%s): %s" % (testExecIssueKey, testIssueKey, str(testRunId)))        
        return testRunId

    def changeIssueTestRunStatus(self, testRunIssueId, status):
        put_url = JIRA_TESTRUN_CHANGE_STATUS_URL.format(testRunIssueId, status)
        put_data = {}
        response = requests.put(put_url, headers = self.http_headers, data = put_data)
        print("Status Code:", response.status_code)
        print("{} na alteracao do status do Test Run {} para {}".format(self.utils.codeToStr(response.status_code, 200), testRunIssueId, status))  

    def addIssueWatcher(self, isseueBugKey, watcher):
        post_url = JIRA_ISSUE_ADD_WATCHER_URL.format(isseueBugKey)
        post_data = json.dumps(watcher)
        print(post_data)
        response = requests.post(post_url, headers = self.http_headers, data = post_data)
        print("Status Code:", response.status_code)
        print("{} na adição do usuario {} como wathcer para o bug {}".format(self.utils.codeToStr(response.status_code, 200), watcher, isseueBugKey))        

    def createBugAndAddToTestRun(self, projectKey, issueTestExecKey, issueTestKey, bugSummary, bugDescription, bugAssignee):
        response = self.createIssueWithRawData(projectKey, ISSUE_BUG_NAME, bugSummary, bugDescription, bugAssignee)
        if (response.status == Response.STATUS_OK):
            #jiraIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_BLOCKS_BY, issueTestKey, response.key)
            #self.addIssueWatcher(response.key, bugAssignee)
            testRunId = self.getTestRunId(issueTestExecKey, issueTestKey)
            self.addDefectToTestRun(testRunId, response.key)
            
        return response

    def finishIssueTestRun(self, issueTestExecKey, issueTestKey, testRunStatus, testResolution=""):
        self.changeIssueTransition(issueTestKey, TEST_STATUS_DONE_ID, testResolution)
        testRunId = self.getTestRunId(issueTestExecKey, issueTestKey)
        self.changeIssueTestRunStatus(testRunId, testRunStatus)

    #Simula envio de email de notificação do bug pelo Jira
    #TODO: configurar JIRA para enviar assim que o Bug for criado
    def sendBugEmailNotification(self, testExecIssueKey, testIssueKey, bugIssueKey):
        testExecInfo = JiraIssueInfo(testExecIssueKey, self.getIssueSummary(ISSUE_TESTEXEC_KEY))
        testIssueInfo = JiraIssueInfo(testIssueKey, self.getIssueSummary(testIssueKey))
        bugIssueInfo = JiraIssueInfo(bugIssueKey, self.getIssueSummary(bugIssueKey))
        subject = self.utils.getEmailSubject(testExecInfo, testIssueInfo, bugIssueInfo)
        messageText = self.utils.getTextlEmailMessage(testExecInfo, testIssueInfo, bugIssueInfo)
        messageHtml = self.utils.getHtmlEmailMessage(testExecInfo, testIssueInfo, bugIssueInfo)
        self.sendEmail.send(EMAIL_TO_NOTIFICATION, EMAIL_CC_NOTIFICATION, subject, messageText, messageHtml)

# Description para teste    
def getBugDescription():
    description = (
        "tan(90)=Limiteexcedido' != 'tan(90)=Valor inexistente'\n"
        "- tan(90)=Limiteexcedido\n"
        "+ tan(90)=Valor inexistente\n"
        ": Resultado do teste de Tangente de 90º"
    )
    return description

if __name__ == '__main__':
    #enable_log()
    dateTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    jiraIssueHandler = JiraIssueHandler()
    testExecIssue = Response(Response.STATUS_OK, "PV-183") #jiraIssueHandler.createIssueWithRawData(PROJECT_POC_KEY, ISSUE_TESTEXEC_NAME, "Rodada de Teste Calculadora - {}".format(dateTime))
    jiraIssueHandler.addTestToTestExec(testExecIssue.key, CASO_TESTE_KEYS)
    
    for key in CASO_TESTE_KEYS:
        jiraIssueHandler.changeIssueTransition(key, TEST_STATUS_RETESTING_ID)
        testRunId = jiraIssueHandler.getTestRunId(testExecIssue.key, key)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_EXECUTING)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_PASS)
        jiraIssueHandler.changeIssueTransition(key, TEST_STATUS_DONE_ID, TEST_RESOLUTION_TESTED)

    testRunId = jiraIssueHandler.getTestRunId(testExecIssue.key, CT_TANGENTE_90.key)
    jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_FAIL)
    testRunId = jiraIssueHandler.getTestRunId(testExecIssue.key, CT_TANGENTE.key)
    jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_FAIL)

    bugIssue = jiraIssueHandler.createIssue(Project(PROJECT_POC_KEY), IssueType(ISSUE_BUG_NAME), CT_TANGENTE_90.bugDescription, getBugDescription(), CT_TANGENTE_90.bugAssignee)
    jiraIssueHandler.addDefectToTestRun(testRunId, bugIssue.key)
    jiraIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_BLOCKS_BY, CT_TANGENTE_90.key, bugIssue.key)
   
    sys.exit(0)
