import time
from datetime import datetime
from src.database.models import PomodoroSession, PomodoroConfig, User
from src.database.database import get_session
from plyer import notification

class PomodoroTimer:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = get_session()
        self.config = self._get_or_create_config()
        self.current_session = None
        self.is_running = False
        self.time_left = self.config.work_time * 60  # Converter para segundos
        
    def _get_or_create_config(self) -> PomodoroConfig:
        """Obtém ou cria uma configuração do Pomodoro para o usuário."""
        config = self.session.query(PomodoroConfig).filter_by(user_id=self.user_id).first()
        
        if not config:
            config = PomodoroConfig(user_id=self.user_id)
            self.session.add(config)
            self.session.commit()
            
        return config
        
    def start(self):
        """Inicia uma nova sessão Pomodoro."""
        if not self.is_running:
            self.current_session = PomodoroSession(
                user_id=self.user_id,
                start_time=datetime.now(),
                duration=self.config.work_time
            )
            self.session.add(self.current_session)
            self.session.commit()
            
            self.is_running = True
            self.time_left = self.config.work_time * 60
            
    def pause(self):
        """Pausa o timer atual."""
        if self.is_running:
            self.is_running = False
            
    def resume(self):
        """Retoma o timer pausado."""
        if not self.is_running:
            self.is_running = True
            
    def stop(self):
        """Para o timer atual."""
        if self.current_session:
            self.current_session.end_time = datetime.now()
            self.current_session.completed = False
            self.session.commit()
            
        self.is_running = False
        self.current_session = None
        self.time_left = self.config.work_time * 60
        
    def reset(self):
        """Reinicia o timer."""
        self.stop()
        self.time_left = self.config.work_time * 60
        
    def update(self):
        """Atualiza o timer."""
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            
            if self.time_left <= 0:
                self._complete_session()
                
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
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes:02d}:{seconds:02d}"
        
    def get_progress(self) -> float:
        """Retorna o progresso atual (0.0 a 1.0)."""
        total_time = self.config.work_time * 60
        return 1 - (self.time_left / total_time)
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 