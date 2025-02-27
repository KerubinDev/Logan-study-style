from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from src.database.models import AppConfig, PomodoroConfig
from src.gui.themes import Theme

class SettingsWindow(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.theme = Theme()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface de configurações."""
        self.setWindowTitle("Configurações")
        self.setMinimumWidth(500)
        self.setStyleSheet(self.theme.get_main_style())
        
        layout = QVBoxLayout(self)
        
        # Configurações do App
        app_group = QGroupBox("Configurações do App")
        app_layout = QVBoxLayout()
        
        # Tema
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Tema:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        app_layout.addLayout(theme_layout)
        
        # Notificações
        self.notifications_check = QCheckBox("Ativar Notificações")
        app_layout.addWidget(self.notifications_check)
        
        # Sincronização com Calendar
        self.calendar_sync_check = QCheckBox("Sincronizar com Google Calendar")
        app_layout.addWidget(self.calendar_sync_check)
        
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)
        
        # Configurações do Pomodoro
        pomodoro_group = QGroupBox("Configurações do Pomodoro")
        pomodoro_layout = QVBoxLayout()
        
        # Tempo de trabalho
        work_layout = QHBoxLayout()
        work_label = QLabel("Tempo de Trabalho (min):")
        self.work_time_spin = QSpinBox()
        self.work_time_spin.setRange(1, 60)
        work_layout.addWidget(work_label)
        work_layout.addWidget(self.work_time_spin)
        pomodoro_layout.addLayout(work_layout)
        
        # Tempo de pausa
        break_layout = QHBoxLayout()
        break_label = QLabel("Tempo de Pausa (min):")
        self.break_time_spin = QSpinBox()
        self.break_time_spin.setRange(1, 30)
        break_layout.addWidget(break_label)
        break_layout.addWidget(self.break_time_spin)
        pomodoro_layout.addLayout(break_layout)
        
        # Pausa longa
        long_break_layout = QHBoxLayout()
        long_break_label = QLabel("Pausa Longa (min):")
        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 60)
        long_break_layout.addWidget(long_break_label)
        long_break_layout.addWidget(self.long_break_spin)
        pomodoro_layout.addLayout(long_break_layout)
        
        # Bloqueio de distrações
        self.block_distractions_check = QCheckBox("Bloquear Distrações")
        pomodoro_layout.addWidget(self.block_distractions_check)
        
        pomodoro_group.setLayout(pomodoro_layout)
        layout.addWidget(pomodoro_group)
        
        # Botões
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Carregar configurações atuais
        self.load_settings()
        
    def load_settings(self):
        """Carrega as configurações do usuário."""
        from src.database.database import get_session
        session = get_session()
        
        # App Config
        app_config = session.query(AppConfig).filter_by(user_id=self.user_id).first()
        if app_config:
            self.theme_combo.setCurrentText(app_config.theme)
            self.notifications_check.setChecked(app_config.notifications_enabled)
            self.calendar_sync_check.setChecked(app_config.calendar_sync_enabled)
            
        # Pomodoro Config
        pomodoro_config = session.query(PomodoroConfig).filter_by(user_id=self.user_id).first()
        if pomodoro_config:
            self.work_time_spin.setValue(pomodoro_config.work_time)
            self.break_time_spin.setValue(pomodoro_config.break_time)
            self.long_break_spin.setValue(pomodoro_config.long_break_time)
            self.block_distractions_check.setChecked(pomodoro_config.block_distractions)
            
        session.close()
        
    def save_settings(self):
        """Salva as configurações do usuário."""
        from src.database.database import get_session
        session = get_session()
        
        # App Config
        app_config = session.query(AppConfig).filter_by(user_id=self.user_id).first()
        if not app_config:
            app_config = AppConfig(user_id=self.user_id)
            session.add(app_config)
            
        app_config.theme = self.theme_combo.currentText()
        app_config.notifications_enabled = self.notifications_check.isChecked()
        app_config.calendar_sync_enabled = self.calendar_sync_check.isChecked()
        
        # Pomodoro Config
        pomodoro_config = session.query(PomodoroConfig).filter_by(user_id=self.user_id).first()
        if not pomodoro_config:
            pomodoro_config = PomodoroConfig(user_id=self.user_id)
            session.add(pomodoro_config)
            
        pomodoro_config.work_time = self.work_time_spin.value()
        pomodoro_config.break_time = self.break_time_spin.value()
        pomodoro_config.long_break_time = self.long_break_spin.value()
        pomodoro_config.block_distractions = self.block_distractions_check.isChecked()
        
        session.commit()
        session.close()
        
        QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")
        self.accept() 