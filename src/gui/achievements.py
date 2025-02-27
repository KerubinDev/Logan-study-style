import customtkinter as ctk
from PIL import Image, ImageTk
import os
from src.services.achievement_manager import AchievementManager

class AchievementsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user_id = parent.user_id
        self.theme = parent.theme
        
        # Configuração da janela
        self.title("Conquistas e Nível")
        self.geometry("800x600")
        
        # Gerenciador de conquistas
        self.achievement_manager = AchievementManager(self.user_id)
        
        # Layout
        self.create_level_frame()
        self.create_achievements_list()
        
    def create_level_frame(self):
        """Cria o frame com informações de nível e XP."""
        level_frame = ctk.CTkFrame(self)
        level_frame.pack(fill="x", padx=20, pady=20)
        
        # Buscar progresso
        progress = self.achievement_manager.get_user_progress()
        
        # Nível atual
        level_label = ctk.CTkLabel(
            level_frame,
            text=f"Nível {progress['level']}",
            font=("Roboto", 32, "bold"),
            text_color=self.theme['accent']
        )
        level_label.pack(pady=10)
        
        # Barra de progresso
        progress_bar = ctk.CTkProgressBar(level_frame)
        progress_bar.pack(fill="x", padx=50, pady=10)
        progress_bar.set(progress['progress'] / 100)
        
        # XP atual/próximo nível
        xp_label = ctk.CTkLabel(
            level_frame,
            text=f"XP: {progress['current_xp']}/{progress['next_level_xp']}",
            font=("Roboto", 14)
        )
        xp_label.pack(pady=5)
        
        # XP total
        total_xp_label = ctk.CTkLabel(
            level_frame,
            text=f"XP Total: {progress['total_xp']}",
            font=("Roboto", 12)
        )
        total_xp_label.pack(pady=5)
        
    def create_achievements_list(self):
        """Cria a lista de conquistas."""
        # Frame principal das conquistas
        achievements_frame = ctk.CTkScrollableFrame(self)
        achievements_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            achievements_frame,
            text="Conquistas Recentes",
            font=("Roboto", 20, "bold")
        )
        title.pack(pady=10)
        
        # Buscar conquistas recentes
        recent_achievements = self.achievement_manager.get_recent_achievements()
        
        for user_achievement in recent_achievements:
            achievement = user_achievement.achievement
            
            # Frame da conquista
            achievement_frame = ctk.CTkFrame(achievements_frame)
            achievement_frame.pack(fill="x", pady=5)
            
            # Ícone (se existir)
            if achievement.icon_path and os.path.exists(achievement.icon_path):
                icon = Image.open(achievement.icon_path)
                icon = ImageTk.PhotoImage(icon.resize((32, 32)))
                
                icon_label = ctk.CTkLabel(
                    achievement_frame,
                    image=icon,
                    text=""
                )
                icon_label.image = icon  # Manter referência
                icon_label.pack(side="left", padx=10)
            
            # Informações da conquista
            info_frame = ctk.CTkFrame(achievement_frame)
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            
            ctk.CTkLabel(
                info_frame,
                text=achievement.name,
                font=("Roboto", 14, "bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=achievement.description,
                font=("Roboto", 12)
            ).pack(anchor="w")
            
            # Data de conquista
            earned_date = user_achievement.earned_at.strftime("%d/%m/%Y")
            ctk.CTkLabel(
                achievement_frame,
                text=earned_date,
                font=("Roboto", 12)
            ).pack(side="right", padx=10) 