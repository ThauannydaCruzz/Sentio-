import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3


dados = [
    ("itau", "Nome no prejuízo do banco central"),
    ("itau", "Voltando a reclamar da mesma situação"),
    ("itau", "Débito automático"),
    ("bradesco", "Problemas com conta corrente"),
    ("bradesco", "Atraso no atendimento"),
    ("nubank", "Erro no processamento do Pix"),
    ("nubank", "Redução de limite sem justificativa")
]


df = pd.DataFrame(dados, columns=["Banco", "Reclamação"])


reclamacoes_itau = len(df[df['Banco'] == 'itau'])
reclamacoes_bradesco = len(df[df['Banco'] == 'bradesco'])
reclamacoes_nubank = len(df[df['Banco'] == 'nubank'])


interseccao_itau_bradesco = 1
interseccao_itau_nubank = 1
interseccao_bradesco_nubank = 1
interseccao_todos = 1


plt.figure(figsize=(8, 8))
venn3(subsets=(
    reclamacoes_itau - interseccao_itau_bradesco - interseccao_itau_nubank + interseccao_todos,
    reclamacoes_bradesco - interseccao_itau_bradesco - interseccao_bradesco_nubank + interseccao_todos,
    interseccao_itau_bradesco,
    reclamacoes_nubank - interseccao_itau_nubank - interseccao_bradesco_nubank + interseccao_todos,
    interseccao_itau_nubank,
    interseccao_bradesco_nubank,
    interseccao_todos
), set_labels=('Itau', 'Bradesco', 'Nubank'))


plt.title("Gráfico de Venn: Reclamações dos Bancos Itau, Bradesco e Nubank")
plt.show()
