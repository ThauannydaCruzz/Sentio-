import matplotlib.pyplot as plt
import pandas as pd
import re

# Dados de reclamações por banco
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


df["Reclamações"] = df["Reclamações"].apply(extrair_reclamacoes)


total_reclamacoes = df.groupby("Banco")["Reclamações"].sum().reset_index()


bancos = total_reclamacoes["Banco"]
reclamacoes = total_reclamacoes["Reclamações"]


fig, ax = plt.subplots(figsize=(8, 8))


ax.pie(reclamacoes, labels=bancos, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax.axis('equal')  


plt.title("Distribuição de Reclamações por Banco")


plt.show()
