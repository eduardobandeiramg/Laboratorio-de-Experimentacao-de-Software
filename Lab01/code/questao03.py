import requests
from datetime import datetime
import statistics
import csv
import matplotlib.pylab as plt
import seaborn as sns
import time

# Definindo a função para requisição:
def fazerQuery(estrelas):
  token = ""
  url = "https://api.github.com/graphql"
  header = {"Authorization": f"Bearer {token}" , "Content-Type": "application/json"}
  body = f"""query {{
        search(query: "stars:>{estrelas}", type: REPOSITORY, first: 20) {{
            nodes {{
                ... on Repository {{
                    name
                    stargazerCount
                    releases{{
                    totalCount
                    }}
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

# Definindo a função para requisição COM PAGINAÇÃO:
def fazerQueryComPaginacao(estrelas , aPartirDe):
  token = ""
  url = "https://api.github.com/graphql"
  header = {"Authorization": f"Bearer {token}" , "Content-Type": "application/json"}
  body = f"""query {{
        search(query: "stars:>{estrelas}", type: REPOSITORY, first: 20 , after: "{aPartirDe}") {{
            nodes {{
                ... on Repository {{
                    name
                    stargazerCount
                    releases{{
                    totalCount
                    }}
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

# Criando variaveis de controle dos loops:
continuaLoop = True
loopDeContagem = True
# Criando lista que armazenará os totais de releases:
releases = []
# Criando variavel para armazenar localizacao do ultimo item:
cursorfinal = ""
# Definindo numero alto de estrelas:
qtdEstrelas = 420000
# Criando lista de linhas para o csv:
linhasDaPlanilha = [["Repositório", "Estrelas", "Total de Releases", "Mediana"]]

while continuaLoop:
  # Reinicializando loop de contagem:
  loopDeContagem = True
  # Criando lista para armazenar repositorios:
  repos = []
  time.sleep(2)
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
        time.sleep(2)
        cursorfinal = respostaRequisicao["data"]["search"]["pageInfo"]["endCursor"]
        resposta = fazerQueryComPaginacao(qtdEstrelas , cursorfinal)
        respostaRequisicao = resposta.json()
    if len(repos) < 1000:
      qtdEstrelas -= 5000
    else:
      continuaLoop = False
      loop = 1
      for valor in repos:
        print(f"{str(loop)}º Repositório mais popular do GitHub:")
        loop+=1
        print(valor)
        if valor["releases"] is not None:
          release = valor["releases"]["totalCount"]
          releases.append(release)
        else:
          release = 0
          releases.append(0)
        linhasDaPlanilha.append([valor["name"], valor["stargazerCount"], release, statistics.median(releases)])
      print(f"Lista das quantidades totais de releases: {releases}")
      print(f"Mediana das quantidades totais de releases: {statistics.median(releases)}")
      # Gerando a planilha com os dados obtidos:
      with open("questao03.csv", mode= "w", newline= "", encoding= "utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)
      # Gerando o gráfico com os dados obtidos:
      plt.hist(releases, bins=16, color='skyblue', edgecolor='black')
      plt.title('Distribuição das quantidades totais de releases lançadas')
      plt.xlabel('Releases lançadas')
      plt.ylabel('Frequência')
      plt.show()
      # Gerando o zoom do grafico de dispersão:
      plt.hist(releases, bins= [0,5,10,15,20,25,30,40,50,100,150,200], color='skyblue', edgecolor='black')
      plt.title('Distribuição das quantidades totais de releases lançadas')
      plt.xlabel('Releases lançadas')
      plt.ylabel('Frequência')
      plt.show()
      # Gerando o gráfico com curva de distribuição:
      sns.histplot(releases, kde=True)
      plt.title('Distribuição das quantidades totais de releases lançadas')
      plt.xlabel('Releases lançadas')
      plt.ylabel('Frequência')
      plt.show()
      # Gerando o gráfico boxplot:
      plt.boxplot(releases)
      plt.title('Distribuição das quantidades de releases lançadas')
      plt.xlabel("Releases lançadas")
      plt.ylabel("Frequência")
      plt.show()
  else:
    print("Erro ao acessar API do GitHub")
    print("Código do erro:")
    print(resposta.status_code)
    print("Corpo do erro:")
    print(resposta.json())