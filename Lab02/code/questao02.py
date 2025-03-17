import subprocess, os, shutil
from pathlib import Path
import csv, statistics

url_repositorio = "https://github.com/google/guava.git"

# Comando para clonar repositório:
# resultado_clonagem = subprocess.run(["git", "clone", url_repositorio], check=True, text=True, cwd="diretorio_repositorio")

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
print(caminho_absoluto_resultados)

# Comando CK:
comando_ck = ["java",  "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", caminho_absoluto_repositorio, "use_jars:true", "0", "variables_and_fields_metrics:true", caminho_absoluto_resultados]

# Executando o comando ck na pasta do repositorio clonado:
resultado_ck = subprocess.run(comando_ck, cwd="ck/target")

# Pegando as métricas:
cbos = []
dits = []
lcoms = []
with open("diretorio_resultados/metricas_extraidas_class.csv", mode="r", newline="", encoding="utf-8") as arquivo:
    planilha = csv.reader(arquivo)
    next(planilha)
    for linha in planilha:
        cbos.append(int(linha[3]))
        dits.append(int(linha[8]))
        lcoms.append(int(linha[11]))

# obtenos os valores de medida central:
mediaCbos = statistics.mean(cbos)
medianaCbos = statistics.median(cbos)
desvioPadraoCbos = statistics.stdev(cbos)

mediaDits = statistics.mean(dits)
medianaDits = statistics.median(dits)
desvioPadraoDits = statistics.stdev(dits)

mediaLcoms = statistics.mean(lcoms)
medianaLcoms = statistics.median(lcoms)
desvioPadraoLcoms = statistics.stdev(lcoms)

# Colocando métricas no mapa:

# Apagando arquivos gerados (arquivos de resultados da ferramenta ck e diretorio do repositorio clonado):
os.remove(Path("diretorio_resultados/metricas_extraidas_class.csv").resolve())
os.remove(Path("diretorio_resultados/metricas_extraidas_method.csv").resolve())
subprocess.run(["rm", "-rf", ".git"], cwd=caminho_absoluto_repositorio)
shutil.rmtree(caminho_absoluto_repositorio)