import json
import os
from datetime import datetime, timedelta
from src.database.models import User
from src.database.database import get_session, get_data_dir
import logging

class SessionManager:
    def __init__(self):
        self.data_dir = get_data_dir()
        self.session_file = os.path.join(self.data_dir, 'session.json')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Configurar logging
        logging.basicConfig(
            filename=os.path.join(self.data_dir, 'session.log'),
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s'
        )
        
    def save_session(self, user_id: int):
        """Salva uma nova sessão."""
        try:
            session_data = {
                'user_id': user_id,
                'last_login': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
                
            logging.debug(f"Sessão salva para usuário {user_id}")
            return True
        except Exception as e:
            logging.error(f"Erro ao salvar sessão: {e}")
            return False
            
    def get_active_session(self):
        """Retorna a sessão ativa se existir e for válida."""
        try:
            if not os.path.exists(self.session_file):
                logging.debug("Arquivo de sessão não encontrado")
                return None
                
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
                
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            
            # Verificar se a sessão expirou
            if datetime.now() > expires_at:
                logging.debug("Sessão expirada")
                self.clear_session()
                return None
                
            # Verificar se o usuário ainda existe
            db_session = get_session()
            user = db_session.query(User).get(session_data['user_id'])
            db_session.close()
            
            if not user:
                logging.debug("Usuário não encontrado")
                self.clear_session()
                return None
                
            # Atualizar data de expiração
            self.save_session(session_data['user_id'])
            logging.debug(f"Sessão válida encontrada para usuário {session_data['user_id']}")
            
            return session_data['user_id']
            
        except Exception as e:
            logging.error(f"Erro ao ler sessão: {e}")
            return None
            
    def clear_session(self):
        """Remove a sessão atual."""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                logging.debug("Sessão removida")
        except Exception as e:
            logging.error(f"Erro ao remover sessão: {e}") 