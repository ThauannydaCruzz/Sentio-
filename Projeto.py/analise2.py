from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))


def ler_reclamacoes(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        texto = file.read()
    
    reclamacoes = re.split(r"\n\n", texto)  
    return reclamacoes

reclamacoes = ler_reclamacoes('reclamacoes_bancarias.txt')
analyzer = SentimentIntensityAnalyzer()


resultados = []
scores = {'positivo': [], 'negativo': [], 'neutro': []}
textos_sentimento = {'positivo': '', 'negativo': '', 'neutro': ''}

for reclamacao in reclamacoes:
   
    texto_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', reclamacao).lower()  
    palavras = texto_limpo.split()
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stop_words]
    texto_processado = ' '.join(palavras_sem_stopwords)
    
    
    score = analyzer.polarity_scores(texto_processado)
   
    if score['compound'] >= 0.05:
        sentimento = 'positivo'
    elif score['compound'] <= -0.05:
        sentimento = 'negativo'
    else:
        sentimento = 'neutro'
    resultados.append((reclamacao, sentimento))
    
    scores[sentimento].append(score['compound'])
    textos_sentimento[sentimento] += texto_processado + ' '


contagem_sentimentos = Counter([resultado[1] for resultado in resultados])
print(contagem_sentimentos)


plt.figure(figsize=(8, 6))
sns.barplot(x=list(contagem_sentimentos.keys()), y=list(contagem_sentimentos.values()), palette="viridis")
plt.title('Contagem de Sentimentos nas Reclamações')
plt.xlabel('Sentimento')
plt.ylabel('Número de Reclamações')
plt.show()


plt.figure(figsize=(10, 6))
for sentimento, valores in scores.items():
    sns.kdeplot(valores, label=sentimento, fill=True)
plt.title('Distribuição das Pontuações de Sentimento')
plt.xlabel('Pontuação de Sentimento')
plt.ylabel('Densidade')
plt.legend(title='Sentimento')
plt.show()


plt.figure(figsize=(15, 5))
for i, sentimento in enumerate(textos_sentimento.keys(), 1):
    plt.subplot(1, 3, i)
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(textos_sentimento[sentimento])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Nuvem de Palavras - Sentimento {sentimento.capitalize()}')
plt.tight_layout()
plt.show()


df = pd.DataFrame(resultados, columns=['reclamacao', 'sentimento'])


for sentimento in ['positivo', 'negativo', 'neutro']:
    palavras_frequentes = ' '.join(df[df['sentimento'] == sentimento]['reclamacao']).lower()
    palavras_frequentes = re.findall(r'\b\w+\b', palavras_frequentes)
    palavras_sem_stopwords = [palavra for palavra in palavras_frequentes if palavra not in stop_words]
    contagem_palavras = Counter(palavras_sem_stopwords)
    print(f"\nPalavras mais frequentes nas reclamações com sentimento {sentimento}:")
    print(contagem_palavras.most_common(10))
