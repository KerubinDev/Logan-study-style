import os
import requests
import base64
from PIL import Image
from io import BytesIO
from pathlib import Path
import json
import customtkinter as ctk

class AssetManager:
    def __init__(self):
        # Emojis para cada tipo de ícone
        self.emojis = {
            "home": "🏠",
            "tasks": "📝",
            "stats": "📊",
            "settings": "⚙️",
            "calendar": "📅",
            "block": "🚫",
            "timer": "⏰",
            "add": "➕",
            "delete": "🗑️",
            "sync": "🔄",
            "save": "💾",
            "cancel": "❌",
            "edit": "✏️",
            "complete": "✅",
            "pause": "⏸️",
            "play": "▶️",
            "stop": "⏹️",
            "reset": "🔄",
            "level": "📚",
            "achievement": "🎯",
            "exit": "🚪",
            "study": "✏️",
            "focus": "🧮",
            "math": "➗",
            "formula": "📐"
        }
        
        # URLs das APIs
        self.apis = {
            "waifu": "https://api.waifu.pics/sfw/",
            "icons8": "https://api.icons8.com/api/iconsets/v4/icons"
        }
        
    def get_emoji(self, name: str) -> str:
        """Retorna o emoji correspondente ao nome."""
        return self.emojis.get(name, "❓")
        
    async def get_anime_image(self, category: str = "wave") -> Image.Image:
        """Obtém uma imagem anime da API Waifu.pics."""
        try:
            url = f"{self.apis['waifu']}{category}"
            response = requests.get(url)
            if response.status_code == 200:
                img_url = response.json()["url"]
                img_response = requests.get(img_url)
                return Image.open(BytesIO(img_response.content))
        except Exception as e:
            print(f"Erro ao obter imagem anime: {e}")
            return self._get_default_image()
            
    def get_icon(self, name: str, size: int = 32) -> ctk.CTkImage:
        """Obtém um ícone do Icons8 ou cache."""
        cache_path = self.cache_dir / f"icon_{name}_{size}.png"
        
        if cache_path.exists():
            return ctk.CTkImage(Image.open(cache_path), size=(size, size))
            
        try:
            # Usar CDN gratuito do Icons8
            url = f"https://img.icons8.com/{size}/000000/{name}.png"
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(cache_path)
                return ctk.CTkImage(img, size=(size, size))
        except:
            return self._get_default_icon(size)
            
    def _get_default_image(self) -> Image.Image:
        """Cria uma imagem padrão."""
        return Image.new('RGB', (64, 64), color='#24283b')
        
    def _get_default_icon(self, size: int) -> ctk.CTkImage:
        """Cria um ícone padrão."""
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        return ctk.CTkImage(img, size=(size, size))
        
    def inject_font_awesome(self, window: ctk.CTk):
        """Injeta o CSS do Font Awesome na janela."""
        fa_css = """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" 
              rel="stylesheet">
        """
        # Injetar via JavaScript no widget
        window.eval('javascript:void(document.head.innerHTML += arguments[0])', fa_css) 