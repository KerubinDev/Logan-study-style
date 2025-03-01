from PySide6.QtWidgets import QMessageBox

class SimpleEffects:
    """Classe simplificada para notificações básicas"""
    
    @staticmethod
    def show_level_up(level: int):
        """Mostra uma mensagem simples de level up."""
        QMessageBox.information(
            None,
            "Novo Nível!",
            f"Parabéns! Você alcançou o nível {level}!"
        )
    
    @staticmethod
    def show_achievement(achievement_name: str):
        """Mostra uma mensagem simples de conquista."""
        QMessageBox.information(
            None,
            "Nova Conquista!",
            f"Parabéns! Você conquistou: {achievement_name}"
        ) 