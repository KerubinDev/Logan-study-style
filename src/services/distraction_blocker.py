import winreg
import ctypes
import os
import sys
from typing import Dict as TypeDict, List as TypeList
import json
from src.config.settings import DISTRACTION_DEFAULTS
from PySide6.QtWidgets import QMessageBox
from src.database.database import get_data_dir

class DistractionBlocker:
    def __init__(self):
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.is_active = False
        self.data_dir = get_data_dir()
        self.blocked_sites = self._load_sites()
        
    def _load_sites(self) -> TypeDict[str, TypeList[str]]:
        """Carrega os sites bloqueados do arquivo ou usa os padrões."""
        sites_file = os.path.join(self.data_dir, 'blocked_sites.json')
        if os.path.exists(sites_file):
            try:
                with open(sites_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return DISTRACTION_DEFAULTS.copy()
        
    def _save_sites(self):
        """Salva os sites bloqueados em arquivo."""
        sites_file = os.path.join(self.data_dir, 'blocked_sites.json')
        with open(sites_file, 'w') as f:
            json.dump(self.blocked_sites, f, indent=4)
            
    def get_sites(self) -> TypeDict[str, TypeList[str]]:
        """Retorna o dicionário de sites bloqueados."""
        return self.blocked_sites
        
    def _is_admin(self) -> bool:
        """Verifica se o programa está rodando como administrador."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def _request_admin(self) -> bool:
        """Solicita privilégios de administrador sem fechar o programa."""
        if not self._is_admin():
            # Mostrar mensagem ao usuário
            QMessageBox.warning(
                None,
                "Permissão Necessária",
                "O bloqueio de sites requer privilégios de administrador.\n"
                "Por favor, execute o programa como administrador."
            )
            return False
        return True
            
    def start_blocking(self) -> bool:
        """Inicia o bloqueio dos sites."""
        try:
            if not self._request_admin():
                return False
                
            # Backup do arquivo hosts
            if not os.path.exists(f"{self.hosts_path}.bak"):
                with open(self.hosts_path, 'r') as f:
                    with open(f"{self.hosts_path}.bak", 'w') as backup:
                        backup.write(f.read())
                        
            # Adicionar sites ao arquivo hosts
            with open(self.hosts_path, 'a') as f:
                f.write("\n# AnimeProductivity Suite - Início do bloqueio\n")
                
                for category, sites in self.blocked_sites.items():
                    f.write(f"\n# {category}\n")
                    for site in sites:
                        f.write(f"127.0.0.1 {site}\n")
                        f.write(f"127.0.0.1 www.{site}\n")
                        
                f.write("\n# AnimeProductivity Suite - Fim do bloqueio\n")
                
            # Limpar cache DNS
            os.system('ipconfig /flushdns')
            
            self.is_active = True
            return True
            
        except Exception as e:
            QMessageBox.critical(
                None,
                "Erro",
                f"Erro ao ativar bloqueio: {str(e)}"
            )
            return False
            
    def stop_blocking(self) -> bool:
        """Para o bloqueio dos sites."""
        try:
            if not self._request_admin():
                return False
                
            # Restaurar backup do arquivo hosts
            if os.path.exists(f"{self.hosts_path}.bak"):
                with open(f"{self.hosts_path}.bak", 'r') as backup:
                    with open(self.hosts_path, 'w') as f:
                        f.write(backup.read())
                        
            # Limpar cache DNS
            os.system('ipconfig /flushdns')
            
            self.is_active = False
            return True
            
        except Exception as e:
            QMessageBox.critical(
                None,
                "Erro",
                f"Erro ao desativar bloqueio: {str(e)}"
            )
            return False
            
    def add_site(self, site: str, category: str) -> bool:
        """Adiciona um site à lista de bloqueios."""
        try:
            if category not in self.blocked_sites:
                self.blocked_sites[category] = []
                
            if site not in self.blocked_sites[category]:
                self.blocked_sites[category].append(site)
                self._save_sites()
            return True
        except:
            return False
            
    def remove_site(self, site: str, category: str) -> bool:
        """Remove um site da lista de bloqueios."""
        try:
            if category in self.blocked_sites and site in self.blocked_sites[category]:
                self.blocked_sites[category].remove(site)
                self._save_sites()
            return True
        except:
            return False 