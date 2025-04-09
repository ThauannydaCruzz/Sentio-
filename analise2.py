import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
from googletrans import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from nltk.corpus import stopwords
import string
from termcolor import colored  # Para colorir o texto no terminal

# Função para carregar os arquivos de comentários
def carregar_comentarios(arquivos):
    comentarios = []
    bancos = []
    fontes = []
    for arquivo in arquivos:
        banco = arquivo.split('/')[-1].split('.')[0]  # Nome do banco a partir do nome do arquivo
        if arquivo.endswith(".txt"):
            with open(arquivo, 'r', encoding='utf-8') as file:
                linhas = file.readlines()
                comentarios.extend(linhas)
                bancos.extend([banco] * len(linhas))
                fontes.extend(["Bluesky"] * len(linhas))  # Fonte dos dados
        elif arquivo.endswith(".xls"):
            df = pd.read_excel(arquivo)
            comentarios.extend(df.iloc[:, 0].dropna().values.tolist())  # Supondo que os comentários estão na primeira coluna
            bancos.extend([banco] * len(df))  # Assumindo que todos os comentários são do mesmo banco
            fontes.extend(["ReclameAqui"] * len(df))  # Fonte dos dados
    return pd.DataFrame({'Comentario': comentarios, 'Banco': bancos, 'Fonte': fontes})

# Função para traduzir comentários (se necessário)
def traduzir_comentarios(comentarios, lang_dest="pt"):
    translator = Translator()
    comentarios_traduzidos = []
    for comentario in comentarios:
        try:
            translated = translator.translate(comentario, dest=lang_dest)
            comentarios_traduzidos.append(translated.text)
        except Exception as e:
            comentarios_traduzidos.append(comentario)  # Caso a tradução falhe, mantém o original
    return comentarios_traduzidos

# Função para realizar análise de sentimentos com transformers
def analisar_sentimentos_transformers(comentarios):
    sentiment_pipeline = pipeline("sentiment-analysis")
    sentimentos = []
    for comentario in comentarios:
        result = sentiment_pipeline(comentario)
        sentimentos.append(result[0]['label'])
    return sentimentos

# Função para realizar análise de sentimentos com Vader, ajustando o limiar de polaridade
def analisar_sentimentos_vader(comentarios):
    sid = SentimentIntensityAnalyzer()
    sentimentos = []
    for comentario in comentarios:
        score = sid.polarity_scores(comentario)
        
        # Ajuste do limiar para considerar um sentimento positivo ou negativo
        if score['compound'] >= 0.2:  # Limite para considerar um sentimento positivo
            sentimentos.append("Positivo")
        elif score['compound'] <= -0.2:  # Limite para considerar um sentimento negativo
            sentimentos.append("Negativo")
        else:
            # Considerando um resultado mais rigoroso para "Neutro"
            if abs(score['compound']) < 0.1:  # Apenas comentários com polaridade muito próxima de zero serão neutros
                sentimentos.append("Neutro")
            else:
                # Se não for neutro, será considerado positivo ou negativo
                sentimentos.append("Indeterminado")
    return sentimentos

# Função para filtrar palavras específicas relacionadas a reclamações
def filtrar_palavras_reclamacoes(comentarios):
    palavras_relevantes = [
        'atendimento', 'fora do ar', 'erro', 'demora', 'problema', 'pior', 'péssimo', 'sistema', 'solução',
        'dúvida', 'impossível', 'insatisfação', 'não funciona', 'não resolve', 'reclamação', 'defeito', 
        'falha', 'atraso', 'insatisfeito', 'não consigo', 'péssima', 'não consigo acessar', 'problema técnico', 'suporte'
    ]
    
    palavras_filtradas = []
    for comentario in comentarios:
        comentario = comentario.lower()  # Tornar tudo minúsculo para consistência
        palavras = comentario.split()
        palavras = [p for p in palavras if p in palavras_relevantes and p not in string.punctuation]  # Filtrar palavras relevantes
        palavras_filtradas.extend(palavras)
    return palavras_filtradas

# Função para extrair os tópicos mais mencionados nos comentários
def extrair_topicos(comentarios):
    palavras_filtradas = filtrar_palavras_reclamacoes(comentarios)
    contagem = Counter(palavras_filtradas)
    topicos = contagem.most_common(15)  # Os 15 tópicos mais mencionados
    return topicos

