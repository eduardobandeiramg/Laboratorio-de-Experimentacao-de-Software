import csv
import statistics
import matplotlib.pyplot as plt

qtdsArquivosPRsFechadas = []
qtdsArquivosPRsMergeadas = []
qtdsAlteracoesPRsFechadas = []
qtdsAlteracoesPRsMergeadas = []
temposPRsFechadas = []
temposPRsMergeadas = []
tamanhosDescricaPRsFechadas = []
tamanhosDescricaPRsMergeadas = []
qtdsParticipantePRsFechadas = []
qtdsParticipantePRsPRsMergeadas = []
qtdsComentariosPRsFechadas = []
qtdsComentariosPRsMergeadas = []

with open("Lab03/planilhas/dados_pull_requests_tratada.csv", mode="r", encoding="utf-8", newline="") as arquivo:
    planilha = csv.reader(arquivo)
    for linha in planilha:
        if linha[9] == "0":
            qtdsArquivosPRsFechadas.append(float(linha[2]))
            qtdsAlteracoesPRsFechadas.append(float(linha[3]) + float(linha[4]))
            temposPRsFechadas.append(float(linha[5]))
            tamanhosDescricaPRsFechadas.append(float(linha[6]))
            qtdsParticipantePRsFechadas.append(float(linha[7]))
            qtdsComentariosPRsFechadas.append(float(linha[8]))
        elif linha[9] == "1":
            qtdsArquivosPRsMergeadas.append(float(linha[2]))
            qtdsAlteracoesPRsMergeadas.append(float(linha[3]) + float(linha[4]))
            temposPRsMergeadas.append(float(linha[5]))
            tamanhosDescricaPRsMergeadas.append(float(linha[6]))
            qtdsParticipantePRsPRsMergeadas.append(float(linha[7]))
            qtdsComentariosPRsMergeadas.append(float(linha[8]))

mediaArquivosPrsFechadas = statistics.mean(qtdsArquivosPRsFechadas)
mediaArquivosPrsMergeadas = statistics.mean(qtdsArquivosPRsMergeadas)
medianaArquivosPrsFechadas = statistics.median(qtdsArquivosPRsFechadas)
medianaArquivosPrsMergeadas = statistics.median(qtdsArquivosPRsMergeadas)

mediaAlteracoesPrsFechadas = statistics.mean(qtdsAlteracoesPRsFechadas)
mediaAlteracoesPrsMergeadas = statistics.mean(qtdsAlteracoesPRsMergeadas)
medianaAlteracoesPrsFechadas = statistics.median(qtdsAlteracoesPRsFechadas)
medianaAlteracoesPrsMergeadas = statistics.median(qtdsAlteracoesPRsMergeadas)

mediaTemposPrsFechadas = statistics.mean(temposPRsFechadas)
mediaTemposPrsMergeadas = statistics.mean(temposPRsMergeadas)
medianaTemposPrsFechadas = statistics.median(temposPRsFechadas)
medianaTemposPrsMergeadas = statistics.median(temposPRsMergeadas)

mediaDescricaoPrsFechadas = statistics.mean(tamanhosDescricaPRsFechadas)
mediaDescricaoPrsMergeadas = statistics.mean(tamanhosDescricaPRsMergeadas)
medianaDescricaoPrsFechadas = statistics.median(tamanhosDescricaPRsFechadas)
medianaDescricaoPrsMergeadas = statistics.median(tamanhosDescricaPRsMergeadas)

mediaParticipantesPrsFechadas = statistics.mean(qtdsParticipantePRsFechadas)
mediaParticipantesPrsMergeadas = statistics.mean(qtdsParticipantePRsPRsMergeadas)
medianaParticipantesPrsFechadas = statistics.median(qtdsParticipantePRsFechadas)
medianaParticipantesPrsMergeadas = statistics.median(qtdsParticipantePRsPRsMergeadas)

