JIRA_PRODUCAO = "PRODUCAO"
JIRA_HOMOLOGACAO = "HOMOLOGACAO"
JIRA_AMBIENTE = JIRA_PRODUCAO

USER_PAULO = "paulosergio"
USER_ANDERSON = "andersonarruda"
USER_TADEU = "tadeuribeiro"
EMAIL_PAULO = USER_PAULO + "@inatel.br"
EMAIL_ANDERSON = USER_ANDERSON + "@inatel.br"
EMAIL_TADEU = USER_TADEU + "@inatel.br"
EMAIL_TO_NOTIFICATION=EMAIL_PAULO
EMAIL_CC_NOTIFICATION=",".join((USER_ANDERSON, EMAIL_TADEU))

class CasoTesteJira():
    key: None
    bugDescription: None
    bugAssignee: None
    def __init__(self, key, bugDescription, bugAssignee=USER_PAULO):
        self.key = key
        self.bugDescription = bugDescription
        self.bugAssignee = bugAssignee

#CONSTANTES PARA AMBIENTE DE HOMOLOGACAO
CT_DIGITACAO = CasoTesteJira("POC-550", "Resultado do teste de Digitacao")
CT_FORMATACAO_DECIMAL = CasoTesteJira("POC-510", "Resultado do teste Formatacao Decimal")
CT_ADICAO = CasoTesteJira("POC-549", "Resultado do teste de Adicao")
CT_SUBTRACAO = CasoTesteJira("POC-545", "Resultado do teste de Subtracao")
CT_MULTIPLICACAO = CasoTesteJira("POC-565", "Resultado do teste de Multiplicacao")
CT_DIVISAO = CasoTesteJira("POC-551", "Resultado do teste de Divisao")
CT_DIVISAO_ZERO = CasoTesteJira("POC-563", "Resultado do teste de Divisao por Zero", USER_ANDERSON)
CT_COSENO = CasoTesteJira("POC-566", "Resultado do teste de Coseno")
CT_SENO = CasoTesteJira("POC-567", "Resultado do teste de Seno")
CT_TANGENTE = CasoTesteJira("POC-568", "Resultado do teste de Tangente")
CT_TANGENTE_90 = CasoTesteJira("POC-571", "Resultado do teste de Tangente de 90", USER_TADEU)
CT_PORCENTAGEM = CasoTesteJira("POC-552", "Resultado do teste de Porcentagem")
CT_POTENCIACAO = CasoTesteJira("POC-569", "Resultado do teste de Potenciacao")
CT_RAIZ_QUADRADA = CasoTesteJira("POC-570", "Resultado do teste de Raiz Quadrada")
PROJECT_POC_KEY = "POC"
ISSUE_TESTEXEC_NAME = "Ciclo de Testes"
ISSUE_TESTEXEC_KEY = "POC-645"
TEST_STATUS_IN_PROGRESS_ID = "31"
TEST_STATUS_RETESTING_ID = TEST_STATUS_IN_PROGRESS_ID
TESTEXEC_STATUS_IN_PROGRESS = "31"
TESTEXEC_STATUS_DONE = "41"
TEST_RESOLUTION_DONE = "Done"

COMPONENT_APP_ID = "10002"
COMPONENT_APP_NAME = "Aplicativos"
AFFECTED_VERSION_ID = "10000"
AFFECTED_VERSION_NAME = "V1R2"

TEST_RESOLUTION_TESTED = TEST_RESOLUTION_DONE
TEST_RESOLUTION_PASSED = TEST_RESOLUTION_DONE
JIRA_SERVER_URL= "http://basetestejira.inatel.br:8080"

if (JIRA_AMBIENTE == JIRA_PRODUCAO):
    #CONSTANTES PARA AMBIENTE DE PRODUCAO
    CT_DIGITACAO.key = "PV-116"
    CT_FORMATACAO_DECIMAL.key = "PV-102"
    CT_ADICAO.key = "PV-103"
    CT_SUBTRACAO.key = "PV-111"
    CT_DIVISAO.key = "PV-113"
    CT_MULTIPLICACAO.key = "PV-112"
    CT_DIVISAO_ZERO.key = "PV-117"
    CT_COSENO.key = "PV-115"
    CT_SENO.key = "PV-114"
    CT_TANGENTE.key = "PV-106"
    CT_TANGENTE_90.key = "PV-107"
    CT_PORCENTAGEM.key = "PV-118"
    CT_POTENCIACAO.key = "PV-119"
    CT_RAIZ_QUADRADA.key = "PV-120"
    PROJECT_POC_KEY = "PV"
    ISSUE_TESTEXEC_NAME = "Test Execution"
    ISSUE_TESTEXEC_KEY = "PV-138"
    TEST_STATUS_IN_PROGRESS_ID = "51"
    TEST_STATUS_RETESTING_ID = "51"
    TESTEXEC_STATUS_IN_PROGRESS = "41"
    TESTEXEC_STATUS_DONE = "31"
    TEST_RESOLUTION_TESTED = "Tested"
    TEST_RESOLUTION_PASSED = "Passed"
    COMPONENT_APP_ID = "13503"
    COMPONENT_APP_NAME = "Aplicativos"
    AFFECTED_VERSION_ID = "14035"
    AFFECTED_VERSION_NAME = "V1R0"    
    JIRA_SERVER_URL = "http://jira.inatel.br/jira"


