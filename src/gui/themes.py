from PySide6.QtGui import QPixmap
import os

class ThemeManager:
    THEMES = {
        'dark': {
            'primary': '#1a1b26',      # Fundo principal (azul escuro)
            'secondary': '#24283b',    # Elementos secundários
            'accent': '#7aa2f7',       # Destaque (azul claro)
            'text': '#c0caf5',         # Texto principal
            'text_secondary': '#565f89', # Texto secundário
            'success': '#9ece6a',      # Verde para sucesso
            'warning': '#e0af68',      # Amarelo para avisos
            'error': '#f7768e',        # Vermelho para erros
            'button': '#414868',       # Botões normais
            'button_hover': '#565f89'  # Hover dos botões
        },
        'light': {
            'primary': '#ffffff',
            'secondary': '#f0f0f0',
            'accent': '#2d4f67',
            'text': '#1a1b26',
            'text_secondary': '#4e5173',
            'success': '#4d9375',
            'warning': '#c98a1b',
            'error': '#f7768e',
            'button': '#e1e2e6',
            'button_hover': '#d0d1d5'
        }
    }

    @staticmethod
    def get_button_style(theme: str = 'dark') -> dict:
        """Retorna o estilo padrão para botões."""
        theme_colors = ThemeManager.THEMES[theme]
        return {
            'fg_color': theme_colors['button'],
            'hover_color': theme_colors['button_hover'],
            'text_color': theme_colors['text'],
            'corner_radius': 8,
            'border_width': 0,
            'font': ('Roboto', 12)
        }

    @staticmethod
    def get_frame_style(theme: str = 'dark') -> dict:
        """Retorna o estilo padrão para frames."""
        theme_colors = ThemeManager.THEMES[theme]
        return {
            'fg_color': theme_colors['secondary'],
            'corner_radius': 10,
            'border_width': 0
        }

