import requests
import csv
import time

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
                    url
                    pullRequests(states:MERGED){{
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
        search(query: "stars:>{estrelas}", type: REPOSITORY, first: 100 , after: "{aPartirDe}") {{
            nodes {{
                ... on Repository {{
                    name
                    stargazerCount
                    url
                    pullRequests(states:MERGED){{
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
# Criando variavel para armazenar localizacao do ultimo item:
cursorfinal = ""
# Definindo numero alto de estrelas:
qtdEstrelas = 420000
# Criando lista de linhas para o csv:
linhasDaPlanilha = [["Repositório", "Estrelas", "PR's mergeadas", "url"]]

while continuaLoop:
  # Reinicializando loop de contagem:
  loopDeContagem = True
  # Criando lista para armazenar repositorios:
  repos = []
  time.sleep(2)
  resposta = fazerQuery(qtdEstrelas)
  if resposta.status_code == 200:
    respostaRequisicao = resposta.json()
    while loopDeContagem:
      if len(respostaRequisicao["data"]["search"]["nodes"]) > 0:
        repos.extend(respostaRequisicao["data"]["search"]["nodes"])
      print(f"REPOSITORIOS ENCONTRADOS ATÉ AGORA: {len(repos)}")
      # removendo da lista repositorio com menos de 100 pull requests mergeadas
      for repositorio in repos:
        if repositorio["pullRequests"]["totalCount"] < 100:
          repos.remove(repositorio)
      if respostaRequisicao["data"]["search"]["pageInfo"]["hasNextPage"] == False:
        loopDeContagem = False
        print("Nao tem proxima pagina")
      else:
        time.sleep(2)
        cursorfinal = respostaRequisicao["data"]["search"]["pageInfo"]["endCursor"]
        resposta = fazerQueryComPaginacao(qtdEstrelas , cursorfinal)
        respostaRequisicao = resposta.json()
    if len(repos) < 300:
      qtdEstrelas -= 5000
    else:
      loop = 1
      continuaLoop = False
      for valor in repos:
        print(f"{str(loop)}º Repositório mais popular do GitHub e com mais de 100 PR's mergeadas:")
        print(valor)
        linhasDaPlanilha.append([valor["name"], valor["stargazerCount"], valor["pullRequests"]["totalCount"], valor["url"]])
        loop+=1
      # Gerando a planilha com os dados obtidos:
      with open("Lab03/planilhas/lista_base_repositorios.csv", mode= "w", newline= "", encoding= "utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)

  else:
    print("Erro ao acessar API do GitHub")
    print("Descrição do erro:")
    print(resposta.status_code)