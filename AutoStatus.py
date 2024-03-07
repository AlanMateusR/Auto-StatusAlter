###### ------- IMPORTAÇÃO DE MÓDULOS
import pandas as pd
import xlsxwriter
import os
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import oathtool
from datetime import datetime
import pytz
import shutil
import json
import requests
import urllib.parse
import http.client
import json
import requests
import urllib.parse
from dotenv import load_dotenv, dotenv_values

####################################################### GUIA DE IMPLEMENTAÇÃO #######################################################################################
""" foi escrito durante codificação do programa """

# (1) - Primeiramente, a planilha RELATORIO_ESTATISTICA é gerada no Sitef [ADENDO- a plAnilha tem que ser gerada com as colunas na ordem certa]
# DATA - NOME DO CLIENTE - CNPJ DO CLIENTE - DESCICAO DA LOJA - CNPJ DA LOJA - TOTALTRANSACAO DIA - VALOR TOTAL TRNANSACAO DIA
#
# (2) - A geração do arquivo com cnpjs valor total != 0 ; a geração do arquivo txt com cnpjs em implantação ; e o curzamento MERGE das duas serão feitas todas no mesmo codigo, então se for apenas testar a aplicação primeiro certifique-se que exista a lista dos cnpjs CRM com os cnpjs em implantação 
# 
# (3) - Com o arquivo  RELATORIO_ESTATISTICA_SAIDA.txt e Implantaçãos.txt no mesmo diretorio, será feito o cruzamento e o arquivo cnpjs_finalizados.txt será gerado, é esperado que nessa lista estejam todos os CNPJ em implantação que estão vendendo.
#
# (4) - Com a lista de cnpjs vendendo em maos o proximo passo é concluir uma forma de encerrar o pedido de vendas
#
#
# (5) - Com todo o fluxo funcionando, a ultima coisa que sera feita será a programação de fazer a aplicação abri o sitef e gerar o RELATORIO_ESTATISTICA sozinho e seguir o fluxo por si proprio 
#
# (6) - Por fim a ultima coisa que será feita vai ser implementar em algum ambiente e fazer com que o programa efetue as buscas em determinados horarios do dia 

""" Aplicação inicia no tempo determinado - duas vezes ao dia 9:30 da manha e 19:00 da noite """
## em andamento


#############################################################################################################################################################

## Foi utilizado metodo de resgate de variaveis .ENV ##
## Os dados contidos no credentials.env.example são ficticios ##

## >>> Não tente replicar o codigo ou utiliza-lo para qualquer fim <<<

""" OBTER VARIAVEIS NECESSARIAS """
# Resgatando variaveis .ENV   
load_dotenv()

# Link para requisição portal Gluo
linkGluo = os.getenv("link_crm")

# Link de acesso ao ambiente cloud Software Express
linkSwe = os.getenv("link_swe")

# Usuario e senha de acesso ao ambiente cloud (o script tem seu proprio login e atenticador)
scriptUser = os.getenv("script_user")
scriptPass = os.getenv("script_pass")
# Codigo do gogle authenticator (script tem acesso ao SECRET para efetuar login)
oathtool = os.getenv("oath_secret")

# Link completo de request quando acompanhado de payload personalizado
UrlApi = os.getenv("api_url")

""" ___________________Inicializado aplicação___________________ """

"""INICIANDO WEBDRIVER"""

servico = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=servico)
browser.get(linkSwe)

# Entra e loga no portal
search_box_login = browser.find_element(By.NAME, "username")
search_box_login.send_keys(scriptUser)

search_box_passw = browser.find_element(By.NAME, "password")
search_box_passw.send_keys(scriptPass)
search_box_login.submit()

sleep(2)

SECRET = oathtool
var = (oathtool.generate_otp(SECRET))

var_u = var[0]
var_d = var[1]
var_t = var[2]
var_q = var[3]
var_c = var[4]
var_s = var[5]

click_primeiro_campo = browser.find_element(By.ID, "camp1")
click_primeiro_campo.send_keys(f'{var_u}')

click_segundo_campo = browser.find_element(By.ID, "camp2")
click_segundo_campo.send_keys(f'{var_d}')

click_terceiro_campo = browser.find_element(By.ID, "camp3")
click_terceiro_campo.send_keys(f'{var_t}')

click_quarto_campo = browser.find_element(By.ID, "camp4")
click_quarto_campo.send_keys(f'{var_q}')

click_quinto_campo = browser.find_element(By.ID, "camp5")
click_quinto_campo.send_keys(f'{var_c}')

