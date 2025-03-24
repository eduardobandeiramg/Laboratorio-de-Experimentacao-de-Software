# Laboratório de Experimentação de Software
## Engenharia de Software - PUC-MG - 1º Semestre de 2025
### Aluno: Eduardo Bandeira de Melo Guimarães (Matrícula 741607)

Este repositório tem como objetivo armazenar as atividades desenvolvidas na disciplina de "Laboratório de Experimentação de Software". 
Esta se baseia no consumo da [API do GitHub usando GraphQL](https://docs.github.com/en/graphql), com Python, para a obtenção de dados referentes a repositórios.
A disciplina é dividida em 5 trabalhos entitulados "labs", a serem realizados ao longo do semestre letivo. Cada um deles é dividido em 2 ou 3 sprints, sendo as sprints semanais.

No LAB 01, são buscados dados sobre os 1000 repositórios mais populares do GitHub, tais quais: idade, contribuições externas, releases, atualizações, linguagem e fechamento de issues.
Os scripts são escritos de forma que as informações desejadas são recuperadas da API, os cálculos devidos são realizados e os resultados são exportados para planilhas e gráficos, de forma a obter informações sobre os aspectos citados para os 1000 repositórios mais populares do GitHub.

No LAB 02, busca-se entender a relação entre alguns atributos de repositórios Java (popularidade/idade/atividade/tamanho) e a qualidade destes. Para isso, faz-se o consumo da API obtendo os dados citados. Então, de posse da url de cada repositório, extrai-se métricas de qualidade usando a ferramente de análise estática [ck](https://github.com/mauricioaniche/ck). Finalmente, é feita uma análise estatística de correlação entre os atributos citados e algumas métricas de qualidade extraídas (CBO, DIT e LCOM).

No LAB 03, ...