# Função para gerar gráficos com seaborn e matplotlib
def gerar_graficos(df, sentimentos, topicos, titulo="Análise de Sentimentos"):
    # Adicionando a coluna de sentimentos no dataframe
    df['Sentimento'] = sentimentos
    
    plt.figure(figsize=(16, 12))
    
    # Gráfico de distribuição de sentimentos por fonte de dados
    plt.subplot(2, 2, 1)
    sns.countplot(x='Sentimento', hue='Fonte', data=df, palette="Set2")
    plt.title(f"Distribuição de Sentimentos por Fonte - {titulo}")
    
    # Gráfico de barras com os sentimentos por fonte
    plt.subplot(2, 2, 2)
    sentimentos_df = df['Sentimento'].value_counts().sort_values()
    sentimentos_df.plot(kind='bar', color='skyblue')
    plt.title(f"Contagem de Sentimentos - {titulo}")
    plt.ylabel('Contagem de Sentimentos')
    
    # Gráfico de top 15 tópicos mais mencionados
    plt.subplot(2, 2, 3)
    topicos_palavras, topicos_freq = zip(*topicos)
    sns.barplot(x=list(topicos_freq), y=list(topicos_palavras), palette="coolwarm")
    plt.title(f"Top 15 Tópicos Mais Mencionados - {titulo}")
    plt.xlabel('Frequência')
    
    # Gráfico de dispersão para sentimentos ao longo dos comentários
    plt.subplot(2, 2, 4)
    comprimento_comentarios = [len(comentario.split()) for comentario in df['Comentario']]
    sentimentos_numericos = [0 if sentiment == "Positivo" else 1 if sentiment == "Neutro" else 2 for sentiment in df['Sentimento']]
    plt.scatter(comprimento_comentarios, sentimentos_numericos, c=sentimentos_numericos, cmap='coolwarm', alpha=0.7)
    plt.title("Sentimentos por Comprimento do Comentário")
    plt.xlabel("Comprimento do Comentário")
    plt.ylabel("Sentimento")
    
    # Ajustes finais e exibição
    plt.tight_layout()
    plt.show()  # Garantir que os gráficos sejam exibidos

# Função para mostrar comentários com cores de sentimento no terminal
def mostrar_comentarios_com_sentimentos(comentarios, sentimentos):
    for comentario, sentimento in zip(comentarios, sentimentos):
        if sentimento == "Positivo":
            print(colored(f"✔️ {comentario.strip()}", 'green'))
        elif sentimento == "Negativo":
            print(colored(f"❌ {comentario.strip()}", 'red'))
        elif sentimento == "Indeterminado":
            print(colored(f"⚪ {comentario.strip()}", 'grey'))
        else:
            print(colored(f"⚖️ {comentario.strip()}", 'yellow'))

# Função principal para processar e analisar os dados
def obter_analise_comentarios():
    arquivos_comentarios = [
        "C:/Users/thaua/OneDrive/Documentos/Sentio/Dados/feed_banco_do_brasil.txt",
        "C:/Users/thaua/OneDrive/Documentos/Sentio/Dados/feed_itau.txt",
        "C:/Users/thaua/OneDrive/Documentos/Sentio/Dados/feed_bradesco.txt",
        "C:/Users/thaua/OneDrive/Documentos/Sentio/Dados/feed_nubank.txt",
        "C:/Users/thaua/OneDrive/Documentos/Sentio/Dados/reclamacoes_bancarias.txt"
    ]
    
    # Carregar os comentários e os bancos
    df = carregar_comentarios(arquivos_comentarios)
    
    # Traduzir os comentários, se necessário
    comentarios_traduzidos = traduzir_comentarios(df['Comentario'])
    
    # Análise de Sentimentos
    sentimentos_transformers = analisar_sentimentos_transformers(comentarios_traduzidos)
    sentimentos_vader = analisar_sentimentos_vader(comentarios_traduzidos)
    
    # Escolher o modelo de sentimento mais adequado (no caso, vamos usar Vader)
    sentimentos = sentimentos_vader
    
    # Extrair tópicos mais mencionados
    topicos = extrair_topicos(df['Comentario'])
    
    # Gerar os gráficos
    gerar_graficos(df, sentimentos, topicos)

# Chama a função para obter a análise dos comentários
obter_analise_comentarios()