click_sexto_campo = browser.find_element(By.ID, "camp6")
click_sexto_campo.send_keys(f'{var_s}')

entrar_botao = browser.find_element(By.XPATH, '//*[@id="kc-login"]').click()

sleep(3)

# clica aba MONITORAÇÃO
mouse_over = browser.find_element(By.XPATH, '//*[@id="menuMonitoracao"]').click()
sleep(2)
over_click = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/table/tbody/tr[2]/td/form[2]/div[3]/div/ul/li[7]/div/table/tbody/tr[1]/td/ul/li[3]/a').click()

sleep(5)



# clica pesquisar
# obs por padrao sitef puxa seis dias pra tras, só dar um jeito de filtrar se houver necessidade 


browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[1]/div/div[2]/table/tbody/tr/td[3]/div/fieldset/div/table/tbody/tr[1]/td/a').click()


print("Pesquisa em andamento, iniciando sleep de 65 segundos...")
sleep(65)

# clica botao de gerar gelatorio

browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[1]/a').click()

# clica "selecionar todos" para des-selecionar todos

sleep(5)

browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/thead/tr/th[1]/div/div[2]/span').click()

# clica nos check box na ordem certa

# DATA - NOME DO CLIENTE - CNPJ DO CLIENTE - DESCICAO DA LOJA - CNPJ DA LOJA - TOTALTRANSACAO DIA - VALOR TOTAL TRNANSACAO DIA

sleep(3)

#data
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/div[2]/span').click()

sleep(1)

#nome do cliente
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[2]/td[1]/div/div[2]/span').click()

sleep(1)

#cnpj do cliente
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[3]/td[1]/div/div[2]/span').click()

sleep(1)

#descricao da loja
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[4]/td[1]/div/div[2]/span').click()

sleep(1)

#cnpj da loja
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[5]/td[1]/div/div[2]/span').click()

sleep(1)

#valor total transacao
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[9]/td[1]/div/div[2]/span').click()

sleep(1)

#valor total transacao dia
browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/table/tbody/tr[10]/td[1]/div/div[2]/span').click()

sleep(2)


# clica em salvar arquivo

browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/form[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/input').click()

#####################################################  [1]  ############################################################


""" COLETA DE DADOS DO HORARIO ATUAL """
# O arquivo de exportação é gerado com a hora e dia de quando foi gerado, sendo assim será coletado os dados de horario atual para buscar o arquivo pelo prefixo no diretorio downloads.

# Defina o fuso horário de Brasília
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')

# Obtém a data e hora atual com base no fuso horário de Brasília
data_hora_atual = datetime.now(fuso_horario_brasilia)

# Extrai os componentes da data e hora
ano = data_hora_atual.year
mes = data_hora_atual.month
dia = data_hora_atual.day
hora = data_hora_atual.hour
minuto = data_hora_atual.minute
segundo = data_hora_atual.second

# Imprime os valores das variáveis
print(f"Ano: {ano}")
print(f"Mês: {mes}")
print(f"Dia: {dia}")
print(f"Hora: {hora}")
print(f"Minuto: {minuto}")
print(f"Segundo: {segundo}")

sleep(5)
browser.quit()

#####################################################  [2]  ############################################################

"""Inicializando busca pelo arquivo gerado pelo sitef no diretorio DONWLOADS"""

sleep(8)

# 1 - procurar arquivo que tenha sido gerado hoje 
# 2 - informar qual arquivo achou, para depois mover e renomear o mesmo 

diretorio = '/home/user/Downloads'

prefixo_procurado = "RELATORIO_ESTATISTICA_" + str(dia) + "_" + "0" + str(mes) + "_" + str(ano) + "_" + str(hora) + "_"
print(prefixo_procurado)

arquivo_encontrado = None  # Inicialize como None

# Lista todos os arquivos no diretório
arquivos_no_diretorio = os.listdir(diretorio)

# Verifica se algum arquivo tem um nome que começa com o prefixo procurado
for arquivo in arquivos_no_diretorio:
    if arquivo.startswith(prefixo_procurado):
        arquivo_encontrado = arquivo
        break  # Se encontrado, saia do loop

if arquivo_encontrado:
    print(f"Arquivo encontrado no diretório {diretorio}. Nome do arquivo: {arquivo_encontrado}")
else:
    print("Nenhum arquivo semelhante encontrado.")

#####################################################  [3]  ############################################################


"""MOVENDO ARQUIVO GERADO PARA DIRETORIO DO SCRIPT"""

#origem = '/home/user/Downloads/RELATORIO_ESTATISTICA_27_10_2023_16_37_37.xlsx'
caminho = '/home/user/Downloads/'
origem = caminho + arquivo_encontrado

print(f"arquivo gerado: {origem}")

destino = '/home/user/Área de Trabalho/RELATORIO_ESTATISTICA.xlsx'

# Move o arquivo
shutil.move(origem, destino)

print(f"Arquivo movido para {destino}")

""" Inicializando tratamento dos dados"""

### Buscando arquivo RELATORIO_ESTATISTICA.xlsx' (gerado no sitef) para iniciar calculo 
pasta_geral = '/home/user/Área de Trabalho/'
relatorio_estatistico = f'{pasta_geral}RELATORIO_ESTATISTICA.xlsx'
### O arquivo RELATORIO_ESTATISTICA_SAIDA.txt será gerado com todos os CNPJS com venda total diferente de 0 para garantir que gere uma lista de diversos clientes vendendo ok no sitef.
relatorio_saida = f'{pasta_geral}/RELATORIO_ESTATISTICA_SAIDA.txt'

""" Calculo das celular e colunas para resultado especificado """

###### ------- MONTAGEM DO DATASETS [OK]
### ---- INFORMAÇÕES DAS EMPRESAS [OK]
df_relatorio_estatistico = pd.read_excel(relatorio_estatistico, usecols="E:G")
### ---- EXCLUSÃO LINHAS CONDICIONAIS [OK]
df_relatorio_estatistico = df_relatorio_estatistico.drop(df_relatorio_estatistico[df_relatorio_estatistico['Valor Total Transações (Dia)'] == 0].index) #excluir esses do DF original
df_cnpj_vendendo = df_relatorio_estatistico.drop(df_relatorio_estatistico[df_relatorio_estatistico['Valor Total Transações (Dia)'] == 0].index)
df_cnpj_vendendo = df_relatorio_estatistico.drop(columns=['Total Transações (Dia)', 'Valor Total Transações (Dia)'])
df_cnpj_vendendo = df_cnpj_vendendo.rename(columns={'Cnpj da Loja': 0})

""" Arquivo de saida RELATORIO_ESTATISTICA_SAIDA.txt foi gerado """

# Inicializar coleta de CNPJS do CRM com status de IMPLANTAÇÃO (range maximo suportado: 20)

import CNPJ_IMPLANTAÇÃO 
CNPJ_IMPLANTAÇÃO.implantacao()

print("Time sleep de 10 seg...")
sleep(10)

### ---- LOAD IMPLANTAÇÕES [resultado do script anterior será o arquivo Implantaçãos.txt]
df_cnpj_implantacoes = pd.read_csv('/home/user/Área de Trabalho/Implantaçãos.txt', header=None)

"""Inicializando cruzamento"""
# -> procurando CNPJs no CRM em IMPLANTAÇÃO no arquivo RELATORIO_ESTATISTICA_SAIDA.txt

### ---- MERGE ENTRE IMPLANTAÇÃO X VENDENDO
df_cnpj_finalizados = pd.merge(df_cnpj_implantacoes, df_cnpj_vendendo, on=[0], how='left', indicator='FINALIZADOS')
df_cnpj_finalizados.drop(df_cnpj_finalizados[df_cnpj_finalizados['FINALIZADOS'] == 'left_only'].index, inplace = True) 
df_cnpj_finalizados = df_cnpj_finalizados.drop(columns=['FINALIZADOS'])
df_cnpj_finalizados = df_cnpj_finalizados.drop_duplicates()

### ---- PARA SALVAR CNPJ'S FINALIZADOS EM TXT [OK]

# -> resultado do cruzamento será a geração de um novo arquivo txt com uma lista de CNPJS
# -> espera-se que nessa lista contenha todos os clientes em implantação que ja fizeram alguma venda no sitef

df_cnpj_finalizados.to_csv(f'{pasta_geral}cnpjs_finalizados.txt', sep='\t', index=False, header=None)

"""Colocar todos os CNPJS gerados em cnpjs_finalizados.txt com status de PEDIDO FINALIZADO no CRM via API"""
""" ALERANDO STATUS DOS PEDIDOS VENDENDO PARA FINALIZADO """

# atribuindo sessao a variavel 'session'

with open("session.txt", "r", encoding="utf-8") as arquivo:
        cnpjs = arquivo.readlines()
        for i, linha in enumerate(cnpjs):
            if i == 0:
                session = linha.strip()


# alterar status do pedido via API com base no PDV_NO
# variavel para PDV_NO é 'pdvs1' (nao existe)

"""REQUISIÇÃO"""

conn = http.client.HTTPSConnection(linkGluo)


def queryCrm(conn, session, query):
    print(f"query: {query}")
    query = urllib.parse.quote(query)
    # convert query to URL format
    conn.request("GET", f"/webservice.php?sessionName={session}&operation=query&query={query}")
    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))

