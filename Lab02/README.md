# Atenção:
## Instruções para execução do código
O código deve ser executado dentro da pasta "code" para que funcione corretamente!

Para isso, execute no terminal:

`cd Lab02/code`

Então, antes de tudo, execute o código contido no arquivo questao00.py

Isso é necessário para que, primeiramente, a API do GitHub seja consumida e seja gerado um arquivo CSV com as informações necessárias de cada repositório. Depois disso, cada repositório será, então, clonado, e serão obtidas as métricas para ele a partir da execução da ferramenta [CK](https://github.com/mauricioaniche/ck) dentro de cada repositório.

Então, execute cada arquivo ("questao01.py", "questao02.py", "questao03.py", "questao04.py") para obter as respostas para cada questão de pesquisa. 

## Questões de Pesquisa:
* RQ 01: Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
* RQ 02: Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
* RQ 03: Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
* RQ 04: Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

# Métricas Consideradas:
* Popularidade: quantidade de estrelas
* Maturidade: idade em anos
* Atividade: número de releases
* Tamanho: quantidade total de linhas (código + comentários)
* Qualidade: CBO (Coupling Between Objects), DIT (Depth of Inheritance Tree) e LCOM (Lack of Cohesion Between Methods)