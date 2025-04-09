from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import os
import random


caminho_chromedriver = "C:/Users/Usuario/Documents/chromedriver-win64/chromedriver.exe"

opcoes = Options()
opcoes.add_argument('--headless')  

servico = Service(caminho_chromedriver)
navegador = uc.Chrome()

lista_links = []

num_paginas = 1


for pagina in range(1, num_paginas + 1):
    navegador.get(f"https://www.reclameaqui.com.br/empresa/itau/lista-reclamacoes/?pagina={pagina}")
    time.sleep(1)

 
    navegador.execute_script("window.scrollBy(0, 1000)")

    
    reclamacoes = navegador.find_elements(By.CSS_SELECTOR, "div.sc-1pe7b5t-0.eJgBOc")  
    
    for reclamacao in reclamacoes:
        link_element = reclamacao.find_element(By.TAG_NAME, "a")  
        link = link_element.get_attribute("href")
        if link not in lista_links:
            lista_links.append(link)


reclamacoes = {}


for link in lista_links:
    navegador.get(link)
    time.sleep(random.uniform(2, 5))  

    detalhes = {
        'titulo': '',
        'cidade': '',
        'data_hora': '',
        'id': '',
        'status': '',
        'relato': '',
        'resposta': ''
    }

    
    elementos = {
        'titulo': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[1]/div[3]/h1',  
        'cidade': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[1]/div[3]/div[1]/section/div[1]/span',
        'data_hora': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[1]/div[3]/div[1]/section/div[2]/span',
        'id': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[1]/div[3]/div[1]/section/div[3]/span',
        'status': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/span',
        'relato': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[1]/div[3]/p',
        'resposta': '//*[@id="__next"]/div[2]/div/div/main/div/div[2]/div[1]/div[2]/div[1]/p'
    }

    for chave, xpath in elementos.items():
        try:
            detalhes[chave] = WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath))).text
        except:
            detalhes[chave] = ''  

    
    reclamacoes[link] = detalhes


navegador.quit()

caminho_diretorio = os.path.expanduser("~/Documents/Projeto_SAC")

if not os.path.exists(caminho_diretorio):
    os.makedirs(caminho_diretorio)

caminho_arquivo_txt = os.path.join(caminho_diretorio, "Reclamacoes.txt")


with open(caminho_arquivo_txt, "a", encoding="utf-8") as arquivo:
    for link, detalhes in reclamacoes.items():
        arquivo.write(f"Link: {link}\n")
        arquivo.write(f"Título: {detalhes['titulo']}\n")
        arquivo.write(f"Cidade: {detalhes['cidade']}\n")
        arquivo.write(f"Data e Hora: {detalhes['data_hora']}\n")
        arquivo.write(f"ID: {detalhes['id']}\n")
        arquivo.write(f"Status: {detalhes['status']}\n")
        arquivo.write(f"Relato: {detalhes['relato']}\n")
        arquivo.write(f"Resposta: {detalhes['resposta']}\n")
        arquivo.write("\n" + "-"*100 + "\n\n")  

print(f"Arquivo salvo com sucesso em: {caminho_arquivo_txt}")
