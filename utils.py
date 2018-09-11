from jira_constants import JIRA_BUG_LINK_URL

class GeneralUtils():

    def __init__(self):
        pass

    def codeToStr(self, responseStatusCode, sucessSatusCode):
        return "Sucesso" if responseStatusCode == sucessSatusCode else "Erro"

    def getEmailSubject(self, testExecIssueInfo, testIssueInfo, bugIssueInfo):
        return "Erro no do teste '{}' referente à execução '{}'".format(testIssueInfo.summary, testExecIssueInfo.summary)

    def getHtmlEmailMessage(self, testExecIssueInfo, testIssueInfo, bugIssueInfo):
        testExecInfo = '<p>Execução do Teste = {}</p><br>'.format(testExecIssueInfo)
        testInfo = '<p>Caso de Teste = {}</p><br>'.format(testIssueInfo)
        bugInfo = '<p>Bug = {}</p><br>'.format(bugIssueInfo)
        bugLinkUrl = JIRA_BUG_LINK_URL.format(bugIssueInfo.key)
        bugLinkInfo = '<p><a href="{}">Clique para visualizar o bug no Jira</a></p><br>'.format(bugLinkUrl)
        return '<html><head></head><body>{}{}{}{}</body></html>'.format(testExecInfo, testInfo, bugInfo, bugLinkInfo)

    def getTextlEmailMessage(self, testExecIssueInfo, testIssueInfo, bugIssueInfo):
        testExecInfo = 'Execução do Teste = {}\n\n'.format(testExecIssueInfo)
        testInfo = 'Caso de Teste = {}\n\n'.format(testIssueInfo)
        bugInfo = 'Bug = {}\n\n'.format(bugIssueInfo)
        bugLinkUrl = JIRA_BUG_LINK_URL.format(bugIssueInfo.key)
        bugLinkInfo = '{}\n'.format(bugLinkUrl)
        return '{}{}{}{}'.format(testExecInfo, testInfo, bugInfo, bugLinkInfo)