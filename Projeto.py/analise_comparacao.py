import re
import os
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download("vader_lexicon")


analisador = SentimentIntensityAnalyzer()


tipos_de_reclamacao = {
    "atendimento": ["atendimento", "suporte", "demora", "não resolvem"],
    "aplicativo": ["aplicativo", "app", "erro de sistema", "falha"],
    "tarifas": ["tarifa", "cobrança", "preço", "taxa", "tarifação"],
    "erro": ["erro", "problema", "bug", "falha"],
    "serviço online": ["serviço online", "site", "internet", "plataforma"]
}

def identificar_tipos_de_reclamacao(comentarios):
   
    tipos_detectados = {tipo: 0 for tipo in tipos_de_reclamacao.keys()}
    
    for comentario in comentarios:
        for tipo, palavras in tipos_de_reclamacao.items():
            if any(palavra in comentario.lower() for palavra in palavras):
                tipos_detectados[tipo] += 1
                
    return tipos_detectados

def analisar_sentimento(comentarios):
    
    sentimentos = {"Positivo": 0, "Negativo": 0, "Neutro": 0}
    
    for comentario in comentarios:
        pontuacao = analisador.polarity_scores(comentario)
        compound = pontuacao["compound"]
        
        if compound >= 0.05:
            sentimentos["Positivo"] += 1
        elif compound <= -0.05:
            sentimentos["Negativo"] += 1
        else:
            sentimentos["Neutro"] += 1
            
    return sentimentos

def carregar_comentarios_arquivo(nome_arquivo):
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            conteudo = file.read()
        
        comentarios = [comentario.strip() for comentario in conteudo.split('-') if comentario.strip()]
        return comentarios
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_arquivo}")
        return []

def extrair_bancos(comentarios):
   
    bancos_detectados = set()
    for comentario in comentarios:
        
        bancos = re.findall(r"([A-Za-zÀ-ÿ]+(?: [A-Za-zÀ-ÿ]+)*):", comentario)
        for banco in bancos:
            bancos_detectados.add(banco.strip())
    return list(bancos_detectados)

def listar_arquivos_no_diretorio(diretorio):
    
    arquivos = os.listdir(diretorio)
    print("Arquivos encontrados no diretório:")
    for arquivo in arquivos:
        print(arquivo)

def gerar_grafico_sentimentos(sentimentos, plataforma, banco):
    
    plt.figure(figsize=(8, 6))
    labels = sentimentos.keys()  
    sizes = sentimentos.values()  
    colors = ["green", "red", "gray"]
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f"Distribuição de Sentimentos no {plataforma} - {banco}")
    plt.show()

def main():
    
    diretorio_atual = os.getcwd()  
    listar_arquivos_no_diretorio(diretorio_atual)
    
    
    arquivo_reclame_aqui = 'detalhes_reclamacoes.txt'  
    arquivo_bluesky = 'reclamacoes_bancarias.txt' 
    
    
    comentarios_reclame_aqui = carregar_comentarios_arquivo(arquivo_reclame_aqui)
    comentarios_bluesky = carregar_comentarios_arquivo(arquivo_bluesky)
    
    
    bancos_reclame_aqui = extrair_bancos(comentarios_reclame_aqui)
    bancos_bluesky = extrair_bancos(comentarios_bluesky)
    
 
    bancos_combinados = set(bancos_reclame_aqui).union(set(bancos_bluesky))
    print(f"Bancos encontrados: {', '.join(bancos_combinados)}")
    
    banco = input("Digite o nome do banco para analisar: ").strip()
    
    
    comentarios_reclame_aqui_banco = [comentario for comentario in comentarios_reclame_aqui if banco.lower() in comentario.lower()]
    comentarios_bluesky_banco = [comentario for comentario in comentarios_bluesky if banco.lower() in comentario.lower()]
    
   
    sentimentos_reclame_aqui = analisar_sentimento(comentarios_reclame_aqui_banco)
    sentimentos_bluesky = analisar_sentimento(comentarios_bluesky_banco)
    
    
    if comentarios_reclame_aqui_banco:
        print(f"\nReclame Aqui - Resultados para {banco}: {sentimentos_reclame_aqui}")
        gerar_grafico_sentimentos(sentimentos_reclame_aqui, "Reclame Aqui", banco)
    else:
        print(f"Sem dados encontrados no Reclame Aqui para {banco}.")
    
    if comentarios_bluesky_banco:
        print(f"\nBluesky - Resultados para {banco}: {sentimentos_bluesky}")
        gerar_grafico_sentimentos(sentimentos_bluesky, "Bluesky", banco)
    else:
        print(f"Sem dados encontrados no Bluesky para {banco}.")


if __name__ == "__main__":
    main()
