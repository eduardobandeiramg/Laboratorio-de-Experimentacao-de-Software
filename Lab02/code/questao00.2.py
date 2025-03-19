# Arquivo temporário para extração das métricas de qualidade
# TODO: NAO DEPENDER DE CONSEGUIR APAGAR REPO OU RESULTADOS
# TODO: JUNTAR COM O CÓDIGO DO ARQUIVO 00.1
import subprocess, os, shutil
from pathlib import Path
import csv, statistics

# Percorrendo o CSV com dados dos repositórios para obter métricas:
linhasDaPlanilha = [["Repositório", "Linguagem Principal", "Url", "Estrelas", "Idade em anos", "Número de releases", "Total de linhas", "Média de CBO's", "Mediana de CBO's", "Desvio Padrão de CBO's", "Média de DIT's", "Mediana de DIT's", "Desvio Padrão de DIT's", "Média de LCOM's", "Mediana de LCOM's", "Desvio Padrão de LCOM's"]]

with open("questao01.csv", mode="r", encoding="utf-8", newline="") as arquivoRepos:
    planilhaRepos = csv.reader(arquivoRepos)
    next(planilhaRepos)
    variavelControle = 0
    for linha in planilhaRepos:
        variavelControle+=1
        erroAoClonar = False
        print(f"Trabalhando sobre o repositório numero {variavelControle}")
        novaLinha = []
        novaLinha.extend([linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6]])
        url_repositorio = linha[2]
        # Comando para clonar repositório:
        try:
            resultado_clonagem = subprocess.run(["git", "clone", url_repositorio], check=True, text=True, cwd="diretorio_repositorio")
            print(f"resultado da clonagem: {resultado_clonagem.returncode}")
            print(f"resultado da clonagem: {resultado_clonagem.stdout}")
            # Obtendo caminho do repositório clonado
            caminho_diretorio_repositorio = Path("diretorio_repositorio")
            subdirs = [d for d in caminho_diretorio_repositorio.iterdir() if d.is_dir()]
            if len(subdirs) == 1:
                caminho_repositorio = subdirs[0]
            else:
                print("Erro: mais de uma ou nenhuma pasta encontrada.")
            # Obtendo o caminho absoluto da pasta do repositorio:
            caminho_absoluto_repositorio = Path(caminho_repositorio).resolve()
            # Obtendo o caminho absoluto da pasta de resultados:
            caminho_absoluto_resultados = Path("diretorio_resultados/metricas_extraidas_").resolve()
            # Comando CK:
            comando_ck = ["java",  "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", caminho_absoluto_repositorio, "use_jars:true", "0", "variables_and_fields_metrics:true", caminho_absoluto_resultados]
            # Executando o comando ck na pasta do repositorio clonado:
            resultado_ck = subprocess.run(comando_ck, cwd="CK/target")
            # Pegando as métricas:
            cbos = []
            dits = []
            lcoms = []
            linhasDeCodigo = []
            with open("diretorio_resultados/metricas_extraidas_class.csv", mode="r", newline="", encoding="utf-8") as arquivoMetricas:
                planilhaMetricas = csv.reader(arquivoMetricas)
                next(planilhaMetricas)
                for linha in planilhaMetricas:
                    cbos.append(int(linha[3]))
                    dits.append(int(linha[8]))
                    lcoms.append(int(linha[11]))
                    linhasDeCodigo.append(int(linha[33]))
            # Obtendo quantidade total de linhas:
            if len(linhasDeCodigo) != 0:
                linhasDeCodigo = sum(linhasDeCodigo)
            else:
                linhasDeCodigo = "Sem dados"
            # Obtendo os valores de medida central:
            # Dos CBO's
            if len(cbos) == 0:
                mediaCbos = "Sem dados"
                medianaCbos = "Sem dados"
                desvioPadraoCbos = "Sem dados"
            else:            
                mediaCbos = statistics.mean(cbos)
                medianaCbos = statistics.median(cbos)
                desvioPadraoCbos = statistics.stdev(cbos)
            # Das DIT's:
            if len(dits) == 0:
                mediaDits = "Sem dados"
                medianaDits = "Sem dados"
                desvioPadraoDits = "Sem dados"
            else:
                mediaDits = statistics.mean(dits)
                medianaDits = statistics.median(dits)
                desvioPadraoDits = statistics.stdev(dits)
            # Dos LCOM's:
            if len(lcoms) == 0:
                mediaLcoms = "Sem dados"
                medianaLcoms = "Sem dados"
                desvioPadraoLcoms = "Sem dados"
            else:
                mediaLcoms = statistics.mean(lcoms)
                medianaLcoms = statistics.median(lcoms)
                desvioPadraoLcoms = statistics.stdev(lcoms)

            # Adicionando métricas na linha da planilha final:
            novaLinha[6] = linhasDeCodigo
            novaLinha.extend([mediaCbos, medianaCbos, desvioPadraoCbos, mediaDits, medianaDits, desvioPadraoDits, mediaLcoms, medianaLcoms, desvioPadraoLcoms])
            linhasDaPlanilha.append(novaLinha)

            # Apagando arquivos gerados (arquivos de resultados da ferramenta ck e diretorio do repositorio clonado):
            os.remove(Path("diretorio_resultados/metricas_extraidas_class.csv").resolve())
            os.remove(Path("diretorio_resultados/metricas_extraidas_method.csv").resolve())
            subprocess.run(["rm", "-rf", ".git"], cwd=caminho_absoluto_repositorio)
            shutil.rmtree(caminho_absoluto_repositorio)
        except Exception as e:
            erroAoClonar = True
            # Adicionando mensagem de erro de clonagem nos campos da linha do repositório:
            novaLinha[6] = "Erro ao clonar repositório"
            novaLinha.extend(["Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório", "Erro ao clonar repositório"])
            linhasDaPlanilha.append(novaLinha)

# Criando CSV com todas as métricas para cada repositório:
with open("diretorio_resultados/resultados_finais.csv", mode="w", encoding="utf-8", newline="") as arquivoFinal:
    csv.writer(arquivoFinal).writerows(linhasDaPlanilha)

# Apagando planilha inicial:
# os.remove(Path("questao01.csv").resolve())
