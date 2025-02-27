import PyInstaller.__main__
import os
import shutil

def build_exe():
    """Gera o executável do programa."""
    # Limpar diretório dist se existir
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Configurar ícone
    icon_path = os.path.join("assets", "icons", "app.ico")
    
    # Definir argumentos do PyInstaller
    args = [
        'src/main.py',                    # Script principal
        '--name=AnimeProductivity',       # Nome do executável
        '--onefile',                      # Gerar um único arquivo
        '--noconsole',                    # Sem console
        '--add-data=assets;assets',       # Incluir pasta assets
        f'--icon={icon_path}',           # Ícone do executável
        '--clean',                        # Limpar cache
        # Adicionar imports ocultos
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=google.auth.transport.requests',
        '--hidden-import=google_auth_oauthlib.flow',
        '--hidden-import=googleapiclient.discovery',
    ]
    
    # Executar PyInstaller
    PyInstaller.__main__.run(args)
    
    # Copiar arquivos necessários
    shutil.copytree("assets", os.path.join("dist", "assets"))
    
    print("Executável gerado com sucesso!")
    print("Localização: dist/AnimeProductivity.exe")

if __name__ == "__main__":
    build_exe() 