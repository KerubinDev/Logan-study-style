import sys
from PySide6.QtWidgets import QApplication
from src.gui.login import LoginWindow
from src.database.database import init_db

def main():
    # Inicializar banco de dados
    init_db()
    
    # Iniciar aplicação
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 