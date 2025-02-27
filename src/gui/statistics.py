from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QFrame, QScrollArea, QPushButton)
from PySide6.QtCore import Qt
from src.database.models import PomodoroSession, Task
from src.database.database import get_session
from datetime import datetime, timedelta

class StatisticsWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_id = parent.user_id
        self.session = get_session()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Estatísticas")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QFrame()
        header_layout = QHBoxLayout(header)
        title = QLabel("Estatísticas de Produtividade")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        header_layout.addWidget(title)
        layout.addWidget(header)
        
        # Estatísticas Gerais
        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)
        
        # Pomodoros completados hoje
        today = datetime.now().date()
        pomodoros_today = self.session.query(PomodoroSession).filter(
            PomodoroSession.user_id == self.user_id,
            PomodoroSession.start_time >= today,
            PomodoroSession.completed == True
        ).count()
        
        pomodoro_label = QLabel(f"Pomodoros Completados Hoje: {pomodoros_today}")
        pomodoro_label.setStyleSheet("font-size: 16pt;")
        stats_layout.addWidget(pomodoro_label)
        
        # Tarefas completadas hoje
        tasks_today = self.session.query(Task).filter(
            Task.user_id == self.user_id,
            Task.completed == True,
            Task.completion_date >= today
        ).count()
        
        tasks_label = QLabel(f"Tarefas Completadas Hoje: {tasks_today}")
        tasks_label.setStyleSheet("font-size: 16pt;")
        stats_layout.addWidget(tasks_label)
        
        # Tempo total focado
        total_time = self.session.query(PomodoroSession).filter(
            PomodoroSession.user_id == self.user_id,
            PomodoroSession.completed == True
        ).count() * 25  # 25 minutos por pomodoro
        
        hours = total_time // 60
        minutes = total_time % 60
        time_label = QLabel(f"Tempo Total Focado: {hours}h {minutes}m")
        time_label.setStyleSheet("font-size: 16pt;")
        stats_layout.addWidget(time_label)
        
        layout.addWidget(stats_frame)
        
        # Aqui você pode adicionar mais widgets para mostrar as estatísticas
        # Por exemplo: gráficos, números, etc. 