from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QCalendarWidget, QFrame)
from PySide6.QtCore import Qt, QDate
from src.database.models import Task
from src.database.database import get_session
from datetime import datetime
from src.services.task_manager import TaskManager

class CalendarWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_id = parent.user_id
        self.session = get_session()
        self.task_manager = TaskManager(self.user_id)
        self.setup_ui()
        self.load_tasks()
        
    def setup_ui(self):
        """Configura a interface do calendário."""
        self.setWindowTitle("Calendário de Tarefas")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Header
        header = QFrame()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Calendário de Tarefas")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        header_layout.addWidget(title)
        
        layout.addWidget(header)
        
        # Área do calendário
        calendar_frame = QFrame()
        calendar_layout = QHBoxLayout(calendar_frame)
        
        # Calendário
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.show_tasks_for_date)
        calendar_layout.addWidget(self.calendar)
        
        # Lista de tarefas do dia
        self.tasks_frame = QFrame()
        self.tasks_layout = QVBoxLayout(self.tasks_frame)
        
        tasks_title = QLabel("Tarefas do Dia")
        tasks_title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.tasks_layout.addWidget(tasks_title)
        
        calendar_layout.addWidget(self.tasks_frame)
        
        layout.addWidget(calendar_frame)
        
        # Botões de controle
        controls = QFrame()
        controls_layout = QHBoxLayout(controls)
        
        add_task_btn = QPushButton("Nova Tarefa")
        add_task_btn.clicked.connect(self.add_task)
        controls_layout.addWidget(add_task_btn)
        
        layout.addWidget(controls)
        
    def load_tasks(self):
        """Carrega todas as tarefas do usuário e marca no calendário."""
        tasks = self.session.query(Task).filter_by(user_id=self.user_id).all()
        
        # Marcar datas com tarefas
        for task in tasks:
            if task.deadline:
                date = QDate(task.deadline.year, task.deadline.month, task.deadline.day)
                format = self.calendar.dateTextFormat(date)
                format.setBackground(Qt.cyan)
                self.calendar.setDateTextFormat(date, format)
                
    def show_tasks_for_date(self, date):
        """Mostra as tarefas para a data selecionada."""
        # Limpar lista atual
        for i in reversed(range(self.tasks_layout.count())):
            self.tasks_layout.itemAt(i).widget().setParent(None)
            
        # Título
        tasks_title = QLabel("Tarefas do Dia")
        tasks_title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.tasks_layout.addWidget(tasks_title)
        
        # Buscar tarefas da data
        selected_date = datetime(date.year(), date.month(), date.day())
        tasks = self.session.query(Task).filter(
            Task.user_id == self.user_id,
            Task.deadline >= selected_date,
            Task.deadline < selected_date.replace(hour=23, minute=59, second=59)
        ).all()
        
        # Mostrar tarefas
        for task in tasks:
            task_frame = QFrame()
            task_layout = QHBoxLayout(task_frame)
            
            title = QLabel(task.title)
            task_layout.addWidget(title)
            
            status = QLabel("✓" if task.completed else "⌛")
            task_layout.addWidget(status)
            
            self.tasks_layout.addWidget(task_frame)
            
        if not tasks:
            no_tasks = QLabel("Nenhuma tarefa para este dia")
            no_tasks.setStyleSheet("font-style: italic;")
            self.tasks_layout.addWidget(no_tasks)
            
    def add_task(self):
        """Abre diálogo para adicionar nova tarefa."""
        from src.gui.main_window import AddTaskDialog
        dialog = AddTaskDialog(self)
        if dialog.exec():
            self.load_tasks()
            self.show_tasks_for_date(self.calendar.selectedDate())
            
    def __del__(self):
        """Fecha as sessões do banco de dados."""
        self.session.close()
        self.task_manager.session.close() 