# Código para análise da relação entre popularidade dos repositórios e suas métricas de qualidade
import csv
import matplotlib.pyplot as plt

## Gerando os gráficos:
### Definindo listas:
estrelas = []
mediaCbos = []
mediaLcoms = []

### Enchendo listas com quantidades de estrelas e respectivas métricas
with open("diretorio_resultados/resultados_finais.csv", newline="", encoding="utf-8", mode="r") as arquivo:
    planilha = csv.reader(arquivo)
    for linha in planilha:
        if linha[7] != "Sem dados" and linha[7] != "Erro ao clonar repositório":
            estrelas.append(linha[3])
            mediaCbos.append(linha[7])

plt.scatter(estrelas, mediaCbos)
plt.xlabel('Estrelas do repositório')
plt.ylabel('Média de CBOs')
plt.title('Relação qtd estrelas / média de cbos')
plt.legend()
plt.show()


### Enchendo listas com quantidades de estrelas e respectivas métricas
### Reinicializando lista de quantidades de estrelas:
estrelas = []
with open("diretorio_resultados/resultados_finais.csv", newline="", encoding="utf-8", mode="r") as arquivo:
    planilha = csv.reader(arquivo)
    for linha in planilha:
        if linha[13] != "Sem dados" and linha[13] != "Erro ao clonar repositório":
            estrelas.append(linha[13])
            mediaLcoms.append(linha[13])

plt.scatter(estrelas, mediaLcoms, color='blue', marker='o', label='Pontos')
plt.xlabel('Estrelas do repositório')
plt.ylabel('Média de LCOMs')
plt.title('Relação qtd estrelas / média de lcoms')
plt.legend()
plt.show()

