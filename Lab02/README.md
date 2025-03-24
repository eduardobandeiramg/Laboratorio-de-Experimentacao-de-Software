# Atenção:
## Instruções para execução do código

1. Execute no terminal o comando:

`cd Lab02/code`

(O código deve ser executado dentro da pasta "code" para que funcione corretamente!)

2. Adicione às duas variáveis "token" do código o seu token de autenticação do GitHub. Veja [aqui](https://docs.github.com/pt/enterprise-cloud@latest/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#como-criar-um-personal-access-token-classic) como criar um.

3. Execute o código

Ao executar o código: as seguintes etapas serão executadas:

- A API do GitHub será consumida e será gerado um arquivo CSV com as informações necessárias de cada repositório.
- Cada repositório será, então, clonado, e serão obtidas as métricas para ele a partir da execução da ferramenta [CK](https://github.com/mauricioaniche/ck) dentro de cada repositório.
- Será criada a matriz de correlação para todas as variáveis (e exportada para csv) dentro da pasta "diretorio_resultados".
- Será gerado o gráfico de calor para todas as variáveis analisadas.


## Questões de Pesquisa:
* RQ 01: Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
* RQ 02: Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
* RQ 03: Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
* RQ 04: Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

## Métricas Consideradas:
* Popularidade: quantidade de estrelas
* Maturidade: idade em anos
* Atividade: número de releases
* Tamanho: quantidade total de linhas (código + comentários)
* Qualidade: CBO (Coupling Between Objects), DIT (Depth of Inheritance Tree) e LCOM (Lack of Cohesion Between Methods)