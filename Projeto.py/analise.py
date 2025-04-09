from transformers import AutoTokenizer, AutoModelForSequenceClassification,pipeline
from tqdm import tqdm


def processar_reclamacoes(detalhes_reclamacoes):
    
    reclamacoes = {}
    categoria_atual = None

    with open(detalhes_reclamacoes, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            
            
            if linha.startswith("Reclamações sobre"):
                categoria_atual = linha.split("sobre o ")[1].strip(":")
                reclamacoes[categoria_atual] = []  
            
            
            elif linha.startswith("-") and categoria_atual:
                reclamacao = linha[1:].strip() 
                reclamacoes[categoria_atual].append(reclamacao)
    
    return reclamacoes


def analise_sentimento_hug(reclamacoes):
    
    
    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    
    resultados = {}
    for categoria, textos in tqdm(reclamacoes.items(), desc="Analisando Sentimentos Hug"):
        resultados[categoria] = []
        
        for texto in textos:
            
            resultado = sentiment_pipeline(texto)[0]
            
            score = resultado['score']
            
            
            if score >= 0.55:
                label = resultado['label']  
                estrelas = int(label.split()[0])  
            else:
                estrelas = "Inválido"
            
            resultados[categoria].append((texto, estrelas,score))
    
    return resultados


def analise_sentimento_tw(reclamacoes):
    
    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    resultados = {}
    for categoria, textos in tqdm(reclamacoes.items(), desc="Analisando Sentimentos"):
        resultados[categoria] = []
        for texto in textos:
            resultado = sentiment_pipeline(texto)[0]
            score = resultado['score']
            label = resultado['label']
            
            if score >= 0.55:
                if label == "neutral": 
                    estrelas = 3
                elif label == "negative":
                    estrelas = 1
                elif label == "positive":
                    estrelas = 5
            else:
                estrelas = 'Inválido'
            
            resultados[categoria].append((texto, estrelas, score))
    
    return resultados


nome_arquivo = r"C:/Users/Usuario/Documents/Faculdade/SEGUNDO TERMO/Projeto.py/reclamacoes_bancarias.txt"


reclamacoes = processar_reclamacoes(nome_arquivo)

resultados_sentimentoT = analise_sentimento_tw(reclamacoes)
resultados_sentimentoH = analise_sentimento_hug(reclamacoes)


for (categoriaT, analisesT), (categoriaH, analisesH) in zip(resultados_sentimentoT.items(), resultados_sentimentoH.items()):
    print(f"\nReclamações sobre {categoriaT}:")
    for (textoT,estrelasT,scoreT), (textoH,estrelasH,scoreH) in zip(analisesT,analisesH):
        
        if scoreT > scoreH:
            print(f" Texto: {textoT}")
            print(f" Estrelas: {estrelasT}")
        else:
            print(f" Texto: {textoH}")
            print(f" Estrelas: {estrelasH}")
    
