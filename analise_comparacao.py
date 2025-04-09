import re
import os
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Baixar o lexicon do VADER
nltk.download("vader_lexicon")

# Inicializar o analisador de sentimentos VADER
analisador = SentimentIntensityAnalyzer()

# Palavras-chave para identificar os tipos de reclamação
tipos_de_reclamacao = {
    "atendimento": ["atendimento", "suporte", "demora", "não resolvem"],
    "aplicativo": ["aplicativo", "app", "erro de sistema", "falha"],
    "tarifas": ["tarifa", "cobrança", "preço", "taxa", "tarifação"],
    "erro": ["erro", "problema", "bug", "falha"],
    "serviço online": ["serviço online", "site", "internet", "plataforma"]
}

def identificar_tipos_de_reclamacao(comentarios):
    """Identifica os tipos de reclamação em uma lista de comentários."""
    tipos_detectados = {tipo: 0 for tipo in tipos_de_reclamacao.keys()}
    
    for comentario in comentarios:
        for tipo, palavras in tipos_de_reclamacao.items():
            if any(palavra in comentario.lower() for palavra in palavras):
                tipos_detectados[tipo] += 1
                
    return tipos_detectados

def analisar_sentimento(comentarios):
    """Analisa o sentimento de uma lista de comentários e retorna a quantidade de positivos, negativos e neutros."""
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
    """Carrega comentários de um arquivo de texto enviado."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            conteudo = file.read()
        # Dividir os comentários usando o separador '-'
        comentarios = [comentario.strip() for comentario in conteudo.split('-') if comentario.strip()]
        return comentarios
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_arquivo}")
        return []

def extrair_bancos(comentarios):
    """Extrai os nomes dos bancos a partir dos comentários."""
    bancos_detectados = set()
    for comentario in comentarios:
        # Supondo que o nome do banco está antes de um ':'
        bancos = re.findall(r"([A-Za-zÀ-ÿ]+(?: [A-Za-zÀ-ÿ]+)*):", comentario)
        for banco in bancos:
            bancos_detectados.add(banco.strip())
    return list(bancos_detectados)

def listar_arquivos_no_diretorio(diretorio):
    """Lista todos os arquivos no diretório atual."""
    arquivos = os.listdir(diretorio)
    print("Arquivos encontrados no diretório:")
    for arquivo in arquivos:
        print(arquivo)

def gerar_grafico_sentimentos(sentimentos, plataforma, banco):
    """Gera um gráfico de pizza com a distribuição de sentimentos (Positivo, Negativo, Neutro)."""
    plt.figure(figsize=(8, 6))
    labels = sentimentos.keys()  # Use 'sentimentos' no lugar de 'sentiments'
    sizes = sentimentos.values()  # Use 'sentimentos' no lugar de 'sentiments'
    colors = ["green", "red", "gray"]
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f"Distribuição de Sentimentos no {plataforma} - {banco}")
    plt.show()

def main():
    # Listar arquivos no diretório atual para verificar o que está disponível
    diretorio_atual = os.getcwd()  # Diretório atual
    listar_arquivos_no_diretorio(diretorio_atual)
    
    # Definir os arquivos com os nomes exatos como você mandou
    arquivo_reclame_aqui = 'detalhes_reclamacoes.txt'  # Arquivo para Reclame Aqui
    arquivo_bluesky = 'reclamacoes_bancarias.txt'  # Arquivo para Bluesky
    
    # Carregar comentários de cada arquivo
    comentarios_reclame_aqui = carregar_comentarios_arquivo(arquivo_reclame_aqui)
    comentarios_bluesky = carregar_comentarios_arquivo(arquivo_bluesky)
    
    # Extrair os nomes dos bancos dos arquivos
    bancos_reclame_aqui = extrair_bancos(comentarios_reclame_aqui)
    bancos_bluesky = extrair_bancos(comentarios_bluesky)
    
    # Exibir bancos encontrados e permitir ao usuário escolher
    bancos_combinados = set(bancos_reclame_aqui).union(set(bancos_bluesky))
    print(f"Bancos encontrados: {', '.join(bancos_combinados)}")
    
    banco = input("Digite o nome do banco para analisar: ").strip()
    
    # Carregar comentários do banco escolhido
    comentarios_reclame_aqui_banco = [comentario for comentario in comentarios_reclame_aqui if banco.lower() in comentario.lower()]
    comentarios_bluesky_banco = [comentario for comentario in comentarios_bluesky if banco.lower() in comentario.lower()]
    
    # Analisar os sentimentos
    sentimentos_reclame_aqui = analisar_sentimento(comentarios_reclame_aqui_banco)
    sentimentos_bluesky = analisar_sentimento(comentarios_bluesky_banco)
    
    # Exibir resultados
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

# Executar o programa
if __name__ == "__main__":
    main()
