import sys
from PySide6.QtWidgets import QApplication
from src.gui.login import LoginWindow
from src.gui.main_window import MainWindow
from src.database.database import init_db, get_data_dir
from src.services.session_manager import SessionManager
import os
from datetime import datetime
from src.database.migrate import migrate_database

def main():
    try:
        # Garantir que o diretório de dados existe
        data_dir = get_data_dir()
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar banco de dados e realizar migrações
        init_db()
        migrate_database()
        
        # Iniciar aplicação
        app = QApplication(sys.argv)
        
        # Verificar sessão existente
        session_manager = SessionManager()
        user_id = session_manager.get_active_session()
        
        if user_id:
            # Se existe sessão válida, abrir direto a janela principal
            window = MainWindow(user_id)
            window.show()
        else:
            # Se não existe sessão, mostrar login
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