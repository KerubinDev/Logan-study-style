import customtkinter as ctk
from src.services.google_calendar import GoogleCalendarService
from src.database.models import AppConfig
from src.database.database import get_session
from PIL import Image, ImageTk
import os
from datetime import datetime

class CalendarSyncWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user_id = parent.user_id
        self.theme = parent.theme
        
        # Configuração da janela
        self.title("Sincronização com Google Calendar")
        self.geometry("600x400")
        
        # Serviços
        self.calendar_service = GoogleCalendarService(self.user_id)
        self.session = get_session()
        
        # Layout
        self.create_header()
        self.create_status_frame()
        self.create_sync_frame()
        
    def create_header(self):
        """Cria o cabeçalho com logo do Google Calendar."""
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Carregar logo
        logo_path = os.path.join("assets", "icons", "google_calendar.png")
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo = ImageTk.PhotoImage(logo.resize((32, 32)))
            
            logo_label = ctk.CTkLabel(
                header_frame,
                image=logo,
                text=""
            )
            logo_label.image = logo
            logo_label.pack(side="left", padx=10)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Sincronização com Google Calendar",
            font=("Roboto", 20, "bold")
        )
        title.pack(side="left", padx=10)
        
    def create_status_frame(self):
        """Cria o frame com status da sincronização."""
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Buscar configuração atual
        app_config = self.session.query(AppConfig).filter_by(
            user_id=self.user_id
        ).first()
        
        # Status atual
        status_label = ctk.CTkLabel(
            status_frame,
            text="Status da Sincronização:",
            font=("Roboto", 14)
        )
        status_label.pack(pady=5)
        
        self.sync_switch = ctk.CTkSwitch(
            status_frame,
            text="Sincronização Automática",
            command=self.toggle_sync
        )
        self.sync_switch.pack(pady=10)
        
        # Definir estado inicial do switch
        if app_config and app_config.calendar_sync_enabled:
            self.sync_switch.select()
        else:
            self.sync_switch.deselect()
            
    def create_sync_frame(self):
        """Cria o frame com botões de sincronização."""
        sync_frame = ctk.CTkFrame(self)
        sync_frame.pack(fill="x", padx=20, pady=10)
        
        # Botão de sincronização manual
        sync_button = ctk.CTkButton(
            sync_frame,
            text="Sincronizar Agora",
            command=self.sync_now
        )
        sync_button.pack(pady=10)
        
        # Status da última sincronização
        self.last_sync_label = ctk.CTkLabel(
            sync_frame,
            text="Última sincronização: Nunca",
            font=("Roboto", 12)
        )
        self.last_sync_label.pack(pady=5)
        
    def toggle_sync(self):
        """Altera o estado da sincronização automática."""
        app_config = self.session.query(AppConfig).filter_by(
            user_id=self.user_id
        ).first()
        
        if app_config:
            app_config.calendar_sync_enabled = self.sync_switch.get()
            self.session.commit()
            
    def sync_now(self):
        """Executa sincronização manual."""
        success, message = self.calendar_service.sync_tasks()
        
        if success:
            self.last_sync_label.configure(
                text=f"Última sincronização: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            )
            
        # Mostrar resultado
        result_window = ctk.CTkToplevel(self)
        result_window.title("Resultado da Sincronização")
        result_window.geometry("300x100")
        
        ctk.CTkLabel(
            result_window,
            text=message,
            text_color="green" if success else "red"
        ).pack(pady=20)
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 