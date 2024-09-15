from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Define o caminho do ChromeDriver
caminho_chromedriver = "C:/Users/Usuario/Documents/chromedriver-win64/chromedriver.exe"

# Configurações para o ChromeDriver
opcoes = Options()
opcoes.add_argument('--headless')  # Se não precisar da interface gráfica

# Instancia o Google Chrome com o Service
servico = Service(caminho_chromedriver)
navegador = webdriver.Chrome(service=servico, options=opcoes)

#Cria uma lista que conterá os links de cada reclamação
lista_links = []

#Define o número de páginas de reclamações existentes
num_paginas = 1

#Percorre todas as páginas
for pagina in range(1,num_paginas+1):    
    #Seleciona a página desejada
    navegador.get(f"https://www.reclameaqui.com.br/empresa/itau/lista-reclamacoes/?pagina={pagina}")

    #Cria um intervalo de espera de 1 segundos
    time.sleep(1)

    #Cria uma regra que defina se a página em questão é a última ou não
    if pagina == num_paginas:
        limite = 10 + 1
    else:
        limite = 11 #Pois por padrão cada página de reclamações contém 10
    
    #Percorre cada reclamação de forma individual
    for i in range(1,limite):
        #Define o elemento html na página que direciona para a reclamação
        reclamacao = '//*[@id="__next"]/div[1]/div[1]/div[2]/main/section[2]/div[2]/div[2]/div[{}]/a'.format(i)
        
        #Cria um loop até que a página carregue completamente e os elementos possam ser coletados
        while navegador.find_element("xpath",reclamacao).get_attribute('href') in lista_links:
            #Cria um intervalo de espera de 2 segundos
            time.sleep(2)
            #Valida se a página já carregou. Se o elemento já está na 'lista_links', a página visualizada ainda é a anterior            
            reclamacao = '//*[@id="__next"]/div[1]/div[1]/div[2]/main/section[2]/div[2]/div[2]/div[{}]/a'.format(i)

        #Adiciona o novo elemento à 'lista_links'
        lista_links.append(navegador.find_element("xpath",reclamacao).get_attribute('href'))
        
#Fecha o navegador
navegador.quit()


#Cria um dicionário que registrará os detalhes de cada reclamação
reclamacoes = {}

#Instancia o Google Chrome
navegador = webdriver.Chrome(caminho_chromedriver)

#Percorre cada link coletado
for link in lista_links:
    #Cria um intervalo de espera de12 segundo
    time.sleep(1)

    #Seleciona a página desejada
    navegador.get(link)
    
    #Cria um intervalo de espera de 2 segundos
    time.sleep(2)

    #Define um dicionário individual para cada reclamação    
    reclamacoes[link] = {}
    
    #Coleta os elementos relevantes com base nos 'xpaths' respectivos, extraindo os textos de cada elemento
    #Todos os elementos abaixo constam para qualquer empresa
    reclamacoes[link]['titulo'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[1]/div[3]/h1').text
    reclamacoes[link]['cidade'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/span').text
    reclamacoes[link]['data_hora'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/span').text
    reclamacoes[link]['id'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[1]/div[3]/div[1]/div[2]/div[3]/span').text
    reclamacoes[link]['status'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/span').text
    reclamacoes[link]['relato'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[1]/div[3]/p').text
    
    #Coleta os elementos secundários com base nos 'xpaths' respectivos, extraindo os textos de cada elemento caso este exista
    try:
        reclamacoes[link]['resposta'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[2]/div[1]/p').text
    #Insere um valor vazio caso o elemento não exista
    except:
        reclamacoes[link]['resposta'] = ''
    try:
        reclamacoes[link]['consideracoes_finais'] = navegador.find_element("xpath",'//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[2]/div[2]/div[1]/p').text
    except:
        reclamacoes[link]['consideracoes_finais'] = ''
    try:
        reclamacoes[link]['problema_resolvido'] = navegador.find_element('xpath','//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div/span').text
    except:
        reclamacoes[link]['problema_resolvido'] = ''
    try:
        reclamacoes[link]['negocio_novamente'] = navegador.find_element('xpath','//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div').text
    except:
        reclamacoes[link]['negocio_novamente'] = ''
    try:
        reclamacoes[link]['nota_atendimento'] = navegador.find_element('xpath','//*[@id="__next"]/div[1]/div[1]/div[3]/main/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div/div').text
    except:
        reclamacoes[link]['nota_atendimento'] = ''
#Cria um dataframe para estruturarmos as informações coletadas
df_reclamacoes = pd.DataFrame()
#Percorre cada reclamação no dicionário principal
for reclamacao in reclamacoes:
    #Cria um dataframe temporário com base na reclamação da etapa
    df_temp = pd.DataFrame(reclamacoes[reclamacao], index = [0])
    #Insere uma coluna adicional no dataframe com o link da reclamação
    df_temp['link'] = reclamacao
    #Insere o dataframe temporário no dataframe principal
    df_reclamacoes = pd.concat([df_reclamacoes,df_temp],axis=0)
#Reorganiza as colunas do dataframe resultante
df_reclamacoes = df_reclamacoes.iloc[:,[-1,0,1,2,3,4,5,6,7,8,9,10]]
df_reclamacoes.to_csv('//mivsvdc01/BI/Base Para Atualização/SAC/detalhes_reclamacoes.csv')
