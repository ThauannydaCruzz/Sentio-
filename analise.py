import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from transformers import pipeline
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles
import re

# Baixar o lexicon do VADER
nltk.download("vader_lexicon")

# Inicializar o tradutor e o analisador de sentimentos VADER
translator = GoogleTranslator(source='pt', target='en')
analisador = SentimentIntensityAnalyzer()

# Inicializar o pipeline para análise de sentimentos com BERT
modelo_bert = pipeline("sentiment-analysis")

# Função para detectar e ajustar ironia ou sarcasmo
def ajustar_ironia(comentario):
    # Lista de expressões que podem ser indicativas de ironia, com um foco mais em padrões usados no Brasil
    padroes_ironia = [
        r"(nossa|que legal|ótimo|maravilhoso|que bom).*(péssimo|horrível|ruim|demorado|muito ruim|não aguento)",  # Contradição em elogios
        r"(sério|não acredito|com certeza).*(isso é incrível|vou adorar|que demais|não vejo a hora)",  # Respostas sarcásticas
        r"(hahaha|kkkk|rsrs|kakak).*",  # Uso de risadas típicas
        r"^.*(justo|com certeza|é claro|obviamente|com toda certeza).*",  # Frases excessivamente afirmativas de maneira irônica
        r"(demais|incrível|maravilhoso).*|.*(péssimo|horrível|ruim)",  # Exageros contraditórios
        r"(perfeito|exatamente o que eu queria).*|.*(muito ruim|horrível|insatisfatório)",  # Exagero de expectativas com o oposto
        r"^(sempre|nunca).*(demora|erro|falha)",  # Contradições e exageros sobre problemas ou expectativas
        r"(não|nunca|jamais).*(funcionou|resolveu|deu certo)",  # Negativas de expectativas contraditórias
        r"^.*(é, claro|obviamente).*(não vou conseguir|não vai mudar)",  # Frases irônicas afirmando que algo ruim é certo
    ]
    
    for padrao in padroes_ironia:
        if re.search(padrao, comentario, re.IGNORECASE):
            return "ironia", comentario  # Se ironia for detectada, marcamos o comentário
    return "normal", comentario  # Se não for ironia, deixamos o comentário como está

# Função para traduzir o comentário para inglês e realizar a análise de sentimento
def analisar_sentimento(comentario):
    tipo_comentario, comentario_ajustado = ajustar_ironia(comentario)  # Ajustar para ironia ou normal
    
    # Traduzir o comentário para o inglês
    comentario_traduzido = translator.translate(comentario_ajustado)
    
    # Usar o VADER para análise de sentimentos em textos curtos
    if len(comentario_traduzido.split()) <= 15:  # Texto curto
        pontuacao = analisador.polarity_scores(comentario_traduzido)
        compound = pontuacao["compound"]
        
        # Ajustando a classificação para ser mais sensível
        if compound >= 0.3:  # Limite mais sensível para positivo
            sentimento = "Positivo"
            explicacao = "Comentário claramente positivo, expressando satisfação."
        elif compound <= -0.3:  # Limite mais sensível para negativo
            sentimento = "Negativo"
            explicacao = "Comentário claramente negativo, com frustração e insatisfação."
        else:
            sentimento = "Neutro"
            explicacao = "Comentário neutro, expressando uma opinião equilibrada sem forte emoção."
    else:  # Usar BERT para textos mais longos
        resultado_bert = modelo_bert(comentario_traduzido)[0]
        sentimento = resultado_bert['label']
        explicacao = f"Comentário classificado como {sentimento.lower()} com base no contexto completo do texto."
    
    if tipo_comentario == "ironia":  # Se detectamos ironia
        explicacao = "Comentário irônico ou sarcástico. A polaridade pode não refletir o sentimento real."
        
    return sentimento, comentario_traduzido, explicacao

