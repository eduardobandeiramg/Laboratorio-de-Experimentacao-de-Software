import requests
from datetime import datetime
import statistics

# Definindo quantidade de repositóris desejados:
qtdRepositorios = 100

# organizando função para a requisição:
def fazerQuery(estrelas):
  token = ""
  url = "https://api.github.com/graphql"
  header = {"Authorization": f"Bearer {token}" , "Content-Type": "application/json"}
  body = f"""query {{
        search(query: "stars:>{estrelas}", type: REPOSITORY, first: {qtdRepositorios}) {{
            nodes {{
                ... on Repository {{
                    name
                    stargazerCount
                    releases{{totalCount}}
                }}
            }}
        }}
    }}"""
  resposta = requests.post(url, headers= header, json= {"query": body})
  return resposta

# Criando lista para armazenar idades dos repositorios:
releases = []
# Criando variavel de controle do loop:
continuaLoop = True
# Definindo numero alto de estrelas:
qtdEstrelas = 420000

while continuaLoop:
  resposta = fazerQuery(qtdEstrelas)
  if resposta.status_code == 200:
    respostaRequisicao = resposta.json()
    qtd = len(respostaRequisicao["data"]["search"]["nodes"])
    print(f"Quantidade de repositorios encontrados com mais de {qtdEstrelas} estrelas: {qtd}")
    if qtd > 0:
      print(f"Repositório encontrado: {respostaRequisicao["data"]["search"]["nodes"][qtd-1]["name"]}, com {respostaRequisicao["data"]["search"]["nodes"][qtd-1]["stargazerCount"]} estrelas")
    if qtd < qtdRepositorios:
      qtdEstrelas -= 3000
    else:
      continuaLoop = False
      loop = 1
      print("\nENCONTRADOS OS 100 REPOSITORIOS MAIS POPULARES!!")
      for valor in resposta.json()["data"]["search"]["nodes"]:
        print(f"{str(loop)}º Repositório mais popular do GitHub:")
        loop+=1
        print(valor)
        releases.append(valor["releases"]["totalCount"])
      print(f"Lista das quantidades totais de releases: {releases}")
      print(f"Mediana das quantidades totais de releases: {statistics.median(releases)}")
  else:
    print("Erro ao acessar API do GitHub")
    print("Código do erro:")
    print(resposta.status_code)
    print("Corpo do erro:")
    print(resposta.json())