import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import User, AppConfig, PomodoroConfig
from src.database.database import get_session
from src.config.settings import AUTH
import re

class AuthService:
    def __init__(self):
        self.session: Session = get_session()

    def validate_password(self, password: str) -> tuple[bool, str]:
        """Valida a força da senha de acordo com os requisitos."""
        if len(password) < AUTH['MIN_PASSWORD_LENGTH']:
            return False, f"A senha deve ter pelo menos {AUTH['MIN_PASSWORD_LENGTH']} caracteres"
        
        if AUTH['REQUIRE_SPECIAL_CHARS']:
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                return False, "A senha deve conter pelo menos um caractere especial"
            
        if not re.search(r"[A-Z]", password):
            return False, "A senha deve conter pelo menos uma letra maiúscula"
            
        if not re.search(r"[0-9]", password):
            return False, "A senha deve conter pelo menos um número"
            
        return True, "Senha válida"

    def register(self, username: str, email: str, password: str) -> tuple[bool, str]:
        """Registra um novo usuário no sistema."""
        # Validação da senha
        is_valid, message = self.validate_password(password)
        if not is_valid:
            return False, message

        try:
            # Hash da senha
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Criar novo usuário
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash.decode('utf-8')
            )
            self.session.add(new_user)
            
            # Criar configurações padrão para o usuário
            app_config = AppConfig(user=new_user)
            pomodoro_config = PomodoroConfig(user=new_user)
            
            self.session.add(app_config)
            self.session.add(pomodoro_config)
            
            self.session.commit()
            return True, "Usuário registrado com sucesso"
            
        except IntegrityError:
            self.session.rollback()
            return False, "Username ou email já existe"
        except Exception as e:
            self.session.rollback()
            return False, f"Erro ao registrar usuário: {str(e)}"

    def login(self, username: str, password: str) -> tuple[bool, dict]:
        """Autentica um usuário no sistema."""
        try:
            user = self.session.query(User).filter(User.username == username).first()
            
            if not user:
                return False, {'message': "Usuário não encontrado"}
                
            if bcrypt.checkpw(password.encode('utf-8'), 
                            user.password_hash.encode('utf-8')):
                return True, {'message': "Login realizado com sucesso", 'user_id': user.id}
            else:
                return False, {'message': "Senha incorreta"}
                
        except Exception as e:
            return False, {'message': f"Erro ao realizar login: {str(e)}"}

    def __del__(self):
        """Fecha a sessão do banco de dados quando o serviço for destruído."""
        self.session.close() 