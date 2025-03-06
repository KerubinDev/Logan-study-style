from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from datetime import datetime, timedelta
import math

class CircularProgressBar(QWidget):
    """Widget de progresso circular para o timer."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.max_value = 100
        self.min_value = 0
        self.suffix = "%"
        self.text_color = QColor("#ffffff")
        self.font = QFont("Roboto", 16, QFont.Bold)
        self.progress_color = QColor("#4169E1")  # Azul royal
        self.bg_color = QColor(50, 50, 50, 100)
        self.progress_width = 15
        self.setMinimumSize(200, 200)
    
    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))
        self.update()
        
    def set_progress_color(self, color):
        self.progress_color = color
        self.update()
    
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        margin = self.progress_width / 2
        size = min(width, height) - 2 * margin
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar círculo de fundo
        pen = QPen()
        pen.setWidth(self.progress_width)
        pen.setColor(self.bg_color)
        painter.setPen(pen)
        painter.drawEllipse(margin, margin, size, size)
        
        # Calcular progresso
        angle = self.value * 360 / (self.max_value - self.min_value)
        
        # Desenhar arco de progresso
        pen.setColor(self.progress_color)
        painter.setPen(pen)
        painter.drawArc(margin, margin, size, size, 90 * 16, -angle * 16)
        
        # Desenhar valor
        painter.setPen(self.text_color)
        painter.setFont(self.font)
        painter.drawText(0, 0, width, height, Qt.AlignCenter, self.time_text)

class AdvancedTimerWidget(QWidget):
    """Widget de cronômetro avançado com estimativa de término e recursos visuais."""
    
    timerFinished = Signal(str)  # Emite o tipo de ciclo (work, break, long_break)
    
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_remaining = 0
        self.total_time = 0
        self.completion_time = None
        self.pomodoro_count = 0
        self.mode = "work"  # work, break, long_break
        
        # Configurações padrão
        self.work_time = 25 * 60  # 25 minutos em segundos
        self.break_time = 5 * 60  # 5 minutos em segundos
        self.long_break_time = 15 * 60  # 15 minutos em segundos
        self.long_break_interval = 4  # A cada 4 pomodoros
        
        # Carregar configurações do usuário
        self.load_settings()
        
        # Inicializar timer para iniciar com modo "work"
        self.reset_timer()
    
    def setup_ui(self):
        """Configura a interface do widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)
        
        # Timer e controles em um card
        timer_card = QFrame()
        timer_card.setObjectName("timerCard")
        timer_layout = QVBoxLayout(timer_card)
        timer_layout.setSpacing(15)
        
        # Título do modo atual
        self.mode_label = QLabel("Pomodoro")
        self.mode_label.setObjectName("timerModeLabel")
        self.mode_label.setAlignment(Qt.AlignCenter)
        timer_layout.addWidget(self.mode_label)
        
        # Container do timer (circular)
        self.progress_bar = CircularProgressBar()
        self.progress_bar.time_text = "25:00"
        timer_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        
        # Estimativa de término
        self.eta_label = QLabel("Término estimado: --:--")
        self.eta_label.setObjectName("etaLabel")
        self.eta_label.setAlignment(Qt.AlignCenter)
        timer_layout.addWidget(self.eta_label)
        
        # Controles
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setSpacing(15)
        
        # Botão de iniciar/pausar
        self.start_btn = QPushButton("Iniciar")
        self.start_btn.setObjectName("timerButton")
        self.start_btn.clicked.connect(self.toggle_timer)
        controls_layout.addWidget(self.start_btn)
        
        # Botão de resetar
        self.reset_btn = QPushButton("Resetar")
        self.reset_btn.setObjectName("timerButton")
        self.reset_btn.clicked.connect(self.reset_timer)
        controls_layout.addWidget(self.reset_btn)
        
        # Botão de pular
        self.skip_btn = QPushButton("Pular")
        self.skip_btn.setObjectName("timerButton")
        self.skip_btn.clicked.connect(self.skip_timer)
        controls_layout.addWidget(self.skip_btn)
        
        timer_layout.addWidget(controls)
        
        # Contador de pomodoros
        pomodoro_counter = QWidget()
        pomodoro_layout = QHBoxLayout(pomodoro_counter)
        pomodoro_layout.setSpacing(10)
        
        pomodoro_label = QLabel("Pomodoros:")
        pomodoro_label.setObjectName("pomoCounterLabel")
        pomodoro_layout.addWidget(pomodoro_label)
        
        self.pomodoro_display = QLabel("0")
        self.pomodoro_display.setObjectName("pomoCounterValue")
        pomodoro_layout.addWidget(self.pomodoro_display)
        
        timer_layout.addWidget(pomodoro_counter, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(timer_card)
        
        # Seção de configurações
        settings_card = QFrame()
        settings_card.setObjectName("settingsCard")
        settings_layout = QVBoxLayout(settings_card)
        
        settings_title = QLabel("Configurações do Timer")
        settings_title.setObjectName("settingsTitle")
        settings_layout.addWidget(settings_title)
        
        # Formulário de configurações
        settings_form = QFormLayout()
        
        # Tempo de trabalho
        self.work_time_input = QSpinBox()
        self.work_time_input.setRange(1, 120)  # 1-120 minutos
        self.work_time_input.setValue(25)
        self.work_time_input.setSuffix(" min")
        settings_form.addRow("Tempo de trabalho:", self.work_time_input)
        
        # Tempo de pausa curta
        self.break_time_input = QSpinBox()
        self.break_time_input.setRange(1, 30)  # 1-30 minutos
        self.break_time_input.setValue(5)
        self.break_time_input.setSuffix(" min")
        settings_form.addRow("Pausa curta:", self.break_time_input)
        
        # Tempo de pausa longa
        self.long_break_time_input = QSpinBox()
        self.long_break_time_input.setRange(5, 60)  # 5-60 minutos
        self.long_break_time_input.setValue(15)
        self.long_break_time_input.setSuffix(" min")
        settings_form.addRow("Pausa longa:", self.long_break_time_input)
        
        # Intervalo de pausas longas
        self.long_break_interval_input = QSpinBox()
        self.long_break_interval_input.setRange(2, 10)  # Após 2-10 pomodoros
        self.long_break_interval_input.setValue(4)
        self.long_break_interval_input.setSuffix(" pomodoros")
        settings_form.addRow("Pausa longa após:", self.long_break_interval_input)
        
        settings_layout.addLayout(settings_form)
        
        # Botão de salvar configurações
        save_btn = QPushButton("Salvar Configurações")
        save_btn.setObjectName("accentButton")
        save_btn.clicked.connect(self.save_settings)
        settings_layout.addWidget(save_btn)
        
        main_layout.addWidget(settings_card)
    
    def toggle_timer(self):
        """Inicia ou pausa o timer."""
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Retomar")
            self.eta_label.setText("Pausa - Término estimado: --:--")
        else:
            self.timer.start(1000)  # Atualizar a cada segundo
            self.start_btn.setText("Pausar")
            
            # Atualizar estimativa de término
            self.update_eta()
    
    def update_timer(self):
        """Atualiza o timer a cada segundo."""
        self.time_remaining -= 1
        
        # Atualizar progresso visual
        progress = 100 - (self.time_remaining * 100 / self.total_time)
        self.progress_bar.set_value(progress)
        
        # Formatar e exibir tempo restante
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        self.progress_bar.time_text = time_text
        self.progress_bar.update()
        
        # Verificar se o timer acabou
        if self.time_remaining <= 0:
            self.timer.stop()
            self.timer_completed()
    
    def reset_timer(self):
        """Reseta o timer para os valores iniciais com base no modo atual."""
        self.timer.stop()
        
        if self.mode == "work":
            self.time_remaining = self.work_time
            self.total_time = self.work_time
            self.mode_label.setText("Pomodoro")
            self.progress_bar.set_progress_color(QColor("#4169E1"))  # Azul
        elif self.mode == "break":
            self.time_remaining = self.break_time
            self.total_time = self.break_time
            self.mode_label.setText("Pausa Curta")
            self.progress_bar.set_progress_color(QColor("#43b581"))  # Verde
        else:  # long_break
            self.time_remaining = self.long_break_time
            self.total_time = self.long_break_time
            self.mode_label.setText("Pausa Longa")
            self.progress_bar.set_progress_color(QColor("#7289da"))  # Lilás
        
        # Atualizar interface
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        self.progress_bar.time_text = time_text
        self.progress_bar.set_value(0)
        self.progress_bar.update()
        
        self.start_btn.setText("Iniciar")
        self.eta_label.setText("Término estimado: --:--")
    
    def skip_timer(self):
        """Pula o timer atual e passa para o próximo estado."""
        self.timer.stop()
        self.timer_completed()
    
    def timer_completed(self):
        """Processa o término do timer e configura o próximo."""
        # Emitir sinal de término
        self.timerFinished.emit(self.mode)
        
        # Se era um ciclo de trabalho, incrementar contador de pomodoros
        if self.mode == "work":
            self.pomodoro_count += 1
            self.pomodoro_display.setText(str(self.pomodoro_count))
            
            # Decidir qual pausa vem a seguir
            if self.pomodoro_count % self.long_break_interval == 0:
                self.mode = "long_break"
            else:
                self.mode = "break"
        else:
            # Se era uma pausa, voltar para o modo de trabalho
            self.mode = "work"
        
        # Resetar e iniciar automaticamente o próximo timer
        self.reset_timer()
        self.toggle_timer()
    
    def update_eta(self):
        """Atualiza a estimativa de término."""
        if not self.timer.isActive():
            return
            
        current_time = datetime.now()
        eta = current_time + timedelta(seconds=self.time_remaining)
        self.eta_label.setText(f"Término estimado: {eta.strftime('%H:%M')}")
    
    def load_settings(self):
        """Carrega as configurações do timer para o usuário atual."""
        # Aqui você pode implementar a lógica para carregar configurações 
        # personalizadas do banco de dados
        
        # Por enquanto, vamos usar as configurações padrão
        self.work_time_input.setValue(self.work_time // 60)
        self.break_time_input.setValue(self.break_time // 60)
        self.long_break_time_input.setValue(self.long_break_time // 60)
        self.long_break_interval_input.setValue(self.long_break_interval)
    
    def save_settings(self):
        """Salva as configurações do timer."""
        # Atualizar configurações
        self.work_time = self.work_time_input.value() * 60
        self.break_time = self.break_time_input.value() * 60
        self.long_break_time = self.long_break_time_input.value() * 60
        self.long_break_interval = self.long_break_interval_input.value()
        
        # Resetar timer com novas configurações
        self.reset_timer()
        
        # Mostrar confirmação
        QMessageBox.information(
            self, "Configurações Salvas",
            "As configurações do timer foram atualizadas."
        )
        
        # Aqui você pode implementar a lógica para salvar as configurações 
        # no banco de dados para o usuário atual 