#CONSTANTES COMUNS PARA AMBOS AMBIENTES
ISSUE_BUG_NAME = "Bug"
ISSUELINKTYPE_BLOCKS_BY = "Blocks"
ISSUELINKTYPE_CAUSED_BY = "Problem/Incident"
ISSUELINKTYPE_CREATE_BY = "Defect"

TEST_STATUS_BACKLOG_ID = "41"
TEST_STATUS_READY_TO_TEST_ID = "21"
TEST_STATUS_TESTING_ID = "31"
TEST_STATUS_DONE_ID = "41"

TESTEXEC_STATUS_BAKCLOG="11"
TESTEXEC_STATUS_OPEN = "51"

TEST_RESOLUTION_PASSED = "Passed"
TEST_RESOLUTION_FAILED = "Failed"
TEST_RESOLUTION_BLOCKED = "Blocked"

TESTRUN_STATUS_TODO="TODO"
TESTRUN_STATUS_EXECUTING="EXECUTING"
TESTRUN_STATUS_PASS="PASS"
TESTRUN_STATUS_FAIL="FAIL"
TESTRUN_STATUS_ABORTED="ABORTED"

JIRA_API_URL = "/rest/api/latest/"
XRAY_API_URL = "/rest/raven/1.0/api/"

JIRA_ISSUE_URL = JIRA_SERVER_URL + JIRA_API_URL + "issue"
JIRA_ISSUE_ADD_WATCHER_URL = JIRA_SERVER_URL + JIRA_API_URL + "issue/{}/watchers"
JIRA_ISSUE_GET_SUMMARY_URL = JIRA_SERVER_URL + JIRA_API_URL + "issue/{}?fields=summary"
JIRA_ISSUELINK_URL = JIRA_SERVER_URL + JIRA_API_URL + "issueLink"
JIRA_ISSUE_TRANSITION_URL = JIRA_SERVER_URL + JIRA_API_URL + "issue/{}/transitions"
JIRA_TESTRUN_ADD_DEFECT_URL = JIRA_SERVER_URL + XRAY_API_URL + "testrun/{}/defect"
JIRA_TESTRUN_ADD_ATTACHMENT_URL = JIRA_SERVER_URL + XRAY_API_URL + "testrun/{}/attachment"
JIRA_TESTRUN_CHANGE_STATUS_URL = JIRA_SERVER_URL + XRAY_API_URL + "testrun/{}/status?status={}"
JIRA_TESTRUN_GET_ID_URL = JIRA_SERVER_URL + XRAY_API_URL + "testrun?testExecIssueKey={}&testIssueKey={}"
JIRA_TESTEXEC_ADD_TEST_URL = JIRA_SERVER_URL + XRAY_API_URL + "testexec/{}/test"

JIRA_BUG_LINK_URL = JIRA_SERVER_URL + "/browse/{}"

JIRA_AUTH = {'Authorization': 'Basic '}
JIRA_CONTENT = {'Content-Type': 'application/json'}
JIRA_ACCEPT = {'Accept': 'application/json'}

MAP_METODO_CASO_TESTE = {
    "testDigitacao": CT_DIGITACAO,
    "testFormatacaoDecimal": CT_FORMATACAO_DECIMAL,
    "testAdicao": CT_ADICAO,
    "testSubtracao": CT_SUBTRACAO,
    "testMultiplicacao": CT_MULTIPLICACAO,
    "testDivisao": CT_DIVISAO,
    "testDivisaoZero": CT_DIVISAO_ZERO,
    "testCoseno": CT_COSENO,
    "testSeno": CT_SENO,
    "testTangente": CT_TANGENTE,
    "testTangente90": CT_TANGENTE_90,
    "testPorcentagem": CT_PORCENTAGEM,
    "testPotenciacao": CT_POTENCIACAO,
    "testRaizQuadrada": CT_RAIZ_QUADRADA,
}

CASO_TESTE_KEYS = [casoTeste.key for method, casoTeste in MAP_METODO_CASO_TESTE.items()]

if __name__ == '__main__':
    print(CASO_TESTE_KEYS)