import os
import requests
import shutil
from pathlib import Path
from zipfile import ZipFile
import json

class AssetDownloader:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.assets_dir = self.base_dir / "assets"
        self.icons_dir = self.assets_dir / "icons"
        self.anime_dir = self.assets_dir / "anime"
        self.sprites_dir = self.assets_dir / "sprites"
        
        # URLs dos recursos
        self.resources = {
            "icons": {
                "url": "https://github.com/seu-repo/logan-study-style/releases/download/v1.0/icons.zip",
                "files": [
                    "app.ico",
                    "google_calendar.png",
                    "settings.png",
                    "tasks.png",
                    "timer.png",
                    "achievements.png",
                    "study.png",
                    "focus.png"
                ]
            },
            "anime": {
                "url": "https://github.com/seu-repo/anime-productivity/releases/download/v1.0/anime.zip",
                "files": [
                    "character_idle.png",
                    "level_up.png",
                    "achievement_unlock.png"
                ]
            },
            "sprites": {
                "url": "https://github.com/seu-repo/anime-productivity/releases/download/v1.0/sprites.zip",
                "files": [
                    "particles.png",
                    "effects.png"
                ]
            }
        }
        
    def create_directories(self):
        """Cria a estrutura de diretórios necessária."""
        directories = [
            self.assets_dir,
            self.icons_dir,
            self.anime_dir,
            self.sprites_dir,
            self.base_dir / "src" / "config",
            self.base_dir / "src" / "database",
            self.base_dir / "src" / "gui",
            self.base_dir / "src" / "services",
            self.base_dir / "src" / "utils",
            self.base_dir / "data",
            self.base_dir / "tokens",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def download_fallback_assets(self):
        """Baixa assets alternativos de CDNs públicas caso os principais falhem."""
        fallback_resources = {
            "icons": {
                # Ícones do Material Design Icons
                "app.ico": "https://cdn.materialdesignicons.com/5.4.55/png/48/timer.png",
                "google_calendar": "https://cdn.materialdesignicons.com/5.4.55/png/48/calendar.png",
                "settings": "https://cdn.materialdesignicons.com/5.4.55/png/48/cog.png",
                "tasks": "https://cdn.materialdesignicons.com/5.4.55/png/48/clipboard-check.png",
                "timer": "https://cdn.materialdesignicons.com/5.4.55/png/48/timer.png",
                "achievements": "https://cdn.materialdesignicons.com/5.4.55/png/48/trophy.png"
            },
            "anime": {
                # Sprites de personagens anime gratuitos
                "character_idle": "https://opengameart.org/sites/default/files/styles/medium/public/anime_character.png",
                "level_up": "https://opengameart.org/sites/default/files/styles/medium/public/level_up_effect.png"
            }
        }
        
        for category, assets in fallback_resources.items():
            target_dir = getattr(self, f"{category}_dir")
            for name, url in assets.items():
                try:
                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        file_path = target_dir / f"{name}.png"
                        with open(file_path, 'wb') as f:
                            response.raw.decode_content = True
                            shutil.copyfileobj(response.raw, f)
                except:
                    print(f"Falha ao baixar {name} de {url}")
                    
    def create_default_config(self):
        """Cria arquivos de configuração padrão."""
        config = {
            "theme": "dark",
            "animations_enabled": True,
            "particle_effects": True,
            "character_enabled": True,
            "sound_effects": True
        }
        
        config_path = self.base_dir / "src" / "config" / "default_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
            
    def setup_project(self):
        """Configura todo o projeto."""
        print("Criando estrutura de diretórios...")
        self.create_directories()
        
        print("Baixando assets...")
        try:
            # Tentar baixar dos repositórios principais
            for category, info in self.resources.items():
                response = requests.get(info["url"], stream=True)
                if response.status_code == 200:
                    zip_path = self.assets_dir / f"{category}.zip"
                    with open(zip_path, 'wb') as f:
                        shutil.copyfileobj(response.raw, f)
                    
                    with ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(getattr(self, f"{category}_dir"))
                    
                    os.remove(zip_path)
        except:
            print("Falha ao baixar assets principais, usando fallback...")
            self.download_fallback_assets()
        
        print("Criando configurações padrão...")
        self.create_default_config()
        
        print("Projeto configurado com sucesso!")
        
if __name__ == "__main__":
    downloader = AssetDownloader()
    downloader.setup_project() 