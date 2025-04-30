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
    rateLimit{{
    limit
    cost
    remaining
    resetAt
    }}
    repository(owner:"{autor}", name:"{nome}"){{
    pullRequests(states:CLOSED, first:20){{
    totalCount
    nodes{{
    number
    files(first:1){{
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
    tentativas = 20
    for tentativa in range(tentativas):
        try:
            resposta = requests.post(url, headers= header, json= {"query": body}, timeout=200)
            if resposta is not None:
                if resposta.status_code == 200:
                    if "data" in resposta.json():
                        return resposta
                    else:
                        print("Resposta 200 mas com erro")
                        time.sleep(15)
                        continue
                else:
                    print("Status code diferente de 200. Tentando de novo")
                    time.sleep(15)
                    continue
            else:
                print("Reposta vazia. Tentando de novo")
                time.sleep(15)
                continue
        except Exception as e:
            print(f"Tentativa {tentativa + 1} falhou com erro: {e}")
            time.sleep(15)
    raise Exception("Falha após múltiplas tentativas")

# Definindo requisição com paginação:
def buscandoDadosPRsComPaginacao(autor, nome, aPartirDe):
    url = "https://api.github.com/graphql"
    token = ""
    header = {"Authorization": f"Bearer {token}"}
    body = f"""query{{
    rateLimit{{
    limit
    cost
    remaining
    resetAt
    }}
    repository(owner:"{autor}", name:"{nome}"){{
    pullRequests(states:CLOSED, first:20, after:"{aPartirDe}"){{
    totalCount
    nodes{{
    number
    files(first:1){{
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
    tentativas = 20
    for tentativa in range(tentativas):
        try:
            resposta = requests.post(url, headers= header, json= {"query": body}, timeout=200)
            if resposta is not None:
                if resposta.status_code == 200:
                    if "data" in resposta.json():
                        return resposta
                    else:
                        print("Resposta 200 mas com erro")
                        time.sleep(15)
                        continue
                else:
                    print("Status code diferente de 200. Tentando de novo")
                    time.sleep(15)
                    continue
            else:
                print("Reposta vazia. Tentando de novo")
                time.sleep(15)
                continue
        except Exception as e:
            print(f"Tentativa {tentativa + 1} falhou com erro: {e}")
            time.sleep(15)
    raise Exception("Falha após múltiplas tentativas")

# Definindo colunas da planilha que será criada:
linhasDaPlanilha = [["Repositório", "N° da PR", "Qtd Arquivos", "Adições", "Deleções", "Tempo p/ Fechamento (h)", "Tamanho Descrição", "N° Participantes", "N° Comentários", "Aceita?"]]

# Percorrendo csv para buscar dados dos repositorios listados:
with open("Lab03/planilhas/lista_base_repositorios.csv", mode="r", encoding="utf-8", newline="") as arquivo:
    planilha = csv.reader(arquivo)
    next(planilha)
    qtdRepos = 0
    controlador_repositorio = 0
    totaRepos = 200
    repositoriosComProblema = []
    for linha in planilha:
        if qtdRepos > 200:
            break
        qtdRepos+=1
        controlador_repositorio+=1
        controlador_paginas = 0
        url = linha[3]
        autor = url.split("/")[3]
        nome = url.split("/")[4]
        percorrePaginas = True
        try:
            time.sleep(1)
            resposta = buscandoDadosPRs(autor, nome)
        except Exception as e:
            print("Erro ao buscar primeira página do repositorio. Passando para o proximo repositorio")
            if resposta is not None:
                print("Status code:", resposta.status_code)
                print("Texto da resposta:", resposta.text)
            resposta = None
            repositoriosComProblema.append(nome)
            qtdRepos-=1
            totaRepos+=1
            continue
        while percorrePaginas:
            if resposta is not None and resposta.status_code == 200:
                controlador_paginas+=1
                totalPaginas = math.ceil((resposta.json()["data"]["repository"]["pullRequests"]["totalCount"])/20)
                listaPRs = resposta.json()["data"]["repository"]["pullRequests"]["nodes"]
                print(f"\n\nRepositório {controlador_repositorio}/{totaRepos}.  Página {controlador_paginas}/{totalPaginas}")
                print(f"Cost: {resposta.json()["data"]["rateLimit"]["cost"]}/{resposta.json()["data"]["rateLimit"]["limit"]}\nRemaining: {resposta.json()["data"]["rateLimit"]["remaining"]}\nReset at: {resposta.json()["data"]["rateLimit"]["resetAt"]}")
                for pr in listaPRs:
                    agora = datetime.now()
                    criacao = datetime.strptime(pr["createdAt"] , f"%Y-%m-%dT%H:%M:%SZ")
                    fechamento = datetime.strptime(pr["closedAt"] , f"%Y-%m-%dT%H:%M:%SZ")
                    duracao = ((fechamento - criacao).total_seconds())/3600
                    aceito = "Sim" if pr["merged"] == True else "Não"
                    if pr["files"] is not None:
                        qtdArquivos = pr["files"]["totalCount"]
                    else:
                        qtdArquivos = "sem dados"
                    linhasDaPlanilha.append([nome, pr["number"], qtdArquivos, pr["additions"], pr["deletions"], duracao, len(pr["body"]), pr["participants"]["totalCount"], pr["comments"]["totalCount"], aceito])
                if resposta.json()["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
                    cursorFinal = resposta.json()["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
                    time.sleep(1)
                    try:
                        resposta = buscandoDadosPRsComPaginacao(autor, nome, cursorFinal)
                    except Exception as e:
                        print("Erro ao buscar pagina. Passando para o proximo repositorio")
                        if resposta is not None:
                            print("Status code:", resposta.status_code)
                            print("Texto da resposta:", resposta.text)
                        resposta = None
                        repositoriosComProblema.append(nome)
                        qtdRepos-=1
                        totaRepos+=1
                        percorrePaginas = False
                else:
                    percorrePaginas = False   
            else:
                print("Primeira pagina do repositório retornou status code diferente de 200. Passando para o proximo repositorio")
                if resposta is not None:
                    print("Status code:", resposta.status_code)
                    print("Texto da resposta:", resposta.text)
                repositoriosComProblema.append(nome)
                qtdRepos-=1
                totaRepos+=1
                break  
    with open("Lab03/planilhas/dados_pull_requests_fechadas.csv", mode="w", encoding="utf-8", newline="") as arquivo2:
        csv.writer(arquivo2).writerows(linhasDaPlanilha)

    print(f"Repositorios com problema: {repositoriosComProblema}")