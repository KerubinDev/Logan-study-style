import customtkinter as ctk

class ShadowFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Criar efeito de sombra
        shadow = ctk.CTkFrame(
            self,
            fg_color=self.cget('fg_color'),
            corner_radius=self.cget('corner_radius')
        )
        shadow.place(relx=0.02, rely=0.02, relwidth=1, relheight=1)
        shadow.lower() 