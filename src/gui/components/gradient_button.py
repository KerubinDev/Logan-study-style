class GradientButton(ModernButton):
    def __init__(self, *args, gradient=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if gradient:
            self._create_gradient(*gradient)
            
    def _create_gradient(self, color1, color2):
        """Cria um gradiente entre duas cores."""
        # Implementação do gradiente usando canvas 