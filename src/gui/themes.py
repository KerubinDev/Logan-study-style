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
        # Cores do tema Tokyo Night
        self.colors = {
            'bg_dark': '#1a1b26',
            'bg_darker': '#16161e',
            'bg_light': '#24283b',
            'fg': '#c0caf5',
            'accent': '#7aa2f7',
            'success': '#9ece6a',
            'warning': '#e0af68',
            'error': '#f7768e'
        }
        
    def get_main_style(self):
        return f"""
            QMainWindow {{
                background-color: {self.colors['bg_dark']};
            }}
            
            #sidebar {{
                background-color: {self.colors['bg_darker']};
                border: none;
            }}
            
            #logoWidget {{
                padding: 20px;
                background-color: {self.colors['bg_darker']};
            }}
            
            #logoTitle {{
                color: {self.colors['accent']};
                font-size: 32px;
                font-weight: bold;
            }}
            
            #logoSubtitle {{
                color: {self.colors['fg']};
                font-size: 16px;
            }}
            
            #navButton {{
                background-color: transparent;
                color: {self.colors['fg']};
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                border-radius: 8px;
                margin: 2px 10px;
            }}
            
            #navButton:hover {{
                background-color: {self.colors['bg_light']};
            }}
            
            #contentArea {{
                background-color: {self.colors['bg_dark']};
            }}
            
            QLabel {{
                color: {self.colors['fg']};
            }}
            
            QPushButton {{
                background-color: {self.colors['accent']};
                color: {self.colors['bg_dark']};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['bg_light']};
                color: {self.colors['accent']};
            }}
            
            QFrame#card {{
                background-color: {self.colors['bg_light']};
                border-radius: 10px;
                padding: 20px;
            }}
            
            #input {{
                background-color: {self.colors['bg_light']};
                color: {self.colors['fg']};
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
            }}
            
            #input:focus {{
                border: 2px solid {self.colors['accent']};
            }}
            
            #primaryButton {{
                background-color: {self.colors['accent']};
                color: {self.colors['bg_dark']};
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            
            #linkButton {{
                background-color: transparent;
                color: {self.colors['accent']};
                border: none;
                padding: 8px;
                font-size: 12px;
            }}
        """ 