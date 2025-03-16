import subprocess
from pathlib import Path

caminho_ck = "/ck"
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
caminho_absoluto = Path(caminho_repositorio).resolve()

# Comando CK:
comando_ck = ["java",  "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", caminho_absoluto, "use_jars:true", "0", "variables_and_fields_metrics:true", "diretorio_resultado"]

# Executando o comando ck na pasta do repositorio clonado:
resultado_ck = subprocess.run(comando_ck, cwd="ck/target")
