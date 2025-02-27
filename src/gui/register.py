from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from src.database.models import User
from src.gui.themes import Theme
from src.gui.login import LoginWindow

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = Theme()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface de registro."""
        self.setWindowTitle("Registro - AnimeProductivity")
        self.setFixedSize(400, 600)
        self.setStyleSheet(self.theme.get_main_style())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo
        logo_frame = QFrame()
        logo_frame.setObjectName("logoWidget")
        logo_layout = QVBoxLayout(logo_frame)
        
        logo_title = QLabel("アニメ")
        logo_title.setObjectName("logoTitle")
        logo_subtitle = QLabel("Productivity")
        logo_subtitle.setObjectName("logoSubtitle")
        
        logo_layout.addWidget(logo_title, alignment=Qt.AlignCenter)
        logo_layout.addWidget(logo_subtitle, alignment=Qt.AlignCenter)
        layout.addWidget(logo_frame)
        
        # Formulário
        form_frame = QFrame()
        form_frame.setObjectName("card")
        form_layout = QVBoxLayout(form_frame)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("input")
        form_layout.addWidget(self.username_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email (opcional)")
        self.email_input.setObjectName("input")
        form_layout.addWidget(self.email_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("input")
        form_layout.addWidget(self.password_input)
        
        # Confirm Password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar Senha")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setObjectName("input")
        form_layout.addWidget(self.confirm_password_input)
        
        # Register button
        register_btn = QPushButton("Criar Conta")
        register_btn.setObjectName("primaryButton")
        register_btn.clicked.connect(self.handle_register)
        form_layout.addWidget(register_btn)
        
        # Login link
        login_btn = QPushButton("Já tem uma conta? Faça login")
        login_btn.setObjectName("linkButton")
        login_btn.clicked.connect(self.show_login)
        form_layout.addWidget(login_btn)
        
        layout.addWidget(form_frame)
        
    def handle_register(self):
        """Processa o registro do usuário."""
        username = self.username_input.text()
        email = self.email_input.text() or None
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validações
        if not username or not password or not confirm_password:
            self.show_error("Por favor, preencha todos os campos obrigatórios!")
            return
            
        if password != confirm_password:
            self.show_error("As senhas não coincidem!")
            return
            
        if len(password) < 6:
            self.show_error("A senha deve ter pelo menos 6 caracteres!")
            return
            
        # Criar usuário
        user = User.create(username=username, password=password, email=email)
        
        if user:
            QMessageBox.information(
                self,
                "Sucesso",
                "Conta criada com sucesso! Faça login para continuar.",
                QMessageBox.Ok
            )
            self.show_login()
        else:
            self.show_error("Nome de usuário já existe!")
            
    def show_error(self, message):
        """Mostra uma mensagem de erro."""
        QMessageBox.critical(self, "Erro", message, QMessageBox.Ok)
        
    def show_login(self):
        """Volta para a tela de login."""
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close() 