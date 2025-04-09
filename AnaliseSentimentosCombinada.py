from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm

# É necessário dar 'pip install' em transformers e sympy

# Função para processar o arquivo e organizar as reclamações
def processar_reclamacoes(nome_arquivo):
    # Cria o dicionário {'Categoria': []}
    reclamacoes = {}
    categoria_atual = None

    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:  # Abre o Arquivo com as reclamações
        for linha in arquivo:
            linha = linha.strip()
            
            # Detecta uma nova categoria de reclamação
            if linha.startswith("Reclamações sobre"):
                categoria_atual = linha.split("sobre o ")[1].strip(":")  # Separa a linha para pegar apenas o nome da empresa, ex: "sobre o" e "Itau", pega a parte de índice 1
                reclamacoes[categoria_atual] = []  # Inicializa a lista para essa categoria
            
            # Adiciona a reclamação na categoria atual, removendo o "-"
            elif linha.startswith("-") and categoria_atual:
                reclamacao = linha[1:].strip()  # Remove o '-' e espaços ao redor
                reclamacoes[categoria_atual].append(reclamacao)
    
    return reclamacoes

# Função para realizar análise de sentimento usando Hugging Face
def analise_sentimento_hug(reclamacoes):
    # Carrega o pipeline de análise de sentimento
    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    # Cria um dicionário resultados que terá como chave as categorias, e vai armazenar uma lista de tuplas, ex: { 'Categoria' : [(x,y,z),(x2,y2,z2),...] }
    resultados = {}
    for categoria, textos in tqdm(reclamacoes.items(), desc="Analisando Sentimentos Hug"):  # Percorre categorias e textos por item de reclamações, tqdm gera a barra de progresso
        # Cria a lista, que vai armazenar tuplas, no dicionário
        resultados[categoria] = []
        # Percorre os textos da categoria
        for texto in textos:
            # Faz a análise de sentimento
            resultado = sentiment_pipeline(texto)[0]
            # Guarda o score, confiabilidade do resultado
            score = resultado['score']
            
            # Define que um nível de confiabilidade aceitável era 0.55 ou 55%
            if score >= 0.55:
                label = resultado['label']  # Exemplo de label: "3 stars"
                estrelas = int(label.split()[0])  # Extrai o número antes do "stars"
            else:
                estrelas = "Inválido"  # Se não for confiável invalidamos o resultado
            
            resultados[categoria].append((texto, estrelas, score))  # Adiciona as tuplas à lista
    
    return resultados  # Retorna o dicionário

# O funcionamento já foi explicado na função acima, irei apenas comentar as diferenças
def analise_sentimento_tw(reclamacoes):
    # Carrega o modelo e tokenizer manualmente para evitar problemas
    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # Usa tokenizer lento (SentencePiece)
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
                if label == "neutral":  # Como não temos um número de 1 a 5, defini eu mesmo, essa métrica para transformar as classificações em estrelas
                    estrelas = 3
                elif label == "negative":
                    estrelas = 1
                elif label == "positive":
                    estrelas = 5
            else:
                estrelas = 'Inválido'
            
            resultados[categoria].append((texto, estrelas, score))
    
    return resultados

# Caminho do arquivo de entrada
nome_arquivo = r"C:\Users\t.oliveira.SORRISOMARILIA\OneDrive - VIACAO SORRISO DE MARILIA LTDA\Documentos\Dados\detalhes_reclamacoes.txt"  # Caminho atualizado

# Processa o arquivo e realiza a análise de sentimento
reclamacoes = processar_reclamacoes(nome_arquivo)  # Vamos obter as reclamações dos bancos já separadas por categoria
# Vamos fazer as duas análises para combiná-las e obtermos melhores resultados
resultados_sentimentoT = analise_sentimento_tw(reclamacoes)
resultados_sentimentoH = analise_sentimento_hug(reclamacoes)

# Exibe os resultados
for (categoriaT, analisesT), (categoriaH, analisesH) in zip(resultados_sentimentoT.items(), resultados_sentimentoH.items()):
    print(f"\nReclamações sobre {categoriaT}:")
    for (textoT, estrelasT, scoreT), (textoH, estrelasH, scoreH) in zip(analisesT, analisesH):
        # Poderíamos fazer alterações aqui para mudar as regras de seleção, estamos selecionando os melhores resultados, se o melhor score for abaixo de 0.55 ambas são inválidas
        if scoreT > scoreH:
            print(f" Texto: {textoT}")
            print(f" Estrelas: {estrelasT}")
        else:
            print(f" Texto: {textoH}")
            print(f" Estrelas: {estrelasH}")
