from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QLineEdit, QComboBox, QFrame, QWidget, QMessageBox)
from PySide6.QtCore import Qt
from src.services.distraction_blocker import DistractionBlocker
from typing import Dict, List
import json

class DistractionManagerWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.user_id = parent.user_id
        self.setWindowTitle("Gerenciador de Distrações")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        
        # Serviço de bloqueio
        self.blocker = DistractionBlocker()
        
        self.create_header()
        self.create_control_frame()
        self.create_sites_manager()
        
        # Atualizar estado inicial
        self.update_status()
        
    def create_header(self):
        """Cria o cabeçalho com título e status."""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("Bloqueio de Distrações")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        header_layout.addWidget(title)
        
        description = QLabel("Gerencie sites que podem atrapalhar sua produtividade")
        description.setStyleSheet("font-size: 12pt;")
        header_layout.addWidget(description)
        
        self.main_layout.addWidget(header_frame)
        
    def create_control_frame(self):
        """Cria o frame com controles de bloqueio."""
        control_frame = QFrame()
        control_layout = QVBoxLayout(control_frame)
        
        # Status atual
        self.status_label = QLabel("Status: Inativo")
        self.status_label.setStyleSheet("font-size: 16pt;")
        control_layout.addWidget(self.status_label)
        
        # Botões de controle
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        
        self.start_button = QPushButton("Ativar Bloqueio")
        self.start_button.clicked.connect(self.toggle_blocking)
        buttons_layout.addWidget(self.start_button)
        
        control_layout.addWidget(buttons_frame)
        self.main_layout.addWidget(control_frame)
        
    def create_sites_manager(self):
        """Cria o gerenciador de sites bloqueados."""
        sites_frame = QFrame()
        sites_layout = QVBoxLayout(sites_frame)
        
        # Frame de adição
        add_frame = QFrame()
        add_layout = QHBoxLayout(add_frame)
        
        add_layout.addWidget(QLabel("Adicionar Site:"))
        
        self.site_entry = QLineEdit()
        self.site_entry.setFixedWidth(200)
        add_layout.addWidget(self.site_entry)
        
        self.category_combobox = QComboBox()
        self.category_combobox.addItems(["Redes Sociais", "Entretenimento", "Jogos"])
        add_layout.addWidget(self.category_combobox)
        
        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_site)
        add_layout.addWidget(add_button)
        
        sites_layout.addWidget(add_frame)
        
        # Lista de sites
        self.sites_list = QFrame()
        sites_list_layout = QVBoxLayout(self.sites_list)
        sites_layout.addWidget(self.sites_list)
        
        self.main_layout.addWidget(sites_frame)
        self.refresh_sites_list()
        
    def toggle_blocking(self):
        """Alterna o estado do bloqueio."""
        if self.blocker.is_active:
            success = self.blocker.stop_blocking()
        else:
            success = self.blocker.start_blocking()
            
        if success:
            is_active = self.blocker.is_active
            self.status_label.setText(f"Status: {'Ativo' if is_active else 'Inativo'}")
            self.start_button.setText("Desativar Bloqueio" if is_active else "Ativar Bloqueio")
            
            QMessageBox.information(
                self,
                "Sucesso",
                f"Bloqueio {'ativado' if is_active else 'desativado'} com sucesso!"
            )
        else:
            QMessageBox.warning(
                self,
                "Erro",
                "Não foi possível alterar o estado do bloqueio."
            )
            
    def add_site(self):
        """Adiciona um novo site à lista de bloqueios."""
        site = self.site_entry.text().strip()
        category = self.category_combobox.currentText()
        
        if site:
            success = self.blocker.add_site(site, category)
            
            if success:
                self.site_entry.clear()
                self.refresh_sites_list()
                QMessageBox.information(self, "Sucesso", "Site adicionado com sucesso!")
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível adicionar o site.")
            
    def remove_site(self, site: str, category: str):
        """Remove um site da lista de bloqueios."""
        success, message = self.blocker.remove_site(site, category)
        
        if success:
            self.refresh_sites_list()
            
        # Mostrar mensagem
        message_window = QDialog(self)
        message_window.setWindowTitle("Resultado")
        message_window.setGeometry(300, 100)
        
        message_label = QLabel(message)
        message_label.setStyleSheet("color: green;" if success else "color: red;")
        message_window.layout().addWidget(message_label)
        
    def refresh_sites_list(self):
        """Atualiza a lista de sites."""
        # Limpar lista atual
        for i in reversed(range(self.sites_list.layout().count())):
            widget = self.sites_list.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Adicionar sites atualizados
        for category, sites in self.blocker.get_sites().items():
            category_label = QLabel(category)
            category_label.setStyleSheet("font-weight: bold;")
            self.sites_list.layout().addWidget(category_label)
            
            for site in sites:
                site_frame = QFrame()
                site_layout = QHBoxLayout(site_frame)
                
                site_label = QLabel(site)
                site_layout.addWidget(site_label)
                
                remove_btn = QPushButton("Remover")
                remove_btn.clicked.connect(lambda s=site, c=category: self.remove_site(s, c))
                site_layout.addWidget(remove_btn)
                
                self.sites_list.layout().addWidget(site_frame)
        
    def update_status(self):
        """Atualiza o status visual do bloqueio."""
        is_active = self.blocker.is_active
        self.status_label.setText(f"Status: {'Ativo' if is_active else 'Inativo'}")
        self.start_button.setText("Desativar Bloqueio" if is_active else "Ativar Bloqueio") 