class PomodoroTimer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.time_remaining = 25 * 60  # 25 minutos em segundos
        self.is_running = False
        self.total_time = 25 * 60
        
    def start(self):
        """Inicia o timer."""
        self.is_running = True
        
    def pause(self):
        """Pausa o timer."""
        self.is_running = False
        
    def reset(self):
        """Reseta o timer."""
        self.time_remaining = self.total_time
        self.is_running = False
        
    def get_remaining_time(self):
        """Retorna o tempo restante em segundos."""
        return self.time_remaining
        
    def update(self):
        """Atualiza o timer."""
        if self.is_running and self.time_remaining > 0:
            self.time_remaining -= 1
            return True
        return False 