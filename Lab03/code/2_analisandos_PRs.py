import requests
import csv
from datetime import datetime
import math
import time

# Definindo requisição para buscar dados das Pull Requests de cada repositório:
def buscandoDadosPRs(autor, nome):
    token = ""
    url = "https://api.github.com/graphql"
    header = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = f"""query{{
    repository(owner:"{autor}", name:"{nome}"){{
    pullRequests(states:CLOSED, first:20){{
    totalCount
    nodes{{
    id
    files{{
    totalCount
    }}
    additions
    deletions
    createdAt
    closedAt
    body
    participants{{
    totalCount
    }}
    comments{{
    totalCount
    }}
    merged
    }}
    pageInfo{{
    hasNextPage
    endCursor
    }}
    }}
    }}
    }}"""
    return requests.post(url, headers= header, json= {"query": body})

# Definindo requisição com paginação:
def buscandoDadosPRsComPaginacao(autor, nome, aPartirDe):
    url = "https://api.github.com/graphql"
    token = ""
    header = {"Authorization": f"Bearer {token}"}
    body = f"""query{{repository(owner:"{autor}", name:"{nome}"){{
    pullRequests(states:CLOSED, first:20, after:"{aPartirDe}"){{
    totalCount
    nodes{{
    id
    files{{
    totalCount
    }}
    additions
    deletions
    createdAt
    closedAt
    body
    participants{{
    totalCount
    }}
    comments{{
    totalCount
    }}
    merged
    }}
    pageInfo{{
    hasNextPage
    endCursor
    }}
    }}
    }}
    }}"""
    return requests.post(url, headers= header, json= {"query": body})

# Definindo colunas da planilha que será criada:
linhasDaPlanilha = [["Repositório", "ID da PR", "Qtd Arquivos", "Linhas Adicionadas", "Linhas Removidas", "Duração do PR (dias)", "Tamanho Descrição", "Qtd Participantes", "Qtd Comentários", "Aceito?"]]

# Percorrendo csv para buscar dados dos repositorios listados:
with open("Lab03/planilhas/lista_base_repositorios.csv", mode="r", encoding="utf-8", newline="") as arquivo:
    planilha = csv.reader(arquivo)
    next(planilha)
    controlador_repositorio = 0
    for linha in planilha:
        controlador_repositorio+=1
        url = linha[3]
        autor = url.split("/")[3]
        nome = url.split("/")[4]
        time.sleep(1)
        resposta = buscandoDadosPRs(autor, nome)
        percorrePaginas = True
        if resposta.status_code == 200:
            controlador_paginas = 1
            totalPaginas = (resposta.json()["data"]["repository"]["pullRequests"]["totalCount"])/20
            totalPaginas = math.ceil(totalPaginas)
            while percorrePaginas:
                print(f"\n\nRepositório {controlador_repositorio}/200.  Página {controlador_paginas}/{totalPaginas}")
                controlador_paginas+=1
                for pr in resposta.json()["data"]["repository"]["pullRequests"]["nodes"]:
                    dataCriacao = datetime.strptime(pr["createdAt"] , f"%Y-%m-%dT%H:%M:%SZ")
                    dataFechamento = datetime.strptime(pr["closedAt"] , f"%Y-%m-%dT%H:%M:%SZ")
                    duracao = (dataFechamento - dataCriacao).days
                    linhasDaPlanilha.append([nome, pr["id"], pr["files"]["totalCount"], pr["additions"], pr["deletions"], duracao, len(pr["body"]), pr["participants"]["totalCount"], pr["comments"]["totalCount"], "Sim" if pr["merged"] else "Não"])
                if resposta.json()["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
                    cursorFinal = resposta.json()["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
                    time.sleep(1)
                    resposta = buscandoDadosPRsComPaginacao(autor, nome, cursorFinal)
                else:
                    percorrePaginas = False
        else:
            print("Erro ao fazer requisição à API do GitHub!")
    with open("Lab03/planilhas/dados_sobre_pull_requests.csv", mode="w", encoding="utf-8", newline="") as arquivo2:
        csv.writer(arquivo2).writerows(linhasDaPlanilha)