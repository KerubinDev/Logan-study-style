import winreg
import ctypes
import os
import sys
from typing import List, Dict
import json
from src.config.settings import DISTRACTION_DEFAULTS

class DistractionBlocker:
    def __init__(self):
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.blocked_sites = self._load_blocked_sites()
        self.is_active = False
        
    def _load_blocked_sites(self) -> Dict[str, List[str]]:
        """Carrega a lista de sites bloqueados do arquivo de configuração."""
        config_path = os.path.join("config", "blocked_sites.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return DISTRACTION_DEFAULTS
        
    def _save_blocked_sites(self):
        """Salva a lista de sites bloqueados."""
        config_path = os.path.join("config", "blocked_sites.json")
        os.makedirs("config", exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(self.blocked_sites, f, indent=4)
            
    def _is_admin(self) -> bool:
        """Verifica se o programa está rodando como administrador."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def _require_admin(self):
        """Reinicia o programa como administrador se necessário."""
        if not self._is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()
            
    def start_blocking(self) -> tuple[bool, str]:
        """Inicia o bloqueio de sites."""
        try:
            self._require_admin()
            
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
            return True, "Bloqueio ativado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao ativar bloqueio: {str(e)}"
            
    def stop_blocking(self) -> tuple[bool, str]:
        """Para o bloqueio de sites."""
        try:
            self._require_admin()
            
            # Restaurar backup do arquivo hosts
            if os.path.exists(f"{self.hosts_path}.bak"):
                with open(f"{self.hosts_path}.bak", 'r') as backup:
                    with open(self.hosts_path, 'w') as f:
                        f.write(backup.read())
                        
            # Limpar cache DNS
            os.system('ipconfig /flushdns')
            
            self.is_active = False
            return True, "Bloqueio desativado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao desativar bloqueio: {str(e)}"
            
    def add_site(self, site: str, category: str = "Outros") -> tuple[bool, str]:
        """Adiciona um site à lista de bloqueios."""
        if category not in self.blocked_sites:
            self.blocked_sites[category] = []
            
        if site not in self.blocked_sites[category]:
            self.blocked_sites[category].append(site)
            self._save_blocked_sites()
            
            # Atualizar bloqueio se ativo
            if self.is_active:
                return self.start_blocking()
                
            return True, "Site adicionado com sucesso"
        return False, "Site já está na lista"
        
    def remove_site(self, site: str, category: str) -> tuple[bool, str]:
        """Remove um site da lista de bloqueios."""
        if category in self.blocked_sites and site in self.blocked_sites[category]:
            self.blocked_sites[category].remove(site)
            self._save_blocked_sites()
            
            # Atualizar bloqueio se ativo
            if self.is_active:
                return self.start_blocking()
                
            return True, "Site removido com sucesso"
        return False, "Site não encontrado" 