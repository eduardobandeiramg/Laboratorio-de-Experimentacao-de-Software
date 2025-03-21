# Código que extrai os repositórios com todas as informações desejadas (popularidade, maturidade, atividade e tamanho) e calcula as métricas de qualidade para cada um deles

import requests
from datetime import datetime
import csv
import time

# Definindo a função para requisição:
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

# Definindo a função para requisição COM PAGINAÇÃO:
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

# Criando variaveis de controle dos loops:
continuaLoop = True
loopDeContagem = True
# Criando variavel para armazenar localizacao do ultimo item:
cursorfinal = ""
# Definindo numero considerável de estrelas:
qtdEstrelas = 150000
# Criando lista de linhas para o csv:
linhasDaPlanilha = [["Repositório", "Linguagem principal", "Url", "Estrelas", "Idade em anos", "Número de releases", "Total de linhas"]]
# Recuperando data atual para cálculo da idade dos repositórios:
agora = datetime.now()

# Consumindo API procurando repositórios e criando o CSV com os dados desses repositórios:
while continuaLoop:
  # Reinicializando loop de contagem:
  loopDeContagem = True
  # Criando lista para armazenar repositorios:
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
        # Calculando idade do repositório:
        dataCriacao = datetime.strptime(valor["createdAt"] , f"%Y-%m-%dT%H:%M:%SZ")
        idade = ((agora - dataCriacao).days)/365
        linhasDaPlanilha.append([valor["name"], valor["primaryLanguage"]["name"], valor["url"], valor["stargazerCount"], idade, valor["releases"]["totalCount"], "Ainda sem dados"])
      # Gerando a planilha com os dados obtidos:
      with open("questao01.csv", mode= "w", newline= "", encoding= "utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)
  else:
    print("Erro ao acessar API do GitHub")
    print("Descrição do erro:")
    print(resposta.status_code)