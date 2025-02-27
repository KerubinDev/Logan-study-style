import time
from datetime import datetime
from src.database.models import PomodoroSession, PomodoroConfig, User
from src.database.database import get_session
from plyer import notification

class PomodoroTimer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.time_remaining = 25 * 60  # 25 minutos em segundos
        self.is_running = False
        self.total_time = 25 * 60
        
    def start(self):
        """Inicia o timer."""
        self.is_running = True
        
    def pause(self):
        """Pausa o timer."""
        self.is_running = False
        
    def reset(self):
        """Reseta o timer."""
        self.time_remaining = self.total_time
        self.is_running = False
        
    def get_remaining_time(self):
        """Retorna o tempo restante em segundos."""
        return self.time_remaining
        
    def update(self):
        """Atualiza o timer."""
        if self.is_running and self.time_remaining > 0:
            self.time_remaining -= 1
            return True
        return False
        
    def _get_or_create_config(self) -> PomodoroConfig:
        """Obtém ou cria uma configuração do Pomodoro para o usuário."""
        config = self.session.query(PomodoroConfig).filter_by(user_id=self.user_id).first()
        
        if not config:
            config = PomodoroConfig(user_id=self.user_id)
            self.session.add(config)
            self.session.commit()
            
        return config
        
    def resume(self):
        """Retoma o timer pausado."""
        if not self.is_running:
            self.is_running = True
            
    def stop(self):
        """Para o timer atual."""
        self.is_running = False
        
    def _complete_session(self):
        """Completa uma sessão Pomodoro."""
        if self.current_session:
            self.current_session.end_time = datetime.now()
            self.current_session.completed = True
            self.session.commit()
            
            # Notificar usuário
            notification.notify(
                title='Pomodoro Completo!',
                message='Hora de uma pausa! ☕',
                timeout=10
            )
            
        self.is_running = False
        self.current_session = None
        
    def get_time_str(self) -> str:
        """Retorna o tempo restante formatado."""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"
        
    def get_progress(self) -> float:
        """Retorna o progresso atual (0.0 a 1.0)."""
        total_time = self.total_time
        return 1 - (self.time_remaining / total_time) 