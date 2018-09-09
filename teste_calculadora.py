# Android environment
import unittest
import os
import sys
import logging
import datetime

from appium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from convert_img_to_base64 import ImgToBase64

from jira_issue_handler import JiraIssueHandler
from jira_issue_handler import Response
from jira_issue_handler import IssueLinkType

from jira_constants import JIRA_AMBIENTE, JIRA_PRODUCAO, JIRA_HOMOLOGACAO
from jira_constants import PROJECT_POC_KEY, ISSUE_BUG_NAME, ISSUE_TESTEXEC_NAME, ISSUE_TESTEXEC_KEY
from jira_constants import TEST_STATUS_IN_PROGRESS_ID, TEST_STATUS_RETESTING_ID, TEST_STATUS_DONE_ID
from jira_constants import TESTEXEC_STATUS_IN_PROGRESS, TESTEXEC_STATUS_DONE
from jira_constants import TEST_RESOLUTION_TESTED, TEST_RESOLUTION_PASSED, TEST_RESOLUTION_FAILED
from jira_constants import TESTRUN_STATUS_TODO, TESTRUN_STATUS_EXECUTING, TESTRUN_STATUS_PASS, TESTRUN_STATUS_FAIL, TESTRUN_STATUS_ABORTED
from jira_constants import CT_DIGITACAO, CT_FORMATACAO_DECIMAL
from jira_constants import CT_ADICAO, CT_SUBTRACAO, CT_MULTIPLICACAO, CT_DIVISAO, CT_DIVISAO_ZERO
from jira_constants import CT_SENO, CT_COSENO, CT_TANGENTE, CT_TANGENTE_90
from jira_constants import CT_PORCENTAGEM, CT_POTENCIACAO, CT_RAIZ_QUADRADA
from jira_constants import MAP_METODO_CASO_TESTE, CASO_TESTE_KEYS

LOGGER.setLevel(logging.INFO)

