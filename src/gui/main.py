import sys
from PySide6.QtWidgets import QApplication
from login import LoginWindow  # Certifique-se de que o caminho está correto

def main():
    app = QApplication(sys.argv)
    
    # Instancie LoginWindow sem argumentos
    login_window = LoginWindow()  # Não passe nenhum argumento
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 