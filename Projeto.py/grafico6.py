import matplotlib.pyplot as plt
import pandas as pd


dados = {
    'Banco': ['Itaú', 'Itaú', 'Itaú', 'Bradesco', 'Bradesco', 'Bradesco', 'Caixa Econômica', 'Caixa Econômica', 'Caixa Econômica'],
    'Tipo de Reclamação': ['Taxas Altas', 'Atendimento ao Cliente', 'Serviços Bancários', 'Erro em Transações', 'Sistema Offline', 'Taxas Altas', 'Serviços Bancários', 'Atendimento ao Cliente', 'Erro em Transações'],
    'Frequência': [150, 120, 80, 60, 40, 100, 70, 50, 30]
}


df = pd.DataFrame(dados)


def gerar_grafico_pareto(banco):
    
    df_banco = df[df['Banco'].str.lower() == banco.lower()]
    
    df_banco = df_banco.sort_values(by='Frequência', ascending=False)
   
    df_banco['Porcentagem Acumulada'] = df_banco['Frequência'].cumsum() / df_banco['Frequência'].sum() * 100
    
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.bar(df_banco['Tipo de Reclamação'], df_banco['Frequência'], color='skyblue')
    ax1.set_xlabel('Tipo de Reclamação')
    ax1.set_ylabel('Frequência')
    ax1.set_title(f'Gráfico de Pareto: Reclamações do {banco}')
   
    ax2 = ax1.twinx()
    ax2.plot(df_banco['Tipo de Reclamação'], df_banco['Porcentagem Acumulada'], color='red', marker='o', linestyle='-', linewidth=2)
    ax2.set_ylabel('Porcentagem Acumulada (%)')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def buscar_banco():
    banco_escolhido = input('Digite o nome do banco (Itaú, Bradesco, Caixa Econômica): ').strip()
    
    if banco_escolhido.lower() in df['Banco'].str.lower().unique():
        gerar_grafico_pareto(banco_escolhido)
    else:
        print("Banco não encontrado. Tente novamente.")


buscar_banco()