class TestCalc(unittest.TestCase):

    def getDesiredCaps(self):
        if (JIRA_AMBIENTE == JIRA_PRODUCAO):
            return self.getDesiredCapsPS()
        else:
            return self.getDesiredCapsInatel()

    def getDesiredCapsPS(self):
        desired_caps = {}
        desired_caps['udid'] = '35da55e8'
        desired_caps['platformName'] = 'android'
        desired_caps['deviceName'] = 'PSSantos'
        desired_caps['appPackage'] = 'com.sec.android.app.popupcalculator'
        desired_caps['appActivity'] = 'com.sec.android.app.popupcalculator.Calculator'
        
        return desired_caps

    def getDesiredCapsInatel(self):
        desired_caps = {}
        desired_caps['udid'] = '4df1730065835fb7'
        desired_caps['platformName'] = 'android'
        desired_caps['deviceName'] = 'Inatel(GT-I9300)'
        desired_caps['appPackage'] = 'com.sec.android.app.popupcalculator'
        desired_caps['appActivity'] = 'com.sec.android.app.popupcalculator.Calculator'

        return desired_caps

    def setUp(self):
        self.desired_caps = self.getDesiredCaps()
        self.screenshot_dir = os.getenv('SCREENSHOT_PATH', '') or os.getcwd() + "/"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.casoDeTeste = MAP_METODO_CASO_TESTE.get(self._testMethodName)
        self.testRunStatus = TESTRUN_STATUS_PASS
        #self.imprimirTodosElements()

    def habilitarCalcCientifica(self):
        self.driver.find_element_by_accessibility_id("Mais opções").click()
        self.driver.find_element_by_id("android:id/title").click()

    def imprimirTodosElements(self):
        #textElements = self.driver.find_elements_by_class_name('android.widget.TextView')
        #print(textElements)
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        [print(e.__getattribute__('id'), e.get_attribute("resourceId")) for e in elements]

    def iniciarCasoTeste(self, casoDeTeste):
        jiraIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_IN_PROGRESS_ID)
        testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_EXECUTING)

    def finalizarCasoTeste(self, casoDeTeste, testRunStatus):
        jiraIssueHandler.changeIssueTransition(casoDeTeste.key, TEST_STATUS_DONE_ID, TEST_RESOLUTION_TESTED)
        testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, testRunStatus)

    def criarBugJira(self, casoDeTeste, exception):
        response = jiraIssueHandler.createIssueWithRawData(PROJECT_POC_KEY, ISSUE_BUG_NAME, casoDeTeste.description, str(exception))
        if (response.status == Response.STATUS_OK):
            #jiraIssueHandler.createIssueLinkWithRawData(ISSUELINKTYPE_BLOCKS_BY, casoDeTeste.key, response.key)
            testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, casoDeTeste.key)
            jiraIssueHandler.addDefectToTestrun(testRunId, response.key)
            imageFileName = self.screenshot_dir + self._testMethodName + ".png"
            imageData = ImgToBase64().convertToBase64(imageFileName)
            jiraIssueHandler.addAttachmentToTestrun(testRunId, imageData, self._testMethodName + ".png")

    def clicarNumero(self, numArray):
        numIdPrefix = "com.sec.android.app.popupcalculator:id/bt_0"
        click = lambda num: self.driver.find_element_by_id(numIdPrefix + str(num)).click()
        [click(i) for i in numArray]

    def clicarOperador(self, operador):
        self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_' + str(operador)).click()

    def getResultadoVisor(self):
        visor = self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/txtCalc')
        resultadoVisor = visor.__getattribute__('text')
        
        return resultadoVisor

    def executarOperacao(self, digitos1, digitos2, operador, operadorPrimeiro=False):
        if (operadorPrimeiro):
            self.clicarOperador(operador)
        self.clicarNumero(digitos1)
        if (not operadorPrimeiro):
            self.clicarOperador(operador)
        self.clicarNumero(digitos2)
        self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_equal').click()

        return self.getResultadoVisor().replace("\n", "").replace(" ","")

    def executarDigitacao(self):
        numeros = [i for i in range(9, -1, -1)]
        self.clicarNumero(numeros)

        return self.getResultadoVisor().replace(",", "").replace(".","")

    def executarFormatacaoDecimal(self):
        numeros = [i for i in range(4, 0, -1)]
        self.clicarNumero(numeros)
        self.driver.find_element_by_id('com.sec.android.app.popupcalculator:id/bt_dot').click()
        self.clicarNumero([0,5])

        return self.getResultadoVisor()

    def executarTeste(self, cientifica, resultadoEsperado, metodoTeste, *args):
        try:
            self.iniciarCasoTeste(self.casoDeTeste)
            if (cientifica):
                self.habilitarCalcCientifica()
            resultadoVisor = metodoTeste(*args)
            self.assertEqual(resultadoVisor, resultadoEsperado, self.casoDeTeste.description)
        except AssertionError as exception:
            self.driver.save_screenshot(self.screenshot_dir + self._testMethodName + ".png")
            self.criarBugJira(self.casoDeTeste, exception)
            self.testRunStatus = TESTRUN_STATUS_FAIL
            raise
        except Exception as exception:
            self.testRunStatus = TESTRUN_STATUS_ABORTED
            raise            
        finally:
            self.finalizarCasoTeste(self.casoDeTeste, self.testRunStatus)

    def testDigitacao(self):
        self.executarTeste(False, "9876543210", self.executarDigitacao)

    #Simula um caso de erro: formatacao decimal não está em portugues
    def testFormatacaoDecimal(self):
        self.executarTeste(False, "4.321,05", self.executarFormatacaoDecimal)

    def testAdicao(self):
        self.executarTeste(False, "2+4=6", self.executarOperacao, *[[2], [4], "add"])

    def testSubtracao(self):
        self.executarTeste(False, "4" + u"\u2212" + "2=2", self.executarOperacao, *[[4], [2], "sub"])

    def testMultiplicacao(self):
        self.executarTeste(False, "4" + u"\u00D7" + "20=80", self.executarOperacao, *[[4], [2,0], "mul"])

    def testDivisao(self):
        self.executarTeste(False, "40÷2=20", self.executarOperacao, *[[4,0], [2], "div"])

    #Simula um caso de erro: mensagem da divisao por zero diferente da emitida pela calculadora
    def testDivisaoZero(self):
        self.executarTeste(False, "4÷0=Divisão por zero", self.executarOperacao, *[[4], [0], "div"])

    def testCoseno(self):
        self.executarTeste(True,"cos(90)=0", self.executarOperacao, *[[9,0], [], "cos",  True])
    
    def testSeno(self):
        self.executarTeste(True, "sin(90)=1", self.executarOperacao, *[[9,0], [], "sin", True])
    
    def testTangente(self):
        self.executarTeste(True, "tan(45)=1", self.executarOperacao, *[[4,5], [], "tan", True])

    #Simula um caso de erro: mensagem de calculo de tangente impossivel diferente da calculadora.
    def testTangente90(self):
        self.executarTeste(True, "tan(90)=Valor inexistente", self.executarOperacao, *[[9,0], [], "tan", True])

    def testPorcentagem(self):
        self.executarTeste(True, "400%" + u"\u00D7" + "20=80", self.executarOperacao, *[[4,0,0], [2,0], "persentage", False])

    def testPotenciacao(self):
        self.executarTeste(True, "2^(3)=8", self.executarOperacao, *[[2], [3], "x_y",  False])

    def testRaizQuadrada(self):
        self.executarTeste(True, u"\u221A" + "(9)=3", self.executarOperacao, *[[9], [], "root", True])

    def tearDown(self):
        self.driver.quit()

