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
                    primaryLanguage{{
                    name
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
                    primaryLanguage{{
                    name
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
# Criando lista para armazenar linguagens mais populares:
linguagensMaisPopulares = ["Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "PHP", "Shell", "C", "Go"]
contemLinguagemPopular = []
# Criando variavel para armazenar localizacao do ultimo item:
cursorfinal = ""
# Definindo numero alto de estrelas:
qtdEstrelas = 420000
# Criando lista de linhas para o csv:
linhasDaPlanilha = [["Repositório", "Estrelas", "Linguagem Primária", "Linguagem Primária é Top-10?", "Percentual que utiliza linguagem popular"]]

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
        dados = [valor["name"], valor["stargazerCount"], "Sem informação", "Sem informação", 0]
        print(f"{str(loop)}º Repositório mais popular do GitHub:")
        loop+=1
        print(valor)
        if valor["primaryLanguage"] is not None:
            linguagem = valor["primaryLanguage"]["name"]
            dados[2] = linguagem
            if linguagem in linguagensMaisPopulares:
                contemLinguagemPopular.append(True)
                dados[3] = "Sim"
            else:
                contemLinguagemPopular.append(False)
                dados[3] = "Não"
        if len(contemLinguagemPopular) > 0:
          dados[4] = contemLinguagemPopular.count(True)/len(contemLinguagemPopular)
        linhasDaPlanilha.append(dados)
      with open("questao05.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)
      print(f"{(contemLinguagemPopular.count(True)) / len(contemLinguagemPopular) * 100}% dos repositórios mais populares têm como linguagem principal alguma das 10 linguagens mais populares do GitHub")
  else:
    print("Erro ao acessar API do GitHub")
    print("Código do erro:")
    print(resposta.status_code)
    print("Corpo do erro:")
    print(resposta.json())
