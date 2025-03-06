from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from src.services.auth_manager import AuthManager
from src.gui.themes import Theme
import os
from src.database.database import get_data_dir

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configurar ícone da janela
        icon = QIcon(os.path.join(os.path.dirname(__file__), '..', 'img', 'logo.png'))
        self.setWindowIcon(icon)
        self.theme = Theme()
        self.auth_manager = AuthManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface de login."""
        self.setWindowTitle("Login - Matemática em Evidência")
        self.setFixedSize(400, 600)
        self.setStyleSheet(self.theme.get_main_style())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Logo
        logo_frame = QFrame()
        logo_frame.setObjectName("logoWidget")
        logo_layout = QVBoxLayout(logo_frame)
        
        if self.theme.logo:
            logo_label = QLabel()
            logo_label.setObjectName("logoImage")
            
            # Criar um QPixmap circular
            original_pixmap = self.theme.logo
            target_size = 150
            scaled_pixmap = original_pixmap.scaled(
                target_size, target_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Criar máscara circular
            mask = QBitmap(scaled_pixmap.size())
            mask.fill(Qt.color0)
            painter = QPainter(mask)
            painter.setBrush(Qt.color1)
            painter.setPen(Qt.color1)
            painter.drawEllipse(0, 0, target_size, target_size)
            painter.end()
            
            scaled_pixmap.setMask(mask)
            logo_label.setPixmap(scaled_pixmap)
            logo_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        
        layout.addWidget(logo_frame)
        
        # Formulário
        form_frame = QFrame()
        form_frame.setObjectName("formCard")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("input")
        form_layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("input")
        form_layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.setObjectName("primaryButton")
        login_btn.clicked.connect(self.handle_login)
        form_layout.addWidget(login_btn)
        
        # Register link
        register_btn = QPushButton("Criar nova conta")
        register_btn.setObjectName("linkButton")
        register_btn.clicked.connect(self.open_register)
        form_layout.addWidget(register_btn)
        
        layout.addWidget(form_frame)
        
    def handle_login(self):
        """Processa a tentativa de login."""
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            
            if not username or not password:
                QMessageBox.warning(
                    self,
                    "Erro",
                    "Por favor, preencha todos os campos!"
                )
                return
            
            user = self.auth_manager.login(username, password)
            if user:
                self.show_main_window(user.id)
            else:
                QMessageBox.warning(
                    self,
                    "Erro",
                    "Usuário ou senha inválidos!\n\n"
                    "Use as credenciais de teste:\n"
                    "Usuário: test\n"
                    "Senha: test123"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao fazer login: {str(e)}"
            )
            
    def show_main_window(self, user_id):
        """Mostra a janela principal."""
        from src.gui.main_window import MainWindow  # Importação local para evitar circular
        self.main_window = MainWindow(user_id)
        self.main_window.show()
        self.close()

    def open_register(self):
        # Importe RegisterWindow apenas quando necessário
        from src.gui.register import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

if __name__ == "__main__":
    app = LoginWindow()
    app.show() 