# Função principal para interação com o usuário e armazenamento de dados
def obter_analise_comentarios():
    comentarios_banco = {}  # Dicionário para armazenar comentários por banco
    sentimentos_gerais = {"Positivo": 0, "Neutro": 0, "Negativo": 0}
    sentimentos_por_banco = {}  # Dicionário para armazenar sentimentos por banco
    tipos_reclamacao_por_banco = {}  # Para armazenar tipos de reclamações (ex: atendimento, aplicativo)

    # Listas de palavras-chave para tipos de reclamação
    tipos_de_reclamacao = {
        "atendimento": ["atendimento", "suporte", "atendimento ao cliente", "demora"],
        "aplicativo": ["aplicativo", "app", "erro de sistema", "falha"],
        "tarifas": ["tarifa", "cobrança", "preço", "taxa", "tarifação"],
        "erro": ["erro", "problema", "falha", "bug"],
        "serviço online": ["serviço online", "site", "plataforma", "internet"]
    }

    while True:
        # Coleta do comentário e banco
        banco = input("Digite o nome do banco (ou 'sair' para finalizar): ").strip()
        if banco.lower() == 'sair':
            break
        
        comentario = input(f"Digite um comentário sobre o {banco}: ").strip()
        if comentario.lower() == 'sair':
            break
        
        # Análise do sentimento
        sentimento, comentario_traduzido, explicacao = analisar_sentimento(comentario)
        
        # Armazenar o comentário no banco correto
        if banco not in comentarios_banco:
            comentarios_banco[banco] = []
        comentarios_banco[banco].append((comentario, sentimento, comentario_traduzido, explicacao))

        # Atualizar contagem de sentimentos gerais
        sentimentos_gerais[sentimento] += 1

        # Atualizar contagem de sentimentos por banco
        if banco not in sentimentos_por_banco:
            sentimentos_por_banco[banco] = {"Positivo": 0, "Neutro": 0, "Negativo": 0}
        sentimentos_por_banco[banco][sentimento] += 1

        # Detecção de tipo de reclamação com base em palavras-chave
        if banco not in tipos_reclamacao_por_banco:
            tipos_reclamacao_por_banco[banco] = {"atendimento": 0, "aplicativo": 0, "tarifas": 0, "erro": 0, "serviço online": 0}

        # Verificar quais tipos de reclamação se aplicam ao comentário
        for tipo, palavras in tipos_de_reclamacao.items():
            if any(palavra in comentario.lower() for palavra in palavras):
                tipos_reclamacao_por_banco[banco][tipo] += 1

        print(f"\nComentário analisado: {comentario}")
        print(f"Sentimento: {sentimento} | Explicação: {explicacao}")
        print(f"Comentário traduzido: {comentario_traduzido}")
        print("-" * 50)

    # Gerar gráficos após o loop
    gerar_graficos(sentimentos_gerais, sentimentos_por_banco, tipos_reclamacao_por_banco, comentarios_banco)

# Função para gerar gráficos de distribuição
def gerar_graficos(sentimentos_gerais, sentimentos_por_banco, tipos_reclamacao_por_banco, comentarios_banco):
    # Gráfico de barras: Quantidade de reclamações por banco
    plt.figure(figsize=(8, 6))
    banco_reclamacoes = {banco: len(comentarios) for banco, comentarios in comentarios_banco.items()}
    plt.bar(banco_reclamacoes.keys(), banco_reclamacoes.values(), color="lightblue")
    plt.title("Quantidade de Reclamações por Banco")
    plt.xlabel("Bancos")
    plt.ylabel("Quantidade de Reclamações")
    plt.show()

    # Gráfico de pizza: Análise de sentimentos gerais
    plt.figure(figsize=(8, 6))
    plt.pie(sentimentos_gerais.values(), labels=sentimentos_gerais.keys(), autopct='%1.1f%%', colors=["green", "gray", "red"])
    plt.title("Análise de Sentimentos Gerais")
    plt.show()

    # Gráfico de Venn: Tipos de reclamações que coincidem entre os bancos
    bancos_comparar = list(tipos_reclamacao_por_banco.keys())[:2]  # Comparando os dois primeiros bancos
    if len(bancos_comparar) > 1:
        banco_1, banco_2 = bancos_comparar
        tipos_banco_1 = set(tipos_reclamacao_por_banco[banco_1].keys())
        tipos_banco_2 = set(tipos_reclamacao_por_banco[banco_2].keys())
        venn2([tipos_banco_1, tipos_banco_2], set_labels=(banco_1, banco_2))
        plt.title("Tipos de Reclamações - Comparação entre Bancos")
        plt.show()

if __name__ == "__main__":
    obter_analise_comentarios()
