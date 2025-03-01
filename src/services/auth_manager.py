from src.database.models import User
from src.database.database import get_session
from src.services.session_manager import SessionManager
import logging

class AuthManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.db_session = get_session()
        self.logger = logging.getLogger('auth_manager')
        
    def login(self, username: str, password: str):
        """Realiza o login do usuário."""
        try:
            self.logger.debug(f"Tentativa de login para usuário: {username}")
            
            user = self.db_session.query(User).filter_by(username=username).first()
            if not user:
                self.logger.debug(f"Usuário não encontrado: {username}")
                return None
                
            if user.verify_password(password):
                self.logger.debug(f"Login bem sucedido para usuário: {username}")
                self.session_manager.save_session(user.id)
                return user
            else:
                self.logger.debug(f"Senha incorreta para usuário: {username}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erro no login: {e}")
            return None
        
    def logout(self):
        """Realiza o logout do usuário."""
        self.session_manager.clear_session()
        
    def check_session(self):
        """Verifica se existe uma sessão ativa."""
        return self.session_manager.get_active_session()
        
    def get_user(self, user_id: int):
        """Retorna o usuário pelo ID."""
        return self.db_session.query(User).get(user_id)
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.db_session.close() 