# Etapas realizadas pelo código:

1. Arquivo "1_buscando_repos.py": primeiro, são buscados os 200 repositórios mais populares do GitHub (mais estrelados) que tenham pelo menos 100 Pull Requests mergeadas. O resultado será um arquivo csv nomeado "lista_base_repositorios.csv", exportado para dentro da sub-pasta "planilhas".
2. Arquivos "2_1_analisando_PRs.py", "2_2_analisando_PRs.py" e "2_3_analisando_PRs.py": o código contido nestes arquivos percorrem a planilha gerada pelo código anterior e, para cada repositório da lista, buscam todos os Pull Requests e os dados analisados para cada PR, gerando planilhas parciais. Essa quebra foi necessária devido à limitação da quantidade de dados entregues pela API do GitHub.
3. Ao final, as planilhas são juntadas em uma só ("dados_sobre_repositorios_final.csv") e são feitas análises sobre as métricas contidas nesta planilha (cálculos de correlação e geração de gráficos).


# Instruções para execução do código:

1. Adicione o token do GitHub em todas as variáveis com esse nome ("token"), em cada arquivo de código. Veja [aqui](https://docs.github.com/pt/enterprise-cloud@latest/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#como-criar-um-personal-access-token-classic) como criar um. Localização das variáveis:
    * Arquivo 1: linhas 7 e 33
    * Arquivo 2: linhas 9 e 52
2. Execute cada código na pasta raiz do projeto. Isso é fundamental devido aos caminhos dos arquivos definidos no código.