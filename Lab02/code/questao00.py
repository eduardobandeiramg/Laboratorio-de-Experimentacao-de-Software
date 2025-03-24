# Código que extrai os repositórios com todas as informações desejadas (popularidade, maturidade, atividade e tamanho) e calcula as métricas de qualidade para cada um deles

## Primeira parte: Extraindo informações sobre os 1000 repositórios Java mais populares:
import requests
from datetime import datetime
import csv
import time
import pandas as pd

### Definindo a função para requisição:
def fazerQuery(estrelas):
  token = ""
  url = "https://api.github.com/graphql"
  header = {"Authorization": f"Bearer {token}" , "Content-Type": "application/json"}
  body = f"""query {{
        search(query: "stars:>{estrelas} language:Java", type: REPOSITORY, first: 50) {{
            nodes {{
                ... on Repository {{
                    name
                    primaryLanguage{{name}}
                    stargazerCount
                    createdAt
                    releases{{totalCount}}
                    url
                }}
            }}
            pageInfo{{
            hasNextPage
            endCursor
            }}
        }}
    }}"""
  resposta = requests.post(url, headers= header, json= {"query": body})
  return resposta

### Definindo a função para requisição COM PAGINAÇÃO:
def fazerQueryComPaginacao(estrelas , aPartirDe):
  token = ""
  url = "https://api.github.com/graphql"
  header = {"Authorization": f"Bearer {token}" , "Content-Type": "application/json"}
  body = f"""query {{
        search(query: "stars:>{estrelas} language:Java", type: REPOSITORY, first: 50 , after: "{aPartirDe}") {{
            nodes {{
                ... on Repository {{
                    name
                    primaryLanguage{{name}}
                    stargazerCount
                    createdAt
                    releases{{totalCount}}
                    url
                }}
            }}
            pageInfo{{
            hasNextPage
            endCursor
            }}
        }}
    }}"""
  resposta = requests.post(url, headers= header, json= {"query": body})
  return resposta

### Criando variaveis de controle dos loops:
continuaLoop = True
loopDeContagem = True
### Criando variavel para armazenar localizacao do ultimo item:
cursorfinal = ""
### Definindo numero considerável de estrelas:
qtdEstrelas = 150000
### Criando lista de linhas para o csv:
linhasDaPlanilha = [["Repositório", "Linguagem principal", "Url", "Estrelas", "Idade em anos", "Número de releases", "Total de linhas"]]
### Recuperando data atual para cálculo da idade dos repositórios:
agora = datetime.now()

