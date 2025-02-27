import json
import os
from datetime import datetime, timedelta
from src.database.models import User
from src.database.database import get_session

class SessionManager:
    def __init__(self):
        self.session_file = os.path.join('data', 'session.json')
        os.makedirs('data', exist_ok=True)
        
    def save_session(self, user_id: int):
        """Salva uma nova sessão."""
        session_data = {
            'user_id': user_id,
            'last_login': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=2)).isoformat()
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)
            
    def get_active_session(self):
        """Retorna a sessão ativa se existir e for válida."""
        try:
            if not os.path.exists(self.session_file):
                return None
                
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
                
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            
            # Verificar se a sessão expirou
            if datetime.now() > expires_at:
                self.clear_session()
                return None
                
            # Verificar se o usuário ainda existe
            db_session = get_session()
            user = db_session.query(User).get(session_data['user_id'])
            db_session.close()
            
            if not user:
                self.clear_session()
                return None
                
            return session_data['user_id']
            
        except Exception as e:
            print(f"Erro ao ler sessão: {e}")
            return None
            
    def clear_session(self):
        """Remove a sessão atual."""
        if os.path.exists(self.session_file):
            os.remove(self.session_file) 