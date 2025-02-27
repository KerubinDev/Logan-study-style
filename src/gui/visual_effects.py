import customtkinter as ctk
from src.utils.asset_manager import AssetManager

class AnimeVisualEffects:
    def __init__(self):
        self.asset_manager = AssetManager()
        
    def create_icon_button(self, parent: ctk.CTk, icon_name: str, 
                          command=None, text: str = "") -> ctk.CTkButton:
        """Cria um botão com emoji."""
        emoji = self.asset_manager.get_emoji(icon_name)
        
        return ctk.CTkButton(
            parent,
            text=f"{emoji} {text}",
            command=command,
            compound="left"
        )
        
    def apply_anime_style(self, window: ctk.CTk):
        """Aplica estilo visual à janela."""
        pass
        
    def show_level_up_animation(self, window: ctk.CTk, level: int):
        """Mostra uma notificação de level up."""
        popup = ctk.CTkToplevel(window)
        popup.title("Level Up!")
        popup.geometry("300x150")
        
        ctk.CTkLabel(
            popup,
            text=f"⭐ LEVEL UP! ⭐\nNível {level}",
            font=("Roboto", 24, "bold")
        ).pack(pady=20)
        
        # Fechar automaticamente após 3 segundos
        window.after(3000, popup.destroy)
        
    def show_achievement_popup(self, window: ctk.CTk, achievement_name: str):
        """Mostra um popup de conquista."""
        popup = ctk.CTkToplevel(window)
        popup.title("Nova Conquista!")
        popup.geometry("300x100")
        
        ctk.CTkLabel(
            popup,
            text=f"🏆 {achievement_name}",
            font=("Roboto", 16, "bold")
        ).pack(pady=20)
        
        # Fechar automaticamente após 3 segundos
        window.after(3000, popup.destroy) 