def makeCnpjsQuery(cnpjs):
   cnpjs = ["'" + cnpj + "'" for cnpj in cnpjs]
   return "SELECT id,cpfcnpj FROM Accounts WHERE cpfcnpj IN (" + ",".join(cnpjs) + ");"

def makeConditionArray(field, values):
    if (values == None):
        return ""
    
    # if values is an array, use IN operator and return a string
    if (type(values) == list):
        values = ["'" + value + "'" for value in values]
        return f"{field} IN (" + ",".join(values) + ")"
    
    values = str(values)
    return f"{field} = '{values}'"

def makeSalesOrderQueryByClientID(ids, andConditionsArray = None):
   ids = ["'" + id + "'" for id in ids]
   sqlres = "SELECT * FROM SalesOrder WHERE account_id IN (" + ",".join(ids) + ")"

   if (andConditionsArray != None):
       sqlres += " AND " + " AND ".join([makeConditionArray(key, andConditionsArray[key]) for key in andConditionsArray])

   sqlres += ";"

   return sqlres


def revisarStatusPedidoCRMParaFinalizado(ObjetoPedido):
    # enviar request para crm
    operation_1 = "revise"
    session_1 = f"{session}"
    element_type_1 = "SalesOrder"
    ajx_1 = "DETAILVIEW"
    sostatus_1 = "Finalizado"

    url = UrlApi

    payload = {'operation': operation_1,
                'sessionName': session_1,
                'elementType': element_type_1,
                'ajxaction': ajx_1,
                'element': json.dumps({"salesorder_no": ObjetoPedido["salesorder_no"], "sostatus": sostatus_1, "id": ObjetoPedido["id"]})
                }

    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    #print teste de resposta
    print(response.text)


def revisarStatusPedidoCRMParaFinalizadoCamposIdSalesOrderNo(id, salesorder_no):
    # enviar request para crm
    operation_1 = "revise"
    session_1 = f"{session}"
    element_type_1 = "SalesOrder"
    ajx_1 = "DETAILVIEW"
    sostatus_1 = "Finalizado"

    url = UrlApi

    payload = {'operation': operation_1,
                'sessionName': session_1,
                'elementType': element_type_1,
                'ajxaction': ajx_1,
                'element': json.dumps({"salesorder_no": salesorder_no, "sostatus": sostatus_1, "id": id})
                }

    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    #print teste de resposta
    print(response.text)


# ler lista de cnpjs e alterar o status de todos pra finalizado

# Nome do arquivo .txt que contém a lista de cnpjs
nome_arquivo = 'cnpjs_finalizados.txt'

# Inicialize uma lista para armazenar os cnpjs
cnpjs = []

# Abra o arquivo e leia os cnpjs

with open(nome_arquivo, 'r') as arquivo:
    for linha in arquivo:
        # Remova espaços em branco e quebras de linha
        dado = linha.strip()
        # Armazene o dado na lista
        cnpjs.append(dado)

# Agora a variável 'cnpjs' contém a lista de cnpjs do arquivo
print(cnpjs)


organizationsData = queryCrm(conn, session, makeCnpjsQuery(cnpjs))

print(organizationsData)

assert organizationsData["success"] == True, "Error on query organizations"

# result is an array of objects, get the field id from each object
organizationsIds = [obj["id"] for obj in organizationsData["result"]]

orders = queryCrm(conn, session, makeSalesOrderQueryByClientID(organizationsIds, {"produto_pdv": ["Sitef Nuvem", "Sitef Nuvem – Promo REDE"]}))

assert orders["success"] == True, "Error on query orders"

#pdvId = [obj["salesorder_no"] for obj in resultOrders]
#print(orders)

for obj in orders["result"]:
    print(obj["salesorder_no"])
    print(obj["id"])
    print(obj["account_id"])
    print(obj["sostatus"])
    print(obj["produto_pdv"])

    revisarStatusPedidoCRMParaFinalizadoCamposIdSalesOrderNo(obj["id"], obj["salesorder_no"])
    print("###############\n\n")



"""limpeza de dados"""

print("Inicializando limpeza do cache...")

os.remove('Implantaçãos.txt')
os.remove('RELATORIO_ESTATISTICA.xlsx')
os.remove('cnpjs_finalizados.txt')
os.remove('session.txt')


"""Encerra aplicação"""
print("Concluído.")


