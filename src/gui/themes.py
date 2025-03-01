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
            QMainWindow {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.colors['bg_dark']},
                    stop: 1 {self.colors['bg_darker']}
                );
            }}
            
            /* Sidebar */
            #sidebar {{
                background-color: rgba(22, 24, 26, 0.95);
                border-right: 1px solid rgba(40, 43, 48, 0.5);
                min-width: 250px;
                padding: 20px 0;
            }}
            
            /* Logo */
            #sidebarLogoImage {{
                border: 3px solid {self.colors['accent']};
                border-radius: 60px;
                padding: 3px;
                margin: 10px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.colors['bg_dark']},
                    stop: 1 {self.colors['bg_darker']}
                );
            }}
            
            /* Botões de Navegação */
            #navButton {{
                background-color: transparent;
                color: {self.colors['fg']};
                border: none;
                padding: 15px 25px;
                text-align: left;
                font-size: 14px;
                border-radius: 12px;
                margin: 5px 15px;
                font-weight: 500;
            }}
            
            #navButton:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(65, 105, 225, 0.1),
                    stop: 1 rgba(65, 105, 225, 0.2)
                );
                color: {self.colors['accent']};
                padding-left: 35px;
            }}
            
            /* Timer Display */
            #timerLabel {{
                color: {self.colors['fg']};
                font-size: 82px;
                font-weight: bold;
                padding: 40px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.colors['bg_darker']},
                    stop: 1 rgba(22, 24, 26, 0.95)
                );
                border-radius: 25px;
                border: 1px solid rgba(65, 105, 225, 0.3);
            }}
            
            /* Botões do Timer */
            #startButton, #pauseButton, #resetButton {{
                padding: 15px 35px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
                min-width: 140px;
            }}
            
            #startButton {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {self.colors['accent']},
                    stop: 1 {self.colors['secondary']}
                );
                color: white;
                border: none;
            }}
            
            #startButton:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {self.colors['secondary']},
                    stop: 1 {self.colors['accent']}
                );
            }}
            
            #pauseButton {{
                background-color: rgba(22, 24, 26, 0.95);
                color: {self.colors['fg']};
                border: 2px solid {self.colors['accent']};
            }}
            
            #pauseButton:hover {{
                background-color: rgba(65, 105, 225, 0.1);
                border-color: {self.colors['secondary']};
            }}
            
            #resetButton {{
                background-color: rgba(237, 66, 69, 0.1);
                color: {self.colors['error']};
                border: 2px solid {self.colors['error']};
            }}
            
            #resetButton:hover {{
                background-color: {self.colors['error']};
                color: white;
            }}
            
            /* Cards */
            QFrame#card {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {self.colors['bg_darker']},
                    stop: 1 rgba(22, 24, 26, 0.95)
                );
                border-radius: 15px;
                padding: 25px;
                border: 1px solid rgba(65, 105, 225, 0.2);
            }}
            
            QFrame#card:hover {{
                border: 1px solid {self.colors['accent']};
            }}
            
            /* Estatísticas */
            #statTitle {{
                color: {self.colors['fg']};
                font-size: 16px;
                opacity: 0.8;
                font-weight: 500;
                margin-bottom: 5px;
            }}
            
            #statValue {{
                color: {self.colors['fg']};
                font-size: 36px;
                font-weight: bold;
            }}
            
            /* Lista de Tarefas */
            #taskCheckbox {{
                color: {self.colors['fg']};
                font-size: 15px;
                padding: 12px;
                spacing: 10px;
                border-radius: 8px;
                background: transparent;
            }}
            
            #taskCheckbox:hover {{
                color: {self.colors['accent']};
                background: rgba(65, 105, 225, 0.1);
                padding-left: 20px;
            }}
            
            /* Botões de Ação */
            #actionButton {{
                background: rgba(65, 105, 225, 0.1);
                color: {self.colors['fg']};
                border: 1px solid rgba(65, 105, 225, 0.3);
                padding: 12px 25px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 500;
            }}
            
            #actionButton:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {self.colors['accent']},
                    stop: 1 {self.colors['secondary']}
                );
                color: white;
                border: none;
            }}
            
            /* Área de Conteúdo */
            #contentArea {{
                background: transparent;
                padding: 30px;
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                border: none;
                background: {self.colors['bg_darker']};
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }}
            
            QScrollBar::handle:vertical {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {self.colors['accent']},
                    stop: 1 {self.colors['secondary']}
                );
                border-radius: 5px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 {self.colors['secondary']},
                    stop: 1 {self.colors['accent']}
                );
            }}
            
            /* Input Fields */
            QLineEdit {{
                background-color: rgba(22, 24, 26, 0.95);
                color: {self.colors['fg']};
                border: 1px solid rgba(65, 105, 225, 0.3);
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
                selection-background-color: {self.colors['accent']};
            }}
            
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent']};
                background-color: rgba(22, 24, 26, 0.98);
            }}
            
            /* Tooltips */
            QToolTip {{
                background-color: {self.colors['bg_darker']};
                color: {self.colors['fg']};
                border: 1px solid {self.colors['accent']};
                padding: 5px;
                border-radius: 4px;
                opacity: 200;
            }}
        """ 