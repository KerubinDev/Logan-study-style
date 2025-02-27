import customtkinter as ctk
from src.services.distraction_blocker import DistractionBlocker
from typing import Dict, List
import json

class DistractionManagerWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.theme = parent.theme
        
        # Configuração da janela
        self.title("Gerenciador de Distrações")
        self.geometry("800x600")
        
        # Serviço de bloqueio
        self.blocker = DistractionBlocker()
        
        # Layout
        self.create_header()
        self.create_control_frame()
        self.create_sites_manager()
        
    def create_header(self):
        """Cria o cabeçalho com título e status."""
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Bloqueio de Distrações",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=10)
        
        description = ctk.CTkLabel(
            header_frame,
            text="Gerencie sites que podem atrapalhar sua produtividade",
            font=("Roboto", 14)
        )
        description.pack()
        
    def create_control_frame(self):
        """Cria o frame com controles de bloqueio."""
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Status atual
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="Status: Inativo",
            font=("Roboto", 16)
        )
        self.status_label.pack(pady=10)
        
        # Botões de controle
        buttons_frame = ctk.CTkFrame(control_frame)
        buttons_frame.pack(pady=10)
        
        self.start_button = ctk.CTkButton(
            buttons_frame,
            text="Ativar Bloqueio",
            command=self.toggle_blocking
        )
        self.start_button.pack(side="left", padx=10)
        
        # Atualizar estado inicial
        if self.blocker.is_active:
            self.status_label.configure(text="Status: Ativo")
            self.start_button.configure(text="Desativar Bloqueio")
            
    def create_sites_manager(self):
        """Cria o gerenciador de sites bloqueados."""
        sites_frame = ctk.CTkFrame(self)
        sites_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame de adição
        add_frame = ctk.CTkFrame(sites_frame)
        add_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            add_frame,
            text="Adicionar Site:"
        ).pack(side="left", padx=5)
        
        self.site_entry = ctk.CTkEntry(add_frame, width=200)
        self.site_entry.pack(side="left", padx=5)
        
        self.category_combobox = ctk.CTkComboBox(
            add_frame,
            values=list(self.blocker.blocked_sites.keys())
        )
        self.category_combobox.pack(side="left", padx=5)
        
        ctk.CTkButton(
            add_frame,
            text="Adicionar",
            command=self.add_site
        ).pack(side="left", padx=5)
        
        # Lista de sites por categoria
        sites_list = ctk.CTkScrollableFrame(sites_frame)
        sites_list.pack(fill="both", expand=True, pady=10)
        
        for category, sites in self.blocker.blocked_sites.items():
            # Frame da categoria
            category_frame = ctk.CTkFrame(sites_list)
            category_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                category_frame,
                text=category,
                font=("Roboto", 14, "bold")
            ).pack(anchor="w", padx=10, pady=5)
            
            # Lista de sites
            for site in sites:
                site_frame = ctk.CTkFrame(category_frame)
                site_frame.pack(fill="x", padx=20, pady=2)
                
                ctk.CTkLabel(
                    site_frame,
                    text=site
                ).pack(side="left", padx=5)
                
                ctk.CTkButton(
                    site_frame,
                    text="Remover",
                    width=80,
                    command=lambda s=site, c=category: self.remove_site(s, c)
                ).pack(side="right", padx=5)
                
    def toggle_blocking(self):
        """Alterna o estado do bloqueio."""
        if self.blocker.is_active:
            success, message = self.blocker.stop_blocking()
        else:
            success, message = self.blocker.start_blocking()
            
        if success:
            self.status_label.configure(
                text=f"Status: {'Ativo' if self.blocker.is_active else 'Inativo'}"
            )
            self.start_button.configure(
                text="Desativar Bloqueio" if self.blocker.is_active else "Ativar Bloqueio"
            )
            
        # Mostrar mensagem
        message_window = ctk.CTkToplevel(self)
        message_window.title("Resultado")
        message_window.geometry("300x100")
        
        ctk.CTkLabel(
            message_window,
            text=message,
            text_color="green" if success else "red"
        ).pack(pady=20)
        
    def add_site(self):
        """Adiciona um novo site à lista de bloqueios."""
        site = self.site_entry.get().strip()
        category = self.category_combobox.get()
        
        if site:
            success, message = self.blocker.add_site(site, category)
            
            if success:
                self.site_entry.delete(0, 'end')
                self.refresh_sites_list()
                
            # Mostrar mensagem
            message_window = ctk.CTkToplevel(self)
            message_window.title("Resultado")
            message_window.geometry("300x100")
            
            ctk.CTkLabel(
                message_window,
                text=message,
                text_color="green" if success else "red"
            ).pack(pady=20)
            
    def remove_site(self, site: str, category: str):
        """Remove um site da lista de bloqueios."""
        success, message = self.blocker.remove_site(site, category)
        
        if success:
            self.refresh_sites_list()
            
        # Mostrar mensagem
        message_window = ctk.CTkToplevel(self)
        message_window.title("Resultado")
        message_window.geometry("300x100")
        
        ctk.CTkLabel(
            message_window,
            text=message,
            text_color="green" if success else "red"
        ).pack(pady=20)
        
    def refresh_sites_list(self):
        """Atualiza a lista de sites."""
        # Recriar a interface
        self.destroy()
        self.__init__(self.parent) 