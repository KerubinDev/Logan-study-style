from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import random
import math
import time

class AnimatedTabWidget(QTabWidget):
    """TabWidget com transições animadas entre abas."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_index = 0
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        
        self.currentChanged.connect(self.animate_tab_change)
        
    def animate_tab_change(self, index):
        """Anima a troca de aba."""
        self.animation.stop()
        self.animation.setStartValue(0.3)
        self.animation.setEndValue(1.0)
        self.animation.start()
        
class SimpleEffects:
    """Classe para efeitos visuais e notificações."""
    
    def __init__(self):
        self.notification_queue = []
        self.current_notification = None
        
    def show_level_up(self, parent, level):
        """Mostra animação de level up com confete."""
        dialog = QDialog(parent)
        dialog.setWindowTitle("")
        dialog.setModal(True)
        dialog.setObjectName("achievementDialog")
        dialog.setFixedSize(400, 300)
        dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Ícone de level up
        icon_label = QLabel()
        pixmap = QPixmap("src/img/level_up.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        # Título
        title = QLabel(f"NÍVEL {level}!")
        title.setObjectName("achievementTitle")
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        # Mensagem
        message = QLabel("Você avançou de nível! Continue estudando para desbloquear novas conquistas.")
        message.setWordWrap(True)
        message.setObjectName("achievementMessage")
        layout.addWidget(message, alignment=Qt.AlignCenter)
        
        # Botão de fechar
        close_btn = QPushButton("Continuar")
        close_btn.setObjectName("achievementButton")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        # Adicionar efeito de confete
        self._add_confetti(dialog)
        
        # Animação de entrada
        opacity_effect = QGraphicsOpacityEffect(dialog)
        dialog.setGraphicsEffect(opacity_effect)
        
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(500)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
        dialog.exec()
        
    def _add_confetti(self, parent):
        """Adiciona efeito de confete à janela."""
        confetti = ConfettiWidget(parent)
        confetti.start()
        
    @staticmethod
    def show_achievement(parent, title, description):
        """Mostra uma notificação de conquista com animação."""
        from src.gui.visual_effects import ConfettiEffect
        
        # Exibir mensagem
        QMessageBox.information(
            parent,
            f"Nova Conquista: {title}",
            f"{description}\n\nParabéns por esta conquista!"
        )
        
        # Mostrar efeito de confete
        confetti = ConfettiEffect(parent)
        confetti.show()
        
    def queue_notification(self, parent, title, message, icon="info"):
        """Adiciona uma notificação à fila."""
        self.notification_queue.append({
            "parent": parent,
            "title": title,
            "message": message,
            "icon": icon
        })
        
        if not self.current_notification:
            self._show_next_notification()
    
    def _show_next_notification(self):
        """Mostra a próxima notificação na fila."""
        if not self.notification_queue:
            self.current_notification = None
            return
            
        notif = self.notification_queue.pop(0)
        self.current_notification = self._create_notification(
            notif["parent"],
            notif["title"],
            notif["message"],
            notif["icon"]
        )
        
    def _create_notification(self, parent, title, message, icon):
        """Cria e mostra uma notificação flutuante."""
        notif = QFrame(parent)
        notif.setObjectName("notification")
        notif.setFixedWidth(300)
        
        # Configurar notificação para ficar em cima da janela principal
        parent_geometry = parent.geometry()
        notif.setGeometry(
            parent_geometry.width() - 320,
            20,
            300,
            100
        )
        
        # Layout
        layout = QVBoxLayout(notif)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title_label = QLabel(title)
        title_label.setObjectName("notificationTitle")
        layout.addWidget(title_label)
        
        # Mensagem
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setObjectName("notificationMessage")
        layout.addWidget(message_label)
        
        # Mostrar notificação
        notif.show()
        
        # Animação de entrada
        animation = QPropertyAnimation(notif, b"geometry")
        animation.setDuration(300)
        start_rect = QRect(
            parent_geometry.width(),
            20,
            300,
            100
        )
        end_rect = QRect(
            parent_geometry.width() - 320,
            20,
            300,
            100
        )
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
        # Timer para remover a notificação
        QTimer.singleShot(5000, lambda: self._remove_notification(notif))
        
        return notif
        
    def _remove_notification(self, notif):
        """Remove uma notificação com animação."""
        parent_geometry = notif.parent().geometry()
        
        animation = QPropertyAnimation(notif, b"geometry")
        animation.setDuration(300)
        start_rect = notif.geometry()
        end_rect = QRect(
            parent_geometry.width(),
            20,
            300,
            100
        )
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.InCubic)
        animation.finished.connect(lambda: self._cleanup_notification(notif))
        animation.start()
        
    def _cleanup_notification(self, notif):
        """Limpa a notificação e mostra a próxima."""
        notif.deleteLater()
        self.current_notification = None
        QTimer.singleShot(300, self._show_next_notification)

class ConfettiWidget(QWidget):
    """Widget que exibe confetes caindo."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, parent.width(), parent.height())
        
        # Definir cores dos confetes
        self.colors = [
            QColor(255, 0, 0),    # Vermelho
            QColor(0, 255, 0),    # Verde
            QColor(0, 0, 255),    # Azul
            QColor(255, 255, 0),  # Amarelo
            QColor(255, 0, 255),  # Magenta
            QColor(0, 255, 255),  # Ciano
            QColor(255, 165, 0),  # Laranja
            QColor(128, 0, 128)   # Roxo
        ]
        
        # Inicializar confetes
        self.confetti = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_confetti)
        
        # Tornar o widget transparente
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def start(self):
        """Inicia a animação de confetes."""
        for _ in range(100):
            self.confetti.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(-50, 0),
                'speed': random.uniform(1, 5),
                'size': random.randint(5, 15),
                'color': random.choice(self.colors),
                'angle': random.uniform(0, 360),
                'rotation_speed': random.uniform(-5, 5)
            })
        
        self.timer.start(30)  # Atualizar a cada 30ms
        
    def update_confetti(self):
        """Atualiza a posição dos confetes."""
        for conf in self.confetti:
            conf['y'] += conf['speed']
            conf['x'] += math.sin(conf['angle'] * math.pi / 180) * 2
            conf['angle'] += conf['rotation_speed']
            
            # Resetar confetes que saíram da tela
            if conf['y'] > self.height():
                conf['y'] = random.randint(-50, 0)
                conf['x'] = random.randint(0, self.width())
        
        self.update()
        
        # Parar a animação após 5 segundos
        if not hasattr(self, 'start_time'):
            self.start_time = time.time()
        elif time.time() - self.start_time > 5:
            self.timer.stop()
            self.hide()
            
    def paintEvent(self, event):
        """Desenha os confetes na tela."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for conf in self.confetti:
            painter.save()
            painter.translate(conf['x'], conf['y'])
            painter.rotate(conf['angle'])
            painter.setBrush(conf['color'])
            painter.setPen(Qt.NoPen)
            painter.drawRect(-conf['size'] / 2, -conf['size'] / 2, conf['size'], conf['size'] / 2)
            painter.restore()

class ConfettiEffect(QWidget):
    """Efeito de confete para celebrações."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, parent.width() if parent else 400, parent.height() if parent else 300)
        
        # Definir cores dos confetes
        self.colors = [
            QColor(255, 0, 0),    # Vermelho
            QColor(0, 255, 0),    # Verde
            QColor(0, 0, 255),    # Azul
            QColor(255, 255, 0),  # Amarelo
            QColor(255, 0, 255),  # Magenta
            QColor(0, 255, 255),  # Ciano
            QColor(255, 165, 0),  # Laranja
            QColor(128, 0, 128)   # Roxo
        ]
        
        # Inicializar confetes
        self.confetti = []
        for _ in range(100):
            self.confetti.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(-50, 0),
                'speed': random.uniform(1, 5),
                'size': random.randint(5, 15),
                'color': random.choice(self.colors),
                'angle': random.uniform(0, 360),
                'rotation_speed': random.uniform(-5, 5)
            })
        
        # Configurar timer para atualização
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_confetti)
        self.timer.start(30)
        
        # Configurações da janela
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        
        # Tempo de início para calcular duração
        self.start_time = time.time()
        
    def update_confetti(self):
        """Atualiza a posição dos confetes."""
        for conf in self.confetti:
            conf['y'] += conf['speed']
            conf['x'] += math.sin(conf['angle'] * math.pi / 180) * 2
            conf['angle'] += conf['rotation_speed']
            
            # Resetar confetes que saírem da tela
            if conf['y'] > self.height():
                conf['y'] = random.randint(-50, 0)
                conf['x'] = random.randint(0, self.width())
        
        self.update()
        
        # Encerrar após 3 segundos
        if time.time() - self.start_time > 3:
            self.timer.stop()
            self.close()
            
    def paintEvent(self, event):
        """Desenha os confetes na tela."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for conf in self.confetti:
            painter.save()
            painter.translate(conf['x'], conf['y'])
            painter.rotate(conf['angle'])
            painter.setBrush(conf['color'])
            painter.setPen(Qt.NoPen)
            painter.drawRect(-conf['size'] / 2, -conf['size'] / 2, conf['size'], conf['size'] / 2)
            painter.restore() 