import matplotlib.pyplot as plt
import numpy as np


dados_variados = {
    "itau": {
        "cobrança indevida": [24973, 47110, 45195, 36229, 123892, 30500, 51200, 42000, 37000, 130000],
        "atendimento": [30500, 51200, 42000, 37000, 130000, 24973, 47110, 45195, 36229, 123892],
        "taxas": [40000, 51200, 42000, 37000, 130000, 24973, 47110, 45195, 36229, 123892],
        "serviços bancários": [30500, 47110, 45195, 36229, 123892, 24973, 51200, 42000, 37000, 130000],
        "sistema": [24973, 47110, 45195, 36229, 123892, 30500, 51200, 42000, 37000, 130000],
    },
    "bradesco": {
        "cobrança indevida": [20933, 39835, 40606, 36964, 118416, 21500, 42000, 43000, 38000, 120000],
        "atendimento": [21500, 42000, 43000, 38000, 120000, 20933, 39835, 40606, 36964, 118416],
        "taxas": [42000, 43000, 38000, 120000, 20933, 39835, 40606, 36964, 21500, 118416],
        "serviços bancários": [21500, 42000, 43000, 38000, 120000, 20933, 39835, 40606, 36964, 118416],
        "sistema": [20933, 39835, 40606, 36964, 118416, 21500, 42000, 43000, 38000, 120000],
    },
    "nubank": {
        "cobrança indevida": [57503, 112402, 91639, 49818, 234827, 59000, 115000, 92000, 50000, 240000],
        "atendimento": [59000, 115000, 92000, 50000, 240000, 57503, 112402, 91639, 49818, 234827],
        "taxas": [59000, 115000, 92000, 50000, 240000, 57503, 112402, 91639, 49818, 234827],
        "serviços bancários": [59000, 115000, 92000, 50000, 240000, 57503, 112402, 91639, 49818, 234827],
        "sistema": [57503, 112402, 91639, 49818, 234827, 59000, 115000, 92000, 50000, 240000],
    },
    "banco-do-brasil": {
        "cobrança indevida": [21577, 41371, 39356, 43594, 127357, 23000, 42000, 40000, 44000, 130000],
        "atendimento": [23000, 42000, 40000, 44000, 130000, 21577, 41371, 39356, 43594, 127357],
        "taxas": [42000, 40000, 44000, 130000, 21577, 41371, 39356, 43594, 23000, 127357],
        "serviços bancários": [23000, 42000, 40000, 44000, 130000, 21577, 41371, 39356, 43594, 127357],
        "sistema": [21577, 41371, 39356, 43594, 127357, 23000, 42000, 40000, 44000, 130000],
    },
    "santander": {
        "cobrança indevida": [37462, 61662, 51493, 76306, 199074, 38000, 62000, 52000, 77000, 200000],
        "atendimento": [38000, 62000, 52000, 77000, 200000, 37462, 61662, 51493, 76306, 199074],
        "taxas": [38000, 62000, 52000, 77000, 200000, 37462, 61662, 51493, 76306, 199074],
        "serviços bancários": [38000, 62000, 52000, 77000, 200000, 37462, 61662, 51493, 76306, 199074],
        "sistema": [37462, 61662, 51493, 76306, 199074, 38000, 62000, 52000, 77000, 200000],
    },
    "inter": {
        "cobrança indevida": [32945, 64754, 60070, 50242, 170591, 34000, 65000, 61000, 51000, 172000],
        "atendimento": [34000, 65000, 61000, 51000, 172000, 32945, 64754, 60070, 50242, 170591],
        "taxas": [34000, 65000, 61000, 51000, 172000, 32945, 64754, 60070, 50242, 170591],
        "serviços bancários": [34000, 65000, 61000, 51000, 172000, 32945, 64754, 60070, 50242, 170591],
        "sistema": [32945, 64754, 60070, 50242, 170591, 34000, 65000, 61000, 51000, 172000],
    },
    "picpay": {
        "cobrança indevida": [19515, 43120, 41211, 44540, 124419, 20000, 44000, 42000, 45000, 125000],
        "atendimento": [20000, 44000, 42000, 45000, 125000, 19515, 43120, 41211, 44540, 124419],
        "taxas": [20000, 44000, 42000, 45000, 125000, 19515, 43120, 41211, 44540, 124419],
        "serviços bancários": [20000, 44000, 42000, 45000, 125000, 19515, 43120, 41211, 44540, 124419],
        "sistema": [19515, 43120, 41211, 44540, 124419, 20000, 44000, 42000, 45000, 125000],
    },
    "c6-bank": {
        "cobrança indevida": [40396, 74112, 72204, 78196, 229768, 41000, 75000, 73000, 79000, 230000],
        "atendimento": [41000, 75000, 73000, 79000, 230000, 40396, 74112, 72204, 78196, 229768],
        "taxas": [41000, 75000, 73000, 79000, 230000, 40396, 74112, 72204, 78196, 229768],
        "serviços bancários": [41000, 75000, 73000, 79000, 230000, 40396, 74112, 72204, 78196, 229768],
        "sistema": [40396, 74112, 72204, 78196, 229768, 41000, 75000, 73000, 79000, 230000],
    },
}


def grafico_reclamacoes(banco, tipo_reclamacao):
    banco = banco.lower()
    tipo_reclamacao = tipo_reclamacao.lower()

    
    if banco not in dados_variados or tipo_reclamacao not in dados_variados[banco]:
        print(f"Banco ou tipo de reclamação não encontrado. Verifique e tente novamente.")
        return

    dados_banco = dados_variados[banco][tipo_reclamacao]

    
    meses = np.arange(1, len(dados_banco) + 1)

    
    plt.figure(figsize=(10, 6))
    plt.plot(meses, dados_banco, marker='o', color='#FFABAB', linestyle='-', linewidth=2, markersize=6)
    plt.title(f'Reclamações - {banco.title()} ({tipo_reclamacao.title()}) ao Longo do Tempo')
    plt.xlabel('Meses')
    plt.ylabel('Número de Reclamações')
    plt.xticks(meses)
    plt.grid(True)
    plt.show()


def main():
    banco_escolhido = input("Digite o nome do banco (ex: Itau, Bradesco, Nubank): ").strip().lower()
    tipo_reclamacao = input("Digite o tipo de reclamação (ex: Cobrança Indevida, Atendimento, Taxas, Serviços Bancários, Sistema): ").strip().lower()

    grafico_reclamacoes(banco_escolhido, tipo_reclamacao)


main()
