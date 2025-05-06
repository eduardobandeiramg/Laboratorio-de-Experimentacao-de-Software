# Realizando análise pare responder às RQs

import csv
import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import pointbiserialr
import seaborn as sns
import matplotlib.pyplot as plt

## Juntando os dois CSVs em um só e alterando valor do resultado para 0/1:
linhasDaPlanilha = [["Repositório", "N° da PR", "Qtd Arquivos", "Adições", "Deleções", "Tempo p/ Fechamento (h)", "Tamanho Descrição", "N° Participantes", "N° Comentários", "Aceita?"]]
with open("Lab03/planilhas/dados_pull_requests_fechadas.csv", mode="r", encoding="utf-8", newline="") as arquivo1:
    planilha = csv.reader(arquivo1)
    next(planilha)
    for linha in planilha:
        if linha[2] == "sem dados" or linha[5] == "sem dados":
            continue
        linha[2] = float(linha[2])
        linha[9] = 1 if linha[9] == "Sim" else 0
        linhasDaPlanilha.append(linha)

with open("Lab03/planilhas/dados_pull_requests_mergeadas.csv", mode="r", encoding="utf-8", newline="") as arquivo2:
    planilha = csv.reader(arquivo2)
    next(planilha)
    for linha in planilha:
        if linha[2] == "sem dados" or linha[5] == "sem dados":
            continue
        linha[2] = float(linha[2])
        linha[9] = 1 if linha[9] == "Sim" else 0
        linhasDaPlanilha.append(linha)

with open("Lab03/planilhas/dados_pull_requests_tratada.csv", mode="w", encoding="utf-8", newline="") as arquivo3:
    csv.writer(arquivo3).writerows(linhasDaPlanilha)





# RELAÇÃO TAMANHO X ACEITAÇÃO

### Gerando mapa de calor:
linhasMatrizQtdArquivosAceita = [["Qtd Arquivos", "Linhas alteradas", "Aceitabilidade"]]
for i in range(len(linhasDaPlanilha)):
    if i == 0:
        continue
    linhasMatrizQtdArquivosAceita.append([linhasDaPlanilha[i][2], linhasDaPlanilha[i][3]+linhasDaPlanilha[i][4], linhasDaPlanilha[i][9]])

with open("Lab03/planilhas/planilhas_base_corr/matriz_corr_qtdArquivos_aceita.csv", mode="w", encoding="utf-8", newline="") as arquivo5:
    csv.writer(arquivo5).writerows(linhasMatrizQtdArquivosAceita)

### Gerando matriz de correlação de Pearson:
matriz = pd.read_csv("Lab03/planilhas/planilhas_base_corr/matriz_corr_qtdArquivos_aceita.csv", encoding="utf-8")
matrizCorr = matriz.corr()
matriz.corr().to_csv("Lab03/planilhas/planilhas_corr/matriz_corr_qtdArquivos_aceita.csv")

plt.figure(figsize=(6, 4))
sns.heatmap(matrizCorr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Relação Tamanho X Aceitabilidade")
plt.show()


# RELAÇÃO TEMPO X ACEITAÇÃO:

### Gerando mapa de calor:
linhasMatrizTempo = [["Tempo p/ Fechamento (h)", "Aceitabilidade"]]
for i in range(len(linhasDaPlanilha)):
    if i == 0:
        continue
    linhasMatrizTempo.append([linhasDaPlanilha[i][5], linhasDaPlanilha[i][9]])

with open("Lab03/planilhas/planilhas_base_corr/matriz_corr_tempo_aceita.csv", mode="w", encoding="utf-8", newline="") as arquivo5:
    csv.writer(arquivo5).writerows(linhasMatrizTempo)

### Gerando matriz de correlação de Pearson:
matriz = pd.read_csv("Lab03/planilhas/planilhas_base_corr/matriz_corr_tempo_aceita.csv", encoding="utf-8")
matrizCorr = matriz.corr()
matriz.corr().to_csv("Lab03/planilhas/planilhas_corr/matriz_corr_tempo_aceita.csv")

plt.figure(figsize=(6, 4))
sns.heatmap(matrizCorr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Relação Tempo de Análise X Aceitabilidade")
plt.show()


# RELAÇÃO DESCRIÇÃO X ACEITAÇÃO:

### Gerando mapa de calor:
linhasMatrizDescricao = [["Tamanho da Descrição", "Aceitabilidade"]]
for i in range(len(linhasDaPlanilha)):
    if i == 0:
        continue
    linhasMatrizDescricao.append([linhasDaPlanilha[i][6], linhasDaPlanilha[i][9]])

with open("Lab03/planilhas/planilhas_base_corr/matriz_corr_descricao_aceita.csv", mode="w", encoding="utf-8", newline="") as arquivo5:
    csv.writer(arquivo5).writerows(linhasMatrizDescricao)

### Gerando matriz de correlação de Pearson:
matriz = pd.read_csv("Lab03/planilhas/planilhas_base_corr/matriz_corr_descricao_aceita.csv", encoding="utf-8")
matrizCorr = matriz.corr()
matriz.corr().to_csv("Lab03/planilhas/planilhas_corr/matriz_corr_descricao_aceita.csv")

plt.figure(figsize=(6, 4))
sns.heatmap(matrizCorr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Relação Tamanho da Descrição X Aceitabilidade")
plt.show()


# RELAÇÃO INTERAÇÕES X ACEITAÇÃO:

### Gerando mapa de calor:
linhasMatrizInteracoes = [["Nº Participantes", "Nº Comentários", "Aceitabilidade"]]
for i in range(len(linhasDaPlanilha)):
    if i == 0:
        continue
    linhasMatrizInteracoes.append([linhasDaPlanilha[i][7], linhasDaPlanilha[i][8], linhasDaPlanilha[i][9]])

with open("Lab03/planilhas/planilhas_base_corr/matriz_corr_interacoes_aceita.csv", mode="w", encoding="utf-8", newline="") as arquivo5:
    csv.writer(arquivo5).writerows(linhasMatrizInteracoes)

### Gerando matriz de correlação de Pearson:
matriz = pd.read_csv("Lab03/planilhas/planilhas_base_corr/matriz_corr_interacoes_aceita.csv", encoding="utf-8")
matrizCorr = matriz.corr()
matriz.corr().to_csv("Lab03/planilhas/planilhas_corr/matriz_corr_interacoes_aceita.csv")

plt.figure(figsize=(6, 4))
sns.heatmap(matrizCorr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Relação Interações X Aceitabilidade")
plt.show()