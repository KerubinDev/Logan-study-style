import PyInstaller.__main__
import sys
import os
from PIL import Image

def build_exe():
    """Gera o executável do programa."""
    # Configurar o caminho do projeto
    project_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_path, 'src')
    
    # Converter PNG para ICO
    icon_path = os.path.join(src_path, 'img', 'logo.png')
    ico_path = os.path.join(project_path, 'app.ico')
    
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        # Salvar como ICO com vários tamanhos
        img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128)])
    
    # Definir argumentos do PyInstaller
    args = [
        'src/main.py',                    # Script principal
        '--name=AnimeProductivity',       # Nome do executável
        '--onefile',                      # Gerar um único arquivo
        '--noconsole',                    # Sem console
        '--clean',                        # Limpar cache
        f'--icon={ico_path}',            # Ícone do executável
        f'--paths={src_path}',           # Adicionar src ao path
        '--add-data=src/config;config',   # Incluir configurações
        '--add-data=src/img;img',        # Incluir pasta de imagens
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