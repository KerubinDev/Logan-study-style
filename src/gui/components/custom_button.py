import customtkinter as ctk
from src.gui.themes import ThemeManager

class ModernButton(ctk.CTkButton):
    def __init__(self, *args, icon_name=None, theme='dark', **kwargs):
        # Aplicar estilo padrão
        button_style = ThemeManager.get_button_style(theme)
        kwargs.update(button_style)
        
        # Configurar texto com emoji
        if icon_name:
            from src.utils.asset_manager import AssetManager
            asset_manager = AssetManager()
            emoji = asset_manager.get_emoji(icon_name)
            if 'text' in kwargs:
                kwargs['text'] = f"{emoji} {kwargs['text']}"
            else:
                kwargs['text'] = emoji
                
        super().__init__(*args, **kwargs)
        
        # Adicionar efeito hover
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        
    def _on_enter(self, e):
        """Efeito ao passar o mouse."""
        self.configure(scale_factor=1.05)
        
    def _on_leave(self, e):
        """Efeito ao remover o mouse."""
        self.configure(scale_factor=1.0) 