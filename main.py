import sys
from PySide6.QtWidgets import QApplication
from src.gui.login import LoginWindow
from src.database.database import init_db

def main():
    """Função principal do programa."""
    # Inicializar banco de dados
    init_db()
    
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    
    # Configurar estilo global
    app.setStyle('Fusion')
    
    # Criar e mostrar janela de login
    login = LoginWindow()
    login.show()
    
    # Executar aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 