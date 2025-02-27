import customtkinter as ctk
from PIL import Image, ImageTk
import os
from typing import Callable
import math

class AnimeAnimations:
    def __init__(self):
        self.current_animations = {}
        self.loaded_sprites = {}
        
    def load_sprite_sheet(self, name: str, path: str, sprite_width: int, sprite_height: int):
        """Carrega uma sprite sheet e divide em frames individuais."""
        if name not in self.loaded_sprites:
            sheet = Image.open(path)
            frames = []
            
            for y in range(0, sheet.height, sprite_height):
                for x in range(0, sheet.width, sprite_width):
                    frame = sheet.crop((x, y, x + sprite_width, y + sprite_height))
                    frames.append(ImageTk.PhotoImage(frame))
                    
            self.loaded_sprites[name] = frames
            
    def animate_label(self, label: ctk.CTkLabel, sprite_name: str, 
                     frame_duration: int = 100, loop: bool = True):
        """Inicia uma animação em um label."""
        if sprite_name not in self.loaded_sprites:
            return
            
        frames = self.loaded_sprites[sprite_name]
        current_frame = 0
        
        def update_frame():
            nonlocal current_frame
            if label.winfo_exists():
                label.configure(image=frames[current_frame])
                current_frame = (current_frame + 1) % len(frames)
                if loop or current_frame > 0:
                    label.after(frame_duration, update_frame)
                    
        update_frame()
        
    def floating_effect(self, widget: ctk.CTkBaseClass, amplitude: float = 10, 
                       period: float = 2000):
        """Aplica um efeito flutuante suave ao widget."""
        start_y = widget.winfo_y()
        start_time = widget.winfo_toplevel().winfo_id()  # Usar como referência de tempo
        
        def update_position():
            if widget.winfo_exists():
                current_time = widget.winfo_toplevel().winfo_id() - start_time
                offset = amplitude * math.sin(2 * math.pi * current_time / period)
                widget.place(y=start_y + offset)
                widget.after(16, update_position)  # ~60 FPS
                
        update_position()
        
    def particle_effect(self, canvas: ctk.CTkCanvas, x: int, y: int, 
                       particle_type: str = "sparkle"):
        """Cria um efeito de partículas no canvas."""
        particles = []
        
        class Particle:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.vx = (random.random() - 0.5) * 4
                self.vy = -random.random() * 6
                self.alpha = 1.0
                self.size = random.randint(3, 8)
                
            def update(self):
                self.x += self.vx
                self.y += self.vy
                self.vy += 0.2  # Gravidade
                self.alpha -= 0.02
                return self.alpha > 0
                
        def create_particles():
            for _ in range(20):
                particles.append(Particle(x, y))
                
        def update_particles():
            if canvas.winfo_exists():
                canvas.delete("particle")
                
                remaining_particles = []
                for p in particles:
                    if p.update():
                        color = self._get_particle_color(particle_type, p.alpha)
                        canvas.create_oval(
                            p.x - p.size, p.y - p.size,
                            p.x + p.size, p.y + p.size,
                            fill=color, tags="particle"
                        )
                        remaining_particles.append(p)
                        
                particles[:] = remaining_particles
                
                if particles:
                    canvas.after(16, update_particles)
                    
        create_particles()
        update_particles()
        
    def _get_particle_color(self, particle_type: str, alpha: float) -> str:
        """Retorna a cor da partícula baseada no tipo e alpha."""
        if particle_type == "sparkle":
            r, g, b = 255, 215, 0  # Dourado
        elif particle_type == "magic":
            r, g, b = 147, 112, 219  # Roxo
        else:
            r, g, b = 122, 162, 247  # Azul anime
            
        return f"#{int(r*alpha):02x}{int(g*alpha):02x}{int(b*alpha):02x}"
        
    def shake_effect(self, widget: ctk.CTkBaseClass, intensity: float = 5, 
                    duration: int = 500):
        """Aplica um efeito de tremor ao widget."""
        start_x = widget.winfo_x()
        start_y = widget.winfo_y()
        start_time = widget.winfo_toplevel().winfo_id()
        
        def update_shake():
            if widget.winfo_exists():
                current_time = widget.winfo_toplevel().winfo_id() - start_time
                if current_time < duration:
                    offset_x = random.uniform(-intensity, intensity)
                    offset_y = random.uniform(-intensity, intensity)
                    widget.place(x=start_x + offset_x, y=start_y + offset_y)
                    widget.after(16, update_shake)
                else:
                    widget.place(x=start_x, y=start_y)
                    
        update_shake() 