### Consumindo API procurando repositórios e criando o CSV com os dados desses repositórios:
while continuaLoop:
  #### Reinicializando loop de contagem:
  loopDeContagem = True
  #### Criando lista para armazenar repositorios:
  repos = []
  time.sleep(1)
  resposta = fazerQuery(qtdEstrelas)
  if resposta.status_code == 200:
    respostaRequisicao = resposta.json()
    print(f"{len(respostaRequisicao["data"]["search"]["nodes"])} REPOSITÓRIOS NA PRIMEIRA PAGINA")
    while loopDeContagem:
      if len(respostaRequisicao["data"]["search"]["nodes"]) > 0:
        repos.extend(respostaRequisicao["data"]["search"]["nodes"])
      print(f"REPOSITORIOS ENCONTRADOS ATÉ AGORA: {len(repos)}")
      if respostaRequisicao["data"]["search"]["pageInfo"]["hasNextPage"] == False:
        loopDeContagem = False
        print("Nao tem proxima pagina")
      else:
        time.sleep(1)
        cursorfinal = respostaRequisicao["data"]["search"]["pageInfo"]["endCursor"]
        resposta = fazerQueryComPaginacao(qtdEstrelas , cursorfinal)
        respostaRequisicao = resposta.json()
    if len(repos) < 1000:
      qtdEstrelas -= 5000
    else:
      loop = 1
      continuaLoop = False
      for valor in repos:
        print(f"{str(loop)}º Repositório mais popular do GitHub:")
        loop+=1
        print(valor)
        #### Calculando idade do repositório:
        dataCriacao = datetime.strptime(valor["createdAt"] , f"%Y-%m-%dT%H:%M:%SZ")
        idade = ((agora - dataCriacao).days)/365
        linhasDaPlanilha.append([valor["name"], valor["primaryLanguage"]["name"], valor["url"], valor["stargazerCount"], idade, valor["releases"]["totalCount"], "Ainda sem dados"])
      #### Gerando a planilha com os dados obtidos:
      with open("planilha_repositorios.csv", mode= "w", newline= "", encoding= "utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)
  else:
    print("Erro ao acessar API do GitHub")
    print("Descrição do erro:")
    print(resposta.status_code)





## Segunda Parte: Extraindo métricas de qualidade para cada um dos 1000 repositórios:
import subprocess, os, shutil
from pathlib import Path
import statistics

### Recuperando hora atual para calcular tempo de execucao:
inicio = datetime.now()

### Criando as pastas onde os arquivos serao criados:
subprocess.run(["mkdir", "diretorio_repositorio"])
subprocess.run(["mkdir", "diretorio_resultados"])

### Percorrendo o CSV com dados dos repositórios para obter métricas:
linhasDaPlanilha = [["Repositório", "Linguagem Principal", "Url", "Estrelas", "Idade em anos", "Número de releases", "Total de linhas", "Média de CBO's", "Mediana de CBO's", "Desvio Padrão de CBO's", "Média de DIT's", "Mediana de DIT's", "Desvio Padrão de DIT's", "Média de LCOM's", "Mediana de LCOM's", "Desvio Padrão de LCOM's"]]

with open("planilha_repositorios.csv", mode="r", encoding="utf-8", newline="") as arquivoRepos:
    planilhaRepos = csv.reader(arquivoRepos)
    next(planilhaRepos)
    variavelControle = 1
    for linha in planilhaRepos:
        print(f"\nTrabalhando sobre o repositório numero {variavelControle}")
        variavelControle+=1
        novaLinha = []
        novaLinha.extend([linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]])
        url_repositorio = linha[2]
        #### Comando para clonar repositório:
        try:
            pasta_repositorio_clonado = "diretorio_repositorio"
            resultado_clonagem = subprocess.run(["git", "clone", url_repositorio], check=True, text=True, cwd=pasta_repositorio_clonado)
            print(f"resultado da clonagem: {resultado_clonagem.returncode}")
            print(f"resultado da clonagem: {resultado_clonagem.stdout}")
            ##### Obtendo o caminho absoluto da pasta do repositorio:
            caminho_absoluto_repositorio = Path(f"{pasta_repositorio_clonado}/{linha[0]}").resolve()
            ##### Obtendo o caminho absoluto da pasta de resultados:
            caminho_absoluto_resultados = Path(f"diretorio_resultados/metricas_{linha[0]}_").resolve()
            ##### Comando CK:
            comando_ck = ["java",  "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", caminho_absoluto_repositorio, "use_jars:true", "0", "variables_and_fields_metrics:true", caminho_absoluto_resultados]
            ##### Executando o comando ck na pasta do repositorio clonado:
            resultado_ck = subprocess.run(comando_ck, cwd="CK/target")
            ##### Pegando as métricas:
            cbos = []
            dits = []
            lcoms = []
            linhasDeCodigo = []
            with open(f"diretorio_resultados/metricas_{linha[0]}_class.csv", mode="r", newline="", encoding="utf-8") as arquivoMetricas:
                planilhaMetricas = csv.reader(arquivoMetricas)
                next(planilhaMetricas)
                for linha2 in planilhaMetricas:
                    cbos.append(int(linha2[3]))
                    dits.append(int(linha2[8]))
                    lcoms.append(int(linha2[11]))
                    linhasDeCodigo.append(int(linha2[34]))
            ##### Obtendo quantidade total de linhas:
            if len(linhasDeCodigo) != 0:
                linhasDeCodigo = sum(linhasDeCodigo)
                print(f"Linhas de código: {linhasDeCodigo}")
            else:
                linhasDeCodigo = "Sem dados"
            ##### Obtendo os valores de medida central:
            ##### Dos CBO's
            if len(cbos) == 0:
                mediaCbos = "Sem dados"
                medianaCbos = "Sem dados"
                desvioPadraoCbos = "Sem dados"
            else:            
                mediaCbos = statistics.mean(cbos)
                medianaCbos = statistics.median(cbos)
                desvioPadraoCbos = statistics.stdev(cbos)
            ##### Das DIT's:
            if len(dits) == 0:
                mediaDits = "Sem dados"
                medianaDits = "Sem dados"
                desvioPadraoDits = "Sem dados"
            else:
                mediaDits = statistics.mean(dits)
                medianaDits = statistics.median(dits)
                desvioPadraoDits = statistics.stdev(dits)
            ##### Dos LCOM's:
            if len(lcoms) == 0:
                mediaLcoms = "Sem dados"
                medianaLcoms = "Sem dados"
                desvioPadraoLcoms = "Sem dados"
            else:
                mediaLcoms = statistics.mean(lcoms)
                medianaLcoms = statistics.median(lcoms)
                desvioPadraoLcoms = statistics.stdev(lcoms)

            ##### Adicionando métricas na linha da planilha final:
            novaLinha[6] = linhasDeCodigo
            novaLinha.extend([mediaCbos, medianaCbos, desvioPadraoCbos, mediaDits, medianaDits, desvioPadraoDits, mediaLcoms, medianaLcoms, desvioPadraoLcoms])
            linhasDaPlanilha.append(novaLinha)

            #### Apagando arquivos gerados (arquivos de resultados da ferramenta ck e diretorio do repositorio clonado):
            os.remove(Path(f"diretorio_resultados/metricas_{linha[0]}_class.csv").resolve())
            os.remove(Path(f"diretorio_resultados/metricas_{linha[0]}_method.csv").resolve())
            #### subprocess.run(["rm", "-rf", ".git"], cwd=caminho_absoluto_repositorio)
            shutil.rmtree(caminho_absoluto_repositorio)
        except Exception as e:
            #### Adicionando mensagem de erro de clonagem nos campos da linha do repositório:
            novaLinha[6] = "Erro ao clonar repositório"
            novaLinha.extend(["Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório"])
            linhasDaPlanilha.append(novaLinha)