def criarTestExec(jiraIssueHandler):
    dateTime = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    testExecIssue = jiraIssueHandler.createIssueWithRawData(PROJECT_POC_KEY, ISSUE_TESTEXEC_NAME, "Rodada de Teste Calculadora - {}".format(dateTime))
    return testExecIssue.key

def inicializarTestExec(jiraIssueHandler):
    jiraIssueHandler.addTestToTestExecution(ISSUE_TESTEXEC_KEY, CASO_TESTE_KEYS)
    jiraIssueHandler.changeIssueTransition(ISSUE_TESTEXEC_KEY, TESTEXEC_STATUS_IN_PROGRESS)
    for key in CASO_TESTE_KEYS:
        jiraIssueHandler.changeIssueTransition(key, TEST_STATUS_RETESTING_ID)
        testRunId = jiraIssueHandler.getTestRunId(ISSUE_TESTEXEC_KEY, key)
        jiraIssueHandler.changeIssueTestRunStatus(testRunId, TESTRUN_STATUS_TODO)

def finalizarTextExec(jiraIssueHandler, result):
    resolution = TEST_RESOLUTION_PASSED if (len(result.failures) == 0 and len(result.errors) == 0) else TEST_RESOLUTION_FAILED
    jiraIssueHandler.changeIssueTransition(ISSUE_TESTEXEC_KEY, TESTEXEC_STATUS_DONE, resolution)

if __name__ == '__main__':
    inicioTeste = datetime.datetime.now()
    testResult = unittest.TestResult()
    jiraIssueHandler = JiraIssueHandler()
    try:
        ISSUE_TESTEXEC_KEY = "PV-183" #criarTestExec(jiraIssueHandler)
        inicializarTestExec(jiraIssueHandler)
        testResult = unittest.main(exit=False).result
    except Exception as ex:
        print(str(ex))
    finally:
        finalizarTextExec(jiraIssueHandler, testResult)
        fimTeste = datetime.datetime.now()
        duracao = fimTeste - inicioTeste
        print("Tempo do teste: {} minutos, {} segundos".format(int(duracao.seconds/60), duracao.seconds % 60))
        sys.exit(0)