mediaComentariosPrsFechadas = statistics.mean(qtdsComentariosPRsFechadas)
mediaComentariosPrsMergeadas = statistics.mean(qtdsComentariosPRsMergeadas)
medianaComentariosPrsFechadas = statistics.median(qtdsComentariosPRsFechadas)
medianaComentariosPrsMergeadas = statistics.median(qtdsComentariosPRsMergeadas)

## Plotando os gráficos:
### Media arquivos
plt.bar(["Recusadas", "Aceitas"], [mediaArquivosPrsFechadas, mediaArquivosPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Média de arquivos')
plt.title('Resultado da revisão X Quantidade média de arquivos das PRs')

plt.show()

### Mediana arquivos
plt.bar(["Recusadas", "Aceitas"], [medianaArquivosPrsFechadas, medianaArquivosPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana de arquivos')
plt.title('Resultado da revisão X Quantidade mediana de arquivos das PRs')

plt.show()


### Media alteracoes
plt.bar(["Recusadas", "Aceitas"], [mediaAlteracoesPrsFechadas, mediaAlteracoesPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Média de alterações em linhas')
plt.title('Resultado da revisão X Quantidade média de alteracoes em linhas das PRs')

plt.show()


### Mediana alteracoes
plt.bar(["Recusadas", "Aceitas"], [medianaAlteracoesPrsFechadas, medianaAlteracoesPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana de alteracoes')
plt.title('Resultado da revisão X Quantidade mediana de alteracoes em linhas das PRs')

plt.show()


### Media tempo
plt.bar(["Recusadas", "Aceitas"], [mediaTemposPrsFechadas, mediaTemposPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Média de tempos para revisão')
plt.title('Resultado da revisão X Tempo médio para revisão das PRs')

plt.show()


### Mediana tempo
plt.bar(["Recusadas", "Aceitas"], [medianaTemposPrsFechadas, medianaTemposPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana de tempos para revisão')
plt.title('Resultado da revisão X Mediana do tempo para revisão das PRs')

plt.show()


### Mediana tempo
plt.bar(["Recusadas", "Aceitas"], [medianaTemposPrsFechadas, medianaTemposPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana de tempos para revisão')
plt.title('Resultado da revisão X Tempo médio para revisão das PRs')

plt.show()


### Média tamanho descrição
plt.bar(["Recusadas", "Aceitas"], [mediaDescricaoPrsFechadas, mediaDescricaoPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Tamanho médio da descrição')
plt.title('Resultado da revisão X Tamanho médio da descrição')

plt.show()


### Mediana tamanho descrição
plt.bar(["Recusadas", "Aceitas"], [medianaDescricaoPrsFechadas, medianaDescricaoPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana do tamanho da descrição')
plt.title('Resultado da revisão X Mediana do tamanho da descrição')

plt.show()


### Média participantes
plt.bar(["Recusadas", "Aceitas"], [mediaParticipantesPrsFechadas, mediaParticipantesPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Média dos participantes nas PRs')
plt.title('Resultado da revisão X Quantidade média de participantes na PR')

plt.show()


### Mediana participantes
plt.bar(["Recusadas", "Aceitas"], [medianaParticipantesPrsFechadas, medianaParticipantesPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana dos participantes nas PRs')
plt.title('Resultado da revisão X Quantidade mediana de participantes nas PRs')

plt.show()


### Média comentários
plt.bar(["Recusadas", "Aceitas"], [mediaComentariosPrsFechadas, mediaComentariosPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Quantidade média de comentários nas PRs')
plt.title('Resultado da revisão X Quantidade média de comentários nas PRs')

plt.show()


### Mediana comentários
plt.bar(["Recusadas", "Aceitas"], [medianaComentariosPrsFechadas, medianaComentariosPrsMergeadas], color='skyblue')

plt.xlabel('Resultado final da revisão')
plt.ylabel('Mediana de comentários nas PRs')
plt.title('Resultado da revisão X Quantidade mediana de comentários nas PRs')

plt.show()