from src.database.models import User
from src.database.database import get_session
from src.services.session_manager import SessionManager

class AuthManager:
    def __init__(self):
        self.session_manager = SessionManager()
        
    def login(self, username: str, password: str):
        """Realiza o login do usuário."""
        user = User.authenticate(username, password)
        if user:
            self.session_manager.save_session(user.id)
            return user
        return None
        
    def logout(self):
        """Realiza o logout do usuário."""
        self.session_manager.clear_session()
        
    def check_session(self):
        """Verifica se existe uma sessão ativa."""
        return self.session_manager.get_active_session()
        
    def get_user(self, user_id: int):
        """Retorna o usuário pelo ID."""
        db_session = get_session()
        user = db_session.query(User).get(user_id)
        db_session.close()
        return user 