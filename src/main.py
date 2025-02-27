import sys
from PySide6.QtWidgets import QApplication
from src.gui.login import LoginWindow
from src.database.database import init_db, get_data_dir
import os
from datetime import datetime

def main():
    try:
        # Garantir que o diretório de dados existe
        data_dir = get_data_dir()
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar banco de dados
        init_db()
        
        # Iniciar aplicação
        app = QApplication(sys.argv)
        login = LoginWindow()
        login.show()
        sys.exit(app.exec())
        
    except Exception as e:
        # Mostrar erro em um arquivo de log
        log_file = os.path.join(get_data_dir(), 'error.log')
        with open(log_file, 'a') as f:
            f.write(f"\n[{datetime.now()}] Error: {str(e)}")
        raise e

if __name__ == "__main__":
    main() 