### Criando CSV com todas as métricas para cada repositório:
with open("diretorio_resultados/resultados_finais.csv", mode="w", encoding="utf-8", newline="") as arquivoFinal:
    csv.writer(arquivoFinal).writerows(linhasDaPlanilha)

### Apagando planilha inicial:
# os.remove(Path("planilha_repositorios.csv").resolve())

### Apagando diretorio de repositórios clonados:
shutil.rmtree(Path("diretorio_repositorio").resolve())

### Recuperando hora final:
fim = datetime.now()
tempoTotal = (fim - inicio).seconds
print(f"Tempo total de execução: {tempoTotal/3600} horas")





## Terceira Parte: Realizando teste de correlação:
import matplotlib.pyplot as plt
import seaborn as sns
### Gerando nova planilha limpa para calcular correlação
linhasDaPlanilha = [["Estrelas", "Idade em anos", "Releases", "Linhas totais", "Media de CBO's", "Mediana de CBO's", "Media de DIT's", "Mediana de DIT's", "Media de LCOM's", "Mediana de LCOM's"]]
with open("diretorio_resultados/resultados_finais.csv", mode="r", newline="", encoding="utf-8") as arquivo:
    planilha = csv.reader(arquivo)
    for linha in planilha:
        try:
            qtdEstrelas = float(linha[3])
            idade = float(linha[4])
            releases = float(linha[5])
            linhas = float(linha[6])
            qtdMediaCbos = float(linha[7])
            qtdMedianaCbos = float(linha[8])
            qtdMediaDits = float(linha[10])
            qtdMedianaDits = float(linha[11])
            qtdMediaLcoms = float(linha[13])
            qtdMedianaLcoms = float(linha[14])
            novaLinha = [qtdEstrelas, idade, releases, linhas, qtdMediaCbos, qtdMedianaCbos, qtdMediaDits, qtdMedianaDits, qtdMediaLcoms, qtdMedianaLcoms]
            linhasDaPlanilha.append(novaLinha)
        except Exception as e:
             continue
with open("diretorio_resultados/planilha_base_correlacao.csv", mode="w", encoding="utf-8", newline="") as arquivo:
    planilha2 = csv.writer(arquivo)
    planilha2.writerows(linhasDaPlanilha)
    
### Gerando matriz de correlação de Pearson:
matriz = pd.read_csv("diretorio_resultados/planilha_base_correlacao.csv", encoding="utf-8")
matrizCorr = matriz.corr()
matriz.corr().to_csv("diretorio_resultados/resultado_correlacao.csv")

### Gerando grafico de calor:
plt.figure(figsize=(6, 4))
sns.heatmap(matrizCorr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlação")
plt.show()