class Theme:
    def __init__(self):
        # Cores do tema Logan Study Style - Matemática em Evidência
        self.colors = {
            'bg_dark': '#1e2124',      # Cinza escuro
            'bg_darker': '#16181a',     # Cinza mais escuro
            'bg_light': '#282b30',      # Cinza médio
            'bg_lighter': '#36393f',    # Cinza mais claro (nova cor)
            'fg': '#ffffff',            # Branco
            'accent': '#4169E1',        # Azul royal (cor principal)
            'success': '#43b581',       # Verde suave
            'warning': '#faa61a',       # Laranja
            'error': '#ed4245',         # Vermelho suave
            'secondary': '#7289da'      # Azul secundário
        }
        
        # Debug da estrutura de diretórios
        self._check_directory_structure()
        
        # Carregar recursos
        self.logo = self._load_logo()
        
    def _load_logo(self) -> QPixmap:
        """Carrega a logo do aplicativo."""
        # Obter o diretório do arquivo atual (themes.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construir o caminho correto para a logo
        logo_path = os.path.join(current_dir, '..', 'img', 'logo.png')
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                print(f"Logo carregada com sucesso de: {logo_path}")
                return pixmap
            else:
                print(f"Falha ao carregar logo de: {logo_path}")
        else:
            print(f"Arquivo de logo não encontrado em: {logo_path}")
        
        return None

    def _check_directory_structure(self):
        """Verifica e imprime a estrutura de diretórios para debug."""
        current_dir = os.getcwd()
        print(f"Diretório atual: {current_dir}")
        print(f"Conteúdo do diretório:")
        for root, dirs, files in os.walk(current_dir):
            level = root.replace(current_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")

    def get_main_style(self):
        return f"""
            /* Títulos e Textos */
            #pageTitle {{
                color: {self.colors['fg']};
                font-size: 24px;
                font-weight: bold;
            }}
            
            #pageDescription {{
                color: {self.colors['fg']};
                font-size: 14px;
                opacity: 0.8;
            }}
            
            #sectionTitle {{
                color: {self.colors['fg']};
                font-size: 18px;
                font-weight: bold;
            }}
            
            /* Cards e Seções */
            #sectionCard {{
                background: {self.colors['bg_darker']};
                border-radius: 12px;
                padding: 20px;
                margin: 5px 0;
            }}
            
            #helpCard {{
                background: rgba(0, 0, 0, 0.2);
                border-radius: 12px;
                padding: 20px;
                margin: 5px 0;
            }}
            
            #subjectCard {{
                background: {self.colors['bg_darker']};
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
            }}
            
            /* Tabela */
            #subjectsTable {{
                background: transparent;
                border: none;
                gridline-color: rgba(255, 255, 255, 0.1);
            }}
            
            #subjectsTable::item {{
                padding: 8px;
                color: {self.colors['fg']};
            }}
            
            #subjectsTable::header {{
                background: {self.colors['bg_light']};
                padding: 8px;
                border: none;
            }}
            
            /* Botões */
            #primaryButton {{
                background: {self.colors['accent']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }}
            
            #primaryButton:hover {{
                background: {self.colors['secondary']};
            }}
            
            #accentButton {{
                background: linear-gradient(45deg, {self.colors['accent']}, {self.colors['secondary']});
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }}
            
            /* Elementos do Card */
            #cardTitle {{
                color: {self.colors['fg']};
                font-size: 16px;
                font-weight: bold;
            }}
            
            #hoursLabel {{
                color: {self.colors['accent']};
                font-size: 16px;
                font-weight: bold;
            }}
            
            #studyBox {{
                background-color: {self.colors['bg_light']};
                border: 2px solid {self.colors['accent']};
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
                min-width: 30px;
                min-height: 30px;
                max-width: 30px;
                max-height: 30px;
            }}
            
            #studyBox:checked {{
                background-color: {self.colors['accent']};
            }}
            
            #hourLabel {{
                color: {self.colors['fg']};
                font-size: 12px;
                opacity: 0.8;
                margin-top: 5px;
            }}
            
            #helpText {{
                color: {self.colors['fg']};
                font-size: 14px;
                line-height: 1.6;
                opacity: 0.9;
            }}
        """ 

class DynamicTheme(Theme):
    """Tema dinâmico que pode mudar em tempo de execução."""
    
    def __init__(self):
        super().__init__()
        self.active_theme = 'default'
        self.themes = {
            'default': {
                'bg_dark': '#1e2124',
                'bg_darker': '#16181a',
                'bg_light': '#282b30',
                'bg_lighter': '#36393f',
                'fg': '#ffffff',
                'accent': '#4169E1',
                'success': '#43b581',
                'warning': '#faa61a',
                'error': '#ed4245',
                'secondary': '#7289da'
            },
            'purple': {
                'bg_dark': '#292341',
                'bg_darker': '#221C36',
                'bg_light': '#362C51',
                'bg_lighter': '#42356B',
                'fg': '#ffffff',
                'accent': '#9B59B6',
                'success': '#2ECC71',
                'warning': '#F39C12',
                'error': '#E74C3C',
                'secondary': '#5D6DBE'
            },
            'ocean': {
                'bg_dark': '#1A2530',
                'bg_darker': '#0F1924',
                'bg_light': '#253545',
                'bg_lighter': '#34495E',
                'fg': '#ECF0F1',
                'accent': '#3498DB',
                'success': '#1ABC9C',
                'warning': '#F1C40F',
                'error': '#E74C3C',
                'secondary': '#2980B9'
            },
            'light': {
                'bg_dark': '#F5F5F5',
                'bg_darker': '#E0E0E0',
                'bg_light': '#FAFAFA',
                'bg_lighter': '#FFFFFF',
                'fg': '#333333',
                'accent': '#3F51B5',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336',
                'secondary': '#2196F3'
            }
        }
        
    def set_theme(self, theme_name):
        """Altera o tema ativo."""
        if theme_name in self.themes:
            self.active_theme = theme_name
            self.colors = self.themes[theme_name]
            return True
        return False
    
    def get_current_theme(self):
        """Retorna o nome do tema atual."""
        return self.active_theme
    
    def get_available_themes(self):
        """Retorna uma lista com os temas disponíveis."""
        return list(self.themes.keys())
    
    def add_custom_theme(self, name, colors):
        """Adiciona um tema personalizado."""
        if all(key in colors for key in self.themes['default'].keys()):
            self.themes[name] = colors
            return True
        return False 