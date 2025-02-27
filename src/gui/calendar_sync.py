from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QFrame, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from src.services.google_calendar import GoogleCalendarService
from src.database.models import AppConfig
from src.database.database import get_session
from PIL import Image, ImageTk
import os
from datetime import datetime

class CalendarSyncWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_id = parent.user_id
        self.theme = parent.theme
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface de sincronização."""
        # Configuração da janela
        self.setWindowTitle("Sincronização com Google Calendar")
        self.setGeometry(100, 100, 600, 400)  # x, y, width, height
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Header
        header = QFrame()
        header_layout = QVBoxLayout(header)
        
        title = QLabel("Sincronização com Google Calendar")
        title.setFont(QFont("Roboto", 20, QFont.Bold))
        header_layout.addWidget(title)
        
        layout.addWidget(header)
        
        # Status
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        
        status_label = QLabel("Status da Sincronização:")
        status_label.setFont(QFont("Roboto", 14))
        status_layout.addWidget(status_label)
        
        self.sync_button = QPushButton("Sincronizar Agora")
        self.sync_button.clicked.connect(self.sync_now)
        status_layout.addWidget(self.sync_button)
        
        layout.addWidget(status_frame)
        
        # Serviços
        self.calendar_service = GoogleCalendarService(self.user_id)
        self.session = get_session()
        
        # Layout
        self.create_status_frame()
        self.create_sync_frame()
        
    def create_status_frame(self):
        """Cria o frame com status da sincronização."""
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        
        # Buscar configuração atual
        app_config = self.session.query(AppConfig).filter_by(
            user_id=self.user_id
        ).first()
        
        # Status atual
        status_label = QLabel(f"Status da Sincronização: {'Ativado' if app_config.calendar_sync_enabled else 'Desativado'}")
        status_layout.addWidget(status_label)
        
        self.sync_switch = QPushButton("Sincronização Automática")
        self.sync_switch.clicked.connect(self.toggle_sync)
        status_layout.addWidget(self.sync_switch)
        
        # Definir estado inicial do switch
        if app_config and app_config.calendar_sync_enabled:
            self.sync_switch.setText("Ativado")
        else:
            self.sync_switch.setText("Desativado")
            
    def create_sync_frame(self):
        """Cria o frame com botões de sincronização."""
        sync_frame = QFrame()
        sync_layout = QVBoxLayout(sync_frame)
        
        # Status da última sincronização
        self.last_sync_label = QLabel("Última sincronização: Nunca")
        sync_layout.addWidget(self.last_sync_label)
        
    def toggle_sync(self):
        """Altera o estado da sincronização automática."""
        app_config = self.session.query(AppConfig).filter_by(
            user_id=self.user_id
        ).first()
        
        if app_config:
            app_config.calendar_sync_enabled = self.sync_switch.text() == "Ativado"
            self.session.commit()
            
    def sync_now(self):
        """Executa sincronização manual."""
        success, message = self.calendar_service.sync_tasks()
        
        if success:
            self.last_sync_label.setText(f"Última sincronização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
        # Mostrar resultado
        result_window = QDialog(self)
        result_window.setWindowTitle("Resultado da Sincronização")
        result_window.setGeometry(300, 100, 300, 100)
        
        result_label = QLabel(message)
        result_label.setFont(QFont("Roboto", 12))
        result_label.setStyleSheet("color: green;" if success else "color: red;")
        
        result_layout = QVBoxLayout(result_window)
        result_layout.addWidget(result_label)
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 