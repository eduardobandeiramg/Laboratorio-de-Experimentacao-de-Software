import requests
from datetime import datetime
import statistics
import csv
import matplotlib.pyplot as plt
import seaborn as sns
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
                    issuesTotais: issues{{
                    totalCount
                    }}
                    issuesFechadas: issues(states: CLOSED){{
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
                    issuesTotais: issues{{
                    totalCount
                    }}
                    issuesFechadas: issues(states: CLOSED){{
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
# Criando lista que armazenará as razões de issues fechadas / issues totais
listaDeRazoes = []
# Criando variavel para armazenar localizacao do ultimo item:
cursorfinal = ""
# Definindo numero alto de estrelas:
qtdEstrelas = 420000
# Criando lista de linhas para o csv:
linhasDaPlanilha = [["Repositório", "Estrelas", "Issues Totais", "Issues fechadas", "Razão de issues fechadas", "Mediana"]]

while continuaLoop:
  # Reinicializando loop de contagem:
  loopDeContagem = True
  # Criando lista para armazenar repositorios:
  repos = []
  time.sleep(2)
  resposta = fazerQuery(qtdEstrelas)
  if resposta.status_code == 200:
    respostaRequisicao = resposta.json()
    print(f"resposta da requisicao: {resposta.headers}")
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
        print(f"resposta da requisicao: {resposta.headers}")

    if len(repos) < 1000:
      qtdEstrelas -= 5000
    else:
      continuaLoop = False
      loop = 1
      for valor in repos:
        dados = [valor["name"], valor["stargazerCount"], "Sem dados", "Sem dados", "Sem dados", "Sem dados"]
        print(f"{str(loop)}º Repositório mais popular do GitHub:")
        loop+=1
        print(valor)
        if ((valor["issuesTotais"] is not None) and (valor["issuesFechadas"] is not None)) and (valor["issuesTotais"]["totalCount"] != 0):
            dados[2] = valor["issuesTotais"]["totalCount"]
            dados[3] = valor["issuesFechadas"]["totalCount"]
            dados[4] = valor["issuesFechadas"]["totalCount"] / valor["issuesTotais"]["totalCount"]
            listaDeRazoes.append(valor["issuesFechadas"]["totalCount"] / valor["issuesTotais"]["totalCount"])
            print(f"ISSUES TOTAIS: {valor["issuesTotais"]["totalCount"]} \n ISSUES FECHADAS: {valor["issuesFechadas"]["totalCount"]} \n RAZÃO: {valor["issuesFechadas"]["totalCount"] / valor["issuesTotais"]["totalCount"]}")
        dados[5] = statistics.median(listaDeRazoes)
        linhasDaPlanilha.append(dados)
      print(f"Mediana das razões entre issues fechadas e issues totais dos 1000 repositórios mais populares do GitHub: {statistics.median(listaDeRazoes)}")
      # Gerando a planilha com os resultados obtidos:
      with open("questao06.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        csv.writer(arquivo).writerows(linhasDaPlanilha)
      razoes = []
      razoesInteiros = []
      with open("questao06.csv", mode="r", newline="", encoding="utf-8") as arquivo:
          file = csv.reader(arquivo)
          for row in file:
              razoes.append(row[4])
      razoes.pop(0)
      for razao in razoes:
          if razao != "Sem dados":
              razoesInteiros.append(float(razao))
      plt.hist(razoesInteiros, bins=10, color='skyblue', edgecolor='black')
      # sns.histplot(razoes, kde=True)
      plt.title('Distribuição das relações issues fechadas/issues abertas')
      plt.xlabel('Razões issues fechada/issues abertas')
      plt.ylabel('Frequência')
      plt.show()
      # Gerando o gráfico boxplot:
      plt.boxplot(razoesInteiros)
      plt.title('Distribuição das relações issues fechadas/issues abertas')
      plt.xlabel("Razões issues fechada/issues abertas")
      plt.ylabel("Frequência")
      plt.show()
  else:
    print("Erro ao acessar API do GitHub")
    print("Código do erro:")
    print(resposta.status_code)
    print("Corpo do erro:")
    print(resposta.json())