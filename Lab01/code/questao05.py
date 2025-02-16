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
                    primaryLanguage{{
                    name
                    }}
                }}
            }}
        }}
    }}"""
  resposta = requests.post(url, headers= header, json= {"query": body})
  return resposta

# Criando lista para armazenar linguagens mais populares:
linguagensMaisPopulares = ["Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "PHP", "Shell", "C", "Go"]
contemLinguagemPopular = []
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
        if valor["primaryLanguage"] is not None:
            linguagem = valor["primaryLanguage"]["name"]
            if linguagem in linguagensMaisPopulares:
                contemLinguagemPopular.append(True)
            else:
                contemLinguagemPopular.append(False)
      print(f"{(contemLinguagemPopular.count(True)) / len(contemLinguagemPopular) * 100}% dos repositórios mais populares têm como linguagem principal alguma das 10 linguagens mais populares do GitHub")
  else:
    print("Erro ao acessar API do GitHub")
    print("Código do erro:")
    print(resposta.status_code)
    print("Corpo do erro:")
    print(resposta.json())