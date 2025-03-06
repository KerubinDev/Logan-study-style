from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
import os
from src.database.database import get_data_dir

class ThemeEditorDialog(QDialog):
    """Diálogo para edição de temas personalizados."""
    
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_theme = theme_manager.get_current_theme()
        self.theme_colors = theme_manager.colors.copy()
        
        self.setWindowTitle("Editor de Temas")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Cabeçalho
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Editor de Temas")
        title.setObjectName("dialogTitle")
        header_layout.addWidget(title)
        
        theme_selector = QComboBox()
        theme_selector.addItems(self.theme_manager.get_available_themes())
        theme_selector.setCurrentText(self.current_theme)
        theme_selector.currentTextChanged.connect(self.change_theme)
        header_layout.addWidget(theme_selector)
        
        main_layout.addWidget(header)
        
        # Área de edição
        editor_area = QSplitter()
        
        # Painel de cores
        color_panel = QFrame()
        color_panel.setObjectName("editorPanel")
        color_layout = QVBoxLayout(color_panel)
        
        color_form = QFormLayout()
        self.color_pickers = {}
        
        for color_name, color_value in self.theme_colors.items():
            label = QLabel(color_name)
            picker = QColorDialog.getColor(QColor(color_value))
            picker_btn = QPushButton()
            picker_btn.setStyleSheet(f"background-color: {color_value}; min-width: 100px; min-height: 30px;")
            picker_btn.clicked.connect(lambda checked=False, name=color_name: self.pick_color(name))
            
            self.color_pickers[color_name] = {
                'button': picker_btn,
                'color': color_value
            }
            
            color_form.addRow(label, picker_btn)
        
        color_layout.addLayout(color_form)
        
        # Botões de salvar/exportar/importar
        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        
        save_as_btn = QPushButton("Salvar como")
        save_as_btn.clicked.connect(self.save_as_theme)
        buttons_layout.addWidget(save_as_btn)
        
        export_btn = QPushButton("Exportar tema")
        export_btn.clicked.connect(self.export_theme)
        buttons_layout.addWidget(export_btn)
        
        import_btn = QPushButton("Importar tema")
        import_btn.clicked.connect(self.import_theme)
        buttons_layout.addWidget(import_btn)
        
        color_layout.addWidget(buttons)
        
        # Painel de visualização
        preview_panel = QFrame()
        preview_panel.setObjectName("previewPanel")
        preview_layout = QVBoxLayout(preview_panel)
        
        preview_title = QLabel("Visualização do Tema")
        preview_title.setObjectName("previewTitle")
        preview_layout.addWidget(preview_title)
        
        # Conteúdo de visualização
        preview_content = QWidget()
        preview_content.setObjectName("previewContent")
        preview_content_layout = QVBoxLayout(preview_content)
        
        # Adicionar elementos de exemplo
        card = QFrame()
        card.setObjectName("previewCard")
        card_layout = QVBoxLayout(card)
        
        card_title = QLabel("Exemplo de Card")
        card_title.setObjectName("cardTitle")
        card_layout.addWidget(card_title)
        
        card_content = QLabel("Este é um exemplo de conteúdo em um card, usando as cores do tema selecionado.")
        card_content.setWordWrap(True)
        card_layout.addWidget(card_content)
        
        preview_content_layout.addWidget(card)
        
        # Exemplo de botões
        buttons_example = QWidget()
        buttons_example_layout = QHBoxLayout(buttons_example)
        
        primary_btn = QPushButton("Botão Primário")
        primary_btn.setObjectName("primaryButton")
        buttons_example_layout.addWidget(primary_btn)
        
        secondary_btn = QPushButton("Botão Secundário")
        secondary_btn.setObjectName("secondaryButton")
        buttons_example_layout.addWidget(secondary_btn)
        
        accent_btn = QPushButton("Botão Accent")
        accent_btn.setObjectName("accentButton")
        buttons_example_layout.addWidget(accent_btn)
        
        preview_content_layout.addWidget(buttons_example)
        
        # Exemplo de checkbox
        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)
        
        for i in range(3):
            checkbox = QCheckBox()
            checkbox.setObjectName("studyBox")
            if i == 1:
                checkbox.setChecked(True)
            checkbox_layout.addWidget(checkbox)
        
        preview_content_layout.addWidget(checkbox_container)
        
        preview_layout.addWidget(preview_content)
        
        # Adicionar painéis ao splitter
        editor_area.addWidget(color_panel)
        editor_area.addWidget(preview_panel)
        editor_area.setSizes([300, 500])
        
        main_layout.addWidget(editor_area)
        
        # Botões de diálogo
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        main_layout.addWidget(dialog_buttons)
        
        # Atualizar preview
        self.update_preview()
    
    def pick_color(self, color_name):
        """Abre o seletor de cores para um campo específico."""
        current_color = QColor(self.color_pickers[color_name]['color'])
        color = QColorDialog.getColor(current_color, self)
        
        if color.isValid():
            self.color_pickers[color_name]['color'] = color.name()
            self.color_pickers[color_name]['button'].setStyleSheet(
                f"background-color: {color.name()}; min-width: 100px; min-height: 30px;"
            )
            self.theme_colors[color_name] = color.name()
            self.update_preview()
    
    def update_preview(self):
        """Atualiza a visualização do tema."""
        style = self.generate_preview_style()
        self.findChild(QWidget, "previewContent").setStyleSheet(style)
    
    def generate_preview_style(self):
        """Gera o CSS para o preview com as cores atuais."""
        return f"""
            #previewContent {{
                background-color: {self.theme_colors['bg_dark']};
                padding: 20px;
                border-radius: 10px;
            }}
            
            #previewCard {{
                background-color: {self.theme_colors['bg_darker']};
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }}
            
            #cardTitle {{
                color: {self.theme_colors['fg']};
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            QLabel {{
                color: {self.theme_colors['fg']};
            }}
            
            #primaryButton {{
                background-color: {self.theme_colors['accent']};
                color: {self.theme_colors['fg']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            
            #secondaryButton {{
                background-color: {self.theme_colors['bg_light']};
                color: {self.theme_colors['fg']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            
            #accentButton {{
                background-color: {self.theme_colors['secondary']};
                color: {self.theme_colors['fg']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }}
            
            #studyBox {{
                background-color: {self.theme_colors['bg_light']};
                border: 2px solid {self.theme_colors['accent']};
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
                min-width: 30px;
                min-height: 30px;
                max-width: 30px;
                max-height: 30px;
            }}
            
            #studyBox:checked {{
                background-color: {self.theme_colors['accent']};
            }}
        """
    
    def change_theme(self, theme_name):
        """Muda para outro tema existente."""
        if theme_name in self.theme_manager.themes:
            self.current_theme = theme_name
            self.theme_colors = self.theme_manager.themes[theme_name].copy()
            
            # Atualizar botões de cores
            for color_name, color_value in self.theme_colors.items():
                self.color_pickers[color_name]['color'] = color_value
                self.color_pickers[color_name]['button'].setStyleSheet(
                    f"background-color: {color_value}; min-width: 100px; min-height: 30px;"
                )
            
            self.update_preview()
    
    def save_as_theme(self):
        """Salva como um novo tema personalizado."""
        name, ok = QInputDialog.getText(
            self, "Salvar Tema", "Nome do novo tema:", 
            QLineEdit.Normal, f"{self.current_theme}_custom"
        )
        
        if ok and name:
            # Verificar se já existe
            if name in self.theme_manager.themes:
                confirm = QMessageBox.question(
                    self, "Sobrescrever Tema", 
                    f"O tema '{name}' já existe. Deseja sobrescrevê-lo?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if confirm != QMessageBox.Yes:
                    return
            
            # Salvar o tema
            self.theme_manager.add_custom_theme(name, self.theme_colors.copy())
            
            # Salvar em arquivo
            self.save_theme_to_file(name, self.theme_colors)
            
            QMessageBox.information(
                self, "Tema Salvo", 
                f"O tema '{name}' foi salvo com sucesso!"
            )
    
    def export_theme(self):
        """Exporta o tema atual para um arquivo JSON."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Tema", "", "JSON Files (*.json)"
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump({
                    'name': self.current_theme,
                    'colors': self.theme_colors
                }, f, indent=4)
            
            QMessageBox.information(
                self, "Tema Exportado", 
                f"O tema foi exportado para:\n{file_path}"
            )
    
    def import_theme(self):
        """Importa um tema de um arquivo JSON."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importar Tema", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    theme_data = json.load(f)
                
                if 'name' in theme_data and 'colors' in theme_data:
                    name = theme_data['name']
                    colors = theme_data['colors']
                    
                    # Verificar se tem todas as cores necessárias
                    if all(key in colors for key in self.theme_manager.themes['default'].keys()):
                        self.theme_manager.add_custom_theme(name, colors)
                        self.save_theme_to_file(name, colors)
                        
                        # Atualizar seletor de temas
                        combo = self.findChild(QComboBox)
                        if combo:
                            combo.blockSignals(True)
                            combo.clear()
                            combo.addItems(self.theme_manager.get_available_themes())
                            combo.setCurrentText(name)
                            combo.blockSignals(False)
                        
                        # Aplicar o tema importado
                        self.change_theme(name)
                        
                        QMessageBox.information(
                            self, "Tema Importado", 
                            f"O tema '{name}' foi importado com sucesso!"
                        )
                    else:
                        QMessageBox.warning(
                            self, "Erro de Importação", 
                            "O arquivo não contém todas as cores necessárias para um tema válido."
                        )
                else:
                    QMessageBox.warning(
                        self, "Erro de Importação", 
                        "O arquivo não está no formato correto."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Erro de Importação", 
                    f"Ocorreu um erro ao importar o tema:\n{str(e)}"
                )
    
    def save_theme_to_file(self, name, colors):
        """Salva o tema em um arquivo no diretório de dados."""
        themes_dir = os.path.join(get_data_dir(), 'themes')
        os.makedirs(themes_dir, exist_ok=True)
        
        file_path = os.path.join(themes_dir, f"{name}.json")
        with open(file_path, 'w') as f:
            json.dump(colors, f, indent=4)
    
    def accept(self):
        """Aplica o tema atual e fecha o diálogo."""
        # Verificar se é um tema existente ou um novo
        if self.current_theme in self.theme_manager.themes:
            # Se for personalizado, atualiza as cores
            self.theme_manager.themes[self.current_theme] = self.theme_colors.copy()
        else:
            # Se não existir, cria um novo
            self.theme_manager.add_custom_theme(f"{self.current_theme}_modified", self.theme_colors.copy())
            self.current_theme = f"{self.current_theme}_modified"
        
        # Ativar o tema
        self.theme_manager.set_theme(self.current_theme)
        
        super().accept() 