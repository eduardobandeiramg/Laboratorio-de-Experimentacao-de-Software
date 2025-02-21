import requests
from datetime import datetime
import statistics
import csv

# Definindo a função para requisição:
def fazerQuery(estrelas):
  token = ""
  url = "https://api.github.com/graphql"
  header = {"Authorization": f"Bearer {token}" , "Content-Type": "application/json"}
  body = f"""query {{
        search(query: "stars:>{estrelas}", type: REPOSITORY, first: 100) {{
            nodes {{
                ... on Repository {{
                    name
                    stargazerCount
                    latestRelease{{
                    publishedAt
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
        search(query: "stars:>{estrelas}", type: REPOSITORY, first: 100 , after: "{aPartirDe}") {{
            nodes {{
                ... on Repository {{
                    name
                    stargazerCount
                    latestRelease{{
                    publishedAt
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
# Buscando TimeStamp de agora:
agora = datetime.now()
# Criando lista para armazenar tempos desde última release:
temposDesdeUltimaRelease = []
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
linhasDaPlanilha = [["Repositório", "Estrelas", "Data da última release", "Dias desde última release", "Mediana"]]

while continuaLoop:
  # Reinicializando loop de contagem:
  loopDeContagem = True
  # Criando lista para armazenar repositorios:
  repos = []
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
        cursorfinal = respostaRequisicao["data"]["search"]["pageInfo"]["endCursor"]
        resposta = fazerQueryComPaginacao(qtdEstrelas , cursorfinal)
        respostaRequisicao = resposta.json()
    if len(repos) < 1000:
      qtdEstrelas -= 5000
    else:
      continuaLoop = False
      loop = 1
      for valor in repos:
        dados = [valor["name"], valor["stargazerCount"], "Sem dados", "Sem dados", "Sem dados"]
        print(f"{str(loop)}º Repositório mais popular do GitHub:")
        loop+=1
        print(valor)
        if valor["latestRelease"] is not None:
          ultimoLancamento = datetime.strptime(valor["latestRelease"]["publishedAt"] , f"%Y-%m-%dT%H:%M:%SZ")
          tempoDesdeUltimoLancamento = agora - ultimoLancamento
          temposDesdeUltimaRelease.append(tempoDesdeUltimoLancamento.days)
          dados[2] = valor["latestRelease"]["publishedAt"]
          dados[3] = tempoDesdeUltimoLancamento.days
          dados[4] = statistics.median(temposDesdeUltimaRelease)
        linhasDaPlanilha.append(dados)
      print(f"Lista das quantidades de dias desde a última release: {temposDesdeUltimaRelease}")
      print(f"Quantidade de repositórios populares que lançaram releases: {len(temposDesdeUltimaRelease)}")
      print(f"Mediana da quantidade de dias desde a última release: {statistics.median(temposDesdeUltimaRelease)}")
      with open("questao04.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)
  else:
    print("Erro ao acessar API do GitHub")
    print("Código do erro:")
    print(resposta.status_code)
    print("Corpo do erro:")
    print(resposta.json())