import plotly.graph_objects as go
import pandas as pd
import re

# Dados de reclamações por banco (os dados fornecidos anteriormente)
dados = [
    ("itau", "Esta empresa recebeu 24973 reclamações."),
    ("itau", "Esta empresa recebeu 47110 reclamações."),
    ("itau", "Esta empresa recebeu 45195 reclamações."),
    ("itau", "Esta empresa recebeu 36229 reclamações."),
    ("itau", "Esta empresa recebeu 123892 reclamações."),
    ("bradesco", "Esta empresa recebeu 20933 reclamações."),
    ("bradesco", "Esta empresa recebeu 39835 reclamações."),
    ("bradesco", "Esta empresa recebeu 40606 reclamações."),
    ("bradesco", "Esta empresa recebeu 36964 reclamações."),
    ("bradesco", "Esta empresa recebeu 118416 reclamações."),
    ("nubank", "Esta empresa recebeu 57503 reclamações."),
    ("nubank", "Esta empresa recebeu 112402 reclamações."),
    ("nubank", "Esta empresa recebeu 91639 reclamações."),
    ("nubank", "Esta empresa recebeu 49818 reclamações."),
    ("nubank", "Esta empresa recebeu 234827 reclamações."),
    ("banco-do-brasil", "Esta empresa recebeu 21577 reclamações."),
    ("banco-do-brasil", "Esta empresa recebeu 41371 reclamações."),
    ("banco-do-brasil", "Esta empresa recebeu 39356 reclamações."),
    ("banco-do-brasil", "Esta empresa recebeu 43594 reclamações."),
    ("banco-do-brasil", "Esta empresa recebeu 127357 reclamações."),
    ("santander", "Esta empresa recebeu 37462 reclamações."),
    ("santander", "Esta empresa recebeu 61662 reclamações."),
    ("santander", "Esta empresa recebeu 51493 reclamações."),
    ("santander", "Esta empresa recebeu 76306 reclamações."),
    ("santander", "Esta empresa recebeu 199074 reclamações."),
    ("inter", "Esta empresa recebeu 32945 reclamações."),
    ("inter", "Esta empresa recebeu 64754 reclamações."),
    ("inter", "Esta empresa recebeu 60070 reclamações."),
    ("inter", "Esta empresa recebeu 50242 reclamações."),
    ("inter", "Esta empresa recebeu 170591 reclamações."),
    ("picpay", "Esta empresa recebeu 19515 reclamações."),
    ("picpay", "Esta empresa recebeu 43120 reclamações."),
    ("picpay", "Esta empresa recebeu 41211 reclamações."),
    ("picpay", "Esta empresa recebeu 44540 reclamações."),
    ("picpay", "Esta empresa recebeu 124419 reclamações."),
    ("btg-mais", "Esta empresa recebeu 1250 reclamações."),
    ("btg-mais", "Esta empresa recebeu 2545 reclamações."),
    ("btg-mais", "Esta empresa recebeu 3221 reclamações."),
    ("btg-mais", "Esta empresa recebeu 3810 reclamações."),
    ("btg-mais", "Esta empresa recebeu 9592 reclamações."),
    ("c6-bank", "Esta empresa recebeu 40396 reclamações."),
    ("c6-bank", "Esta empresa recebeu 74112 reclamações."),
    ("c6-bank", "Esta empresa recebeu 72204 reclamações."),
    ("c6-bank", "Esta empresa recebeu 78196 reclamações."),
    ("c6-bank", "Esta empresa recebeu 229768 reclamações."),
    ("santander", "Esta empresa recebeu 38813 reclamações."),
    ("santander", "Esta empresa recebeu 64324 reclamações."),
    ("santander", "Esta empresa recebeu 51470 reclamações."),
    ("santander", "Esta empresa recebeu 76300 reclamações."),
    ("santander", "Esta empresa recebeu 199000 reclamações."),
]

# Criando o DataFrame
df = pd.DataFrame(dados, columns=["Banco", "Reclamações"])

# Função para extrair o número de reclamações
def extrair_reclamacoes(texto):
    match = re.search(r"(\d+)", texto)
    if match:
        return int(match.group(1))
    return 0

# Aplicando a função para extrair as reclamações
df["Reclamações"] = df["Reclamações"].apply(extrair_reclamacoes)

# Calculando o total de reclamações por banco
total_reclamacoes = df.groupby("Banco")["Reclamações"].sum().reset_index()

# Organizando os dados
bancos = total_reclamacoes["Banco"]
reclamacoes = total_reclamacoes["Reclamações"]

# Identificando o banco com mais reclamações
banco_max_reclamacoes = bancos[reclamacoes.idxmax()]
max_reclamacoes = max(reclamacoes)

# Criando o gráfico com Plotly
fig = go.Figure()

# Barras para o total de reclamações por banco
fig.add_trace(go.Bar(
    y=bancos,
    x=reclamacoes,
    name="Total de Reclamações",
    orientation='h',
    marker=dict(
        color=['#6fa3ef' if banco == banco_max_reclamacoes else '#a2c2d0' for banco in bancos],  # Azul para o destaque, azul claro para os outros
        line=dict(color='rgba(0, 0, 0, 0.1)', width=1.5)  # Bordas suaves
    ),
    text=reclamacoes,
    textposition='outside',
    hovertemplate='Reclamações: %{x}'
))

fig.update_layout(
    title="Total de Reclamações por Banco (Com Destaque para o Maior)",
    xaxis_title="Número de Reclamações",
    yaxis_title="",
    barmode='group',
    legend_title="Fonte dos Comentários",
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor='white',
    title_font=dict(size=22, color='black', family="Arial"),
    margin=dict(l=50, r=50, t=50, b=50)
)

# Destacando o banco com mais reclamações no título
fig.add_annotation(
    x=max_reclamacoes,
    y=banco_max_reclamacoes,
    text=f"Maior Reclamação: {banco_max_reclamacoes} ({max_reclamacoes} reclamações)",
    showarrow=True,
    arrowhead=2,
    ax=-50,
    ay=-40,
    font=dict(size=12, color="black"),
    bgcolor="white"
)

# Exibindo o gráfico
fig.show()


