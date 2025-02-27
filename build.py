import PyInstaller.__main__
import sys
import os

def build_exe():
    """Gera o executável do programa."""
    # Configurar o caminho do projeto
    project_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_path, 'src')
    
    # Definir argumentos do PyInstaller
    args = [
        'src/main.py',                    # Script principal
        '--name=AnimeProductivity',       # Nome do executável
        '--onefile',                      # Gerar um único arquivo
        '--noconsole',                    # Sem console
        '--clean',                        # Limpar cache
        f'--paths={src_path}',           # Adicionar src ao path
        '--add-data=src/config;config',   # Incluir configurações
        # Adicionar imports ocultos necessários
        '--hidden-import=plyer.platforms.win.notification',
        '--hidden-import=google.auth.transport.requests',
        '--hidden-import=google_auth_oauthlib.flow',
        '--hidden-import=googleapiclient.discovery',
        '--hidden-import=sqlalchemy.sql.default_comparator',  # SQLAlchemy
        '--hidden-import=bcrypt',  # Para hash de senha
        '--hidden-import=typing',
        '--hidden-import=collections.abc',
    ]
    
    # Executar PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Executável gerado com sucesso!")
    print("Localização: dist/AnimeProductivity.exe")

if __name__ == "__main__":
    build_exe() 