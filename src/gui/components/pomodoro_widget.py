from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_color = QColor("#7aa2f7")
        self.setFixedSize(self.width, self.height)
        
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRectF(
            self.progress_width/2,
            self.progress_width/2,
            self.width - self.progress_width,
            self.height - self.progress_width
        )
        
        # Desenhar círculo base
        painter.setPen(QPen(QColor("#24283b"), self.progress_width))
        painter.drawArc(rect, 0, 360 * 16)
        
        # Desenhar progresso
        painter.setPen(QPen(self.progress_color, self.progress_width))
        painter.drawArc(rect, 90 * 16, -self.value * 360 * 16)
        
        painter.end()
        
    def set_value(self, value):
        self.value = value
        self.update()

class PomodoroWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        
        layout = QVBoxLayout(self)
        
        # Timer circular
        self.progress = CircularProgress()
        layout.addWidget(self.progress, alignment=Qt.AlignCenter)
        
        # Timer display
        self.time_label = QLabel("25:00")
        self.time_label.setObjectName("timerLabel")
        self.time_label.setStyleSheet("""
            QLabel#timerLabel {
                font-size: 48px;
                font-weight: bold;
                color: #7aa2f7;
            }
        """)
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        
        # Controles
        controls = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Iniciar")
        self.pause_btn = QPushButton("⏸️ Pausar")
        self.reset_btn = QPushButton("🔄 Resetar")
        
        controls.addWidget(self.start_btn)
        controls.addWidget(self.pause_btn)
        controls.addWidget(self.reset_btn)
        
        layout.addLayout(controls) 