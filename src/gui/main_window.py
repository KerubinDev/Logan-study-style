from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from src.config.settings import THEMES, POMODORO_DEFAULTS
from src.services.pomodoro import PomodoroTimer
from src.services.task_manager import TaskManager
from src.services.report_generator import ReportGenerator
from src.gui.visual_effects import AnimeVisualEffects
from plyer import notification
from src.gui.settings import SettingsWindow
from tkinter import filedialog
import os
from src.gui.calendar_view import CalendarWindow
from src.gui.distraction_manager import DistractionManagerWindow
from src.gui.themes import Theme
from PySide6.QtCore import QTimer
from src.services.session_manager import SessionManager
from src.gui.login import LoginWindow
from src.services.auth_manager import AuthManager

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.theme = Theme()
        self.pomodoro_timer = PomodoroTimer(user_id)
        self.task_manager = TaskManager(user_id)
        self.visual_effects = AnimeVisualEffects()
        self.auth_manager = AuthManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface principal."""
        # Configuração da janela
        self.setWindowTitle("AnimeProductivity")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(self.theme.get_main_style())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Área de conteúdo
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(content_area)
        
        # Adicionar widgets de conteúdo
        self.create_pomodoro_widget(content_layout)
        self.create_tasks_widget(content_layout)
        self.create_stats_widget(content_layout)
        
    def create_sidebar(self):
        """Cria a barra lateral com navegação."""
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo
        logo_widget = QWidget()
        logo_widget.setObjectName("logoWidget")
        logo_layout = QVBoxLayout(logo_widget)
        
        logo_title = QLabel("アニメ")
        logo_title.setObjectName("logoTitle")
        logo_subtitle = QLabel("Productivity")
        logo_subtitle.setObjectName("logoSubtitle")
        
        logo_layout.addWidget(logo_title, alignment=Qt.AlignCenter)
        logo_layout.addWidget(logo_subtitle, alignment=Qt.AlignCenter)
        sidebar_layout.addWidget(logo_widget)
        
        # Menu de navegação
        nav_menu = QWidget()
        nav_menu.setObjectName("navMenu")
        nav_layout = QVBoxLayout(nav_menu)
        nav_layout.setSpacing(5)
        
        menu_items = [
            ("Dashboard", "🏠", self.show_dashboard),
            ("Tarefas", "📝", self.show_tasks),
            ("Estatísticas", "📊", self.show_stats),
            ("Configurações", "⚙️", self.show_settings),
            ("Agenda", "📅", self.show_calendar_sync),
            ("Bloqueio", "🚫", self.show_distraction_manager)
        ]
        
        for text, icon, callback in menu_items:
            btn = QPushButton(f"{icon} {text}")
            btn.setObjectName("navButton")
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            
        # Adicionar botão de logout
        logout_button = QPushButton("🚪 Logout")
        logout_button.setObjectName("navButton")
        logout_button.clicked.connect(self.handle_logout)
        nav_layout.addWidget(logout_button)
        
        sidebar_layout.addWidget(nav_menu)
        sidebar_layout.addStretch()
        
    def create_pomodoro_widget(self, layout):
        """Cria o widget do timer Pomodoro."""
        self.pomodoro_frame = QFrame()
        self.pomodoro_frame.setObjectName("pomodoroFrame")
        pomodoro_layout = QVBoxLayout(self.pomodoro_frame)
        
        # Timer display (sem imagem)
        self.timer_label = QLabel("25:00")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setStyleSheet("font-size: 48pt; font-weight: bold;")
        pomodoro_layout.addWidget(self.timer_label)
        
        # Botões de controle com emojis
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(5)
        
        self.start_button = QPushButton("▶️ Iniciar")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_pomodoro)
        controls_layout.addWidget(self.start_button)
        
        self.pause_button = QPushButton("⏸️ Pausar")
        self.pause_button.setObjectName("pauseButton")
        self.pause_button.clicked.connect(self.pause_pomodoro)
        controls_layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("🔄 Resetar")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_pomodoro)
        controls_layout.addWidget(self.reset_button)
        
        pomodoro_layout.addWidget(controls_frame)
        layout.addWidget(self.pomodoro_frame)
        
        # Atualizar display inicial
        self.update_timer_display()
        
    def create_tasks_widget(self, layout):
        """Cria o widget de tarefas."""
        self.tasks_frame = QFrame()
        self.tasks_frame.setObjectName("tasksFrame")
        tasks_layout = QVBoxLayout(self.tasks_frame)
        
        # Título e botão de adicionar
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        header_title = QLabel("Tarefas de Hoje")
        header_title.setStyleSheet("font-size: 20pt; font-weight: bold;")
        header_layout.addWidget(header_title)
        
        add_button = QPushButton("+ Nova Tarefa")
        add_button.clicked.connect(self.show_add_task_dialog)
        header_layout.addWidget(add_button)
        
        tasks_layout.addWidget(header_frame)
        
        # Lista de tarefas
        self.tasks_list = QFrame()
        tasks_list_layout = QVBoxLayout(self.tasks_list)  # Adicionar layout aqui
        self.tasks_list.setLayout(tasks_list_layout)
        tasks_layout.addWidget(self.tasks_list)
        
        layout.addWidget(self.tasks_frame)
        
        # Carregar tarefas do usuário
        self.load_tasks()
        
    def create_stats_widget(self, layout):
        """Cria o widget de estatísticas."""
        self.stats_frame = QFrame()
        self.stats_frame.setObjectName("statsFrame")
        stats_layout = QVBoxLayout(self.stats_frame)
        
        # Estatísticas básicas
        stats = [
            ("Pomodoros Hoje", "0"),
            ("Tempo Focado", "0h 0m"),
            ("Tarefas Concluídas", "0")
        ]
        
        for title, value in stats:
            stat_frame = QFrame()
            stat_layout = QHBoxLayout(stat_frame)
            stat_layout.setContentsMargins(10, 10, 10, 10)
            
            stat_title = QLabel(title)
            stat_title.setObjectName("statTitle")
            stat_layout.addWidget(stat_title)
            
            stat_value = QLabel(value)
            stat_value.setObjectName("statValue")
            stat_value.setStyleSheet("font-size: 24pt; font-weight: bold;")
            stat_layout.addWidget(stat_value)
            
            stats_layout.addWidget(stat_frame)
        
        # Criar e conectar o botão de estatísticas aqui
        self.stats_button = QPushButton("Ver Estatísticas Detalhadas")
        self.stats_button.setObjectName("statsButton")
        self.stats_button.clicked.connect(self.show_statistics)
        stats_layout.addWidget(self.stats_button)
        
        # Botão de relatório
        report_button = QPushButton("Gerar Relatório Semanal")
        report_button.setObjectName("reportButton")
        report_button.clicked.connect(self.generate_report)
        stats_layout.addWidget(report_button)
        
        layout.addWidget(self.stats_frame)
        
    def start_pomodoro(self):
        """Inicia o timer Pomodoro."""
        self.pomodoro_timer.start()
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        QTimer.singleShot(1000, self.update_timer)  # Importante: iniciar o timer
        
    def pause_pomodoro(self):
        """Pausa o timer Pomodoro."""
        self.pomodoro_timer.pause()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        
    def reset_pomodoro(self):
        """Reseta o timer Pomodoro."""
        self.pomodoro_timer.reset()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.timer_label.setText("25:00")
        
    def update_timer(self):
        """Atualiza o display do timer."""
        if self.pomodoro_timer.is_running:
            remaining = self.pomodoro_timer.get_remaining_time()
            if remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
                self.pomodoro_timer.time_remaining -= 1
                QTimer.singleShot(1000, self.update_timer)
            else:
                self.show_break_notification()
                self.reset_pomodoro()
                
    def show_break_notification(self):
        """Mostra notificação de intervalo."""
        notification.notify(
            title="Hora do Intervalo!",
            message="Parabéns! Você completou um Pomodoro. Hora de descansar!",
            app_icon=None,  # Adicionar ícone personalizado
            timeout=10
        )
        
    def load_tasks(self):
        """Carrega e exibe as tarefas do usuário."""
        # Limpar lista atual
        while self.tasks_list.layout().count():
            child = self.tasks_list.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Carregar tarefas do dia
        tasks = self.task_manager.get_today_tasks()
        
        for task in tasks:
            self.add_task_to_list(task)
            
    def add_task_to_list(self, task):
        """Adiciona uma tarefa à lista visual."""
        task_frame = QFrame()
        task_layout = QHBoxLayout(task_frame)
        task_layout.setContentsMargins(5, 2, 5, 2)
        
        checkbox = QCheckBox()
        checkbox.setObjectName("taskCheckbox")
        checkbox.setText(task.title)
        checkbox.setChecked(task.completed)  # Definir estado inicial
        checkbox.stateChanged.connect(lambda state, t=task.id: self.toggle_task(t))
        task_layout.addWidget(checkbox)
        
        # Adicionar deadline se existir
        if task.deadline:
            deadline_label = QLabel(task.deadline.strftime("%d/%m/%Y %H:%M"))
            deadline_label.setStyleSheet("color: gray;")
            task_layout.addWidget(deadline_label)
        
        delete_button = QPushButton("🗑️")
        delete_button.setObjectName("deleteButton")
        delete_button.clicked.connect(lambda _, t=task.id: self.delete_task(t))
        task_layout.addWidget(delete_button)
        
        self.tasks_list.layout().addWidget(task_frame)
        
    def show_add_task_dialog(self):
        """Mostra diálogo para adicionar nova tarefa."""
        dialog = AddTaskDialog(self)
        dialog.exec()
        
    def show_dashboard(self):
        """Mostra a página do dashboard."""
        self.pomodoro_frame.show()
        self.tasks_frame.show()
        self.stats_frame.show()
        
    def show_tasks(self):
        """Mostra a página de tarefas."""
        self.tasks_frame.show()
        self.pomodoro_frame.hide()
        self.stats_frame.hide()
        
    def show_stats(self):
        """Mostra a página de estatísticas."""
        self.stats_frame.show()
        self.pomodoro_frame.hide()
        self.tasks_frame.hide()
        
    def show_settings(self):
        """Mostra a página de configurações."""
        settings_window = SettingsWindow(self)
        settings_window.exec()
        
    def show_calendar_sync(self):
        """Mostra o calendário de tarefas."""
        calendar_window = CalendarWindow(self)
        calendar_window.exec()
        
    def show_distraction_manager(self):
        """Mostra o gerenciador de bloqueio de distrações."""
        distraction_window = DistractionManagerWindow(self)
        distraction_window.exec()
        
    def apply_theme(self, theme_name: str):
        """Aplica o tema selecionado à interface."""
        self.theme = THEMES[theme_name]
        
        # Atualizar estilos da janela principal
        self.setStyleSheet(self.theme.get_main_style())
        
        # Atualizar estilos da sidebar
        self.sidebar.setStyleSheet(self.theme.get_sidebar_style())
        
        # Atualizar estilos dos widgets
        self.pomodoro_frame.setStyleSheet(self.theme.get_pomodoro_style())
        self.tasks_frame.setStyleSheet(self.theme.get_tasks_style())
        self.stats_frame.setStyleSheet(self.theme.get_stats_style())
        
        # Atualizar estilos dos textos
        self.timer_label.setStyleSheet(self.theme.get_timer_style())
        
        # Atualizar estilos dos botões
        for button in self.sidebar.findChildren(QPushButton):
            button.setStyleSheet(self.theme.get_button_style())

    def generate_report(self):
        """Gera e salva um relatório semanal em PDF."""
        # Solicitar local para salvar
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório Semanal", "", "PDF Files (*.pdf)")
        
        if file_path:
            try:
                # Gerar o relatório
                report_generator = ReportGenerator(self.user_id)
                report_generator.generate_weekly_report(file_path)
                
                # Mostrar mensagem de sucesso
                notification.notify(
                    title="Relatório Gerado",
                    message=f"O relatório foi salvo em:\n{file_path}",
                    timeout=5
                )
                
                # Abrir o relatório
                os.startfile(file_path)
                
            except Exception as e:
                # Mostrar erro
                error_window = QMessageBox(self)
                error_window.setIcon(QMessageBox.Critical)
                error_window.setWindowTitle("Erro")
                error_window.setText(f"Erro ao gerar relatório:\n{str(e)}")
                error_window.exec()

    def show_statistics(self):
        """Mostra a janela de estatísticas."""
        from src.gui.statistics import StatisticsWindow
        stats_window = StatisticsWindow(self)
        stats_window.exec()  # Use exec() para diálogos modais

    def toggle_task(self, task_id: int):
        """Alterna o estado de conclusão da tarefa."""
        if self.task_manager.complete_task(task_id):
            # Recarregar a lista de tarefas para atualizar a interface
            self.load_tasks()
            
            # Atualizar estatísticas
            self.update_stats()
            
            # Mostrar notificação
            notification.notify(
                title="Tarefa Concluída",
                message="Parabéns! Continue assim! 🎉",
                timeout=5
            )
    
    def delete_task(self, task_id: int):
        """Remove uma tarefa."""
        # Confirmar exclusão
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir esta tarefa?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            if self.task_manager.delete_task(task_id):
                # Recarregar a lista de tarefas
                self.load_tasks()
                
                # Atualizar estatísticas
                self.update_stats()
                
                # Mostrar notificação
                notification.notify(
                    title="Tarefa Removida",
                    message="A tarefa foi removida com sucesso.",
                    timeout=5
                )
    
    def update_stats(self):
        """Atualiza as estatísticas exibidas."""
        # Implementar atualização das estatísticas aqui
        pass

    def handle_logout(self):
        """Processa o logout do usuário."""
        confirm = QMessageBox.question(
            self,
            "Confirmar Logout",
            "Tem certeza que deseja sair?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.auth_manager.logout()
            self.close()
            
            # Mostrar nova janela de login
            login = LoginWindow()
            login.show()

    def update_timer_display(self):
        """Atualiza o display do timer com o tempo atual."""
        minutes = self.pomodoro_timer.time_remaining // 60
        seconds = self.pomodoro_timer.time_remaining % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

class AddTaskDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        
        self.setWindowTitle("Nova Tarefa")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Campos do formulário
        self.title_label = QLabel("Título:")
        self.title_entry = QLineEdit()
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_entry)
        
        self.description_label = QLabel("Descrição:")
        self.description_entry = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_entry)
        
        # Usar QDateTimeEdit para deadline
        self.deadline_label = QLabel("Deadline:")
        self.deadline_entry = QDateTimeEdit()
        self.deadline_entry.setCalendarPopup(True)
        self.deadline_entry.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_entry)
        
        # Botões
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_task)
        buttons_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        
    def save_task(self):
        """Salva a nova tarefa."""
        title = self.title_entry.text()
        description = self.description_entry.toPlainText()
        deadline = self.deadline_entry.dateTime().toString("yyyy-MM-dd HH:mm")
        
        if title:
            self.parent_window.task_manager.add_task(title, description, deadline)
            self.parent_window.load_tasks()
            self.accept() 