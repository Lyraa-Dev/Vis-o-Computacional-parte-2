class Config:
    def __init__(self):
        # Canvas
        self.WIDTH = 800
        self.HEIGHT = 600
        
        # FPS
        self.FPS = 60
        
        # Cores
        self.BG_COLOR = (0, 0, 0)
        self.TARGET_COLOR = (0, 255, 0)  # Verde para Ligeirinho
        self.PURSUER_COLOR = (255, 0, 0)  # Vermelho para Frajola
        self.TEXT_COLOR = (255, 255, 255)
        
        # Agente Alvo (Ligeirinho)
        self.TARGET_SIZE = 20
        self.TARGET_MIN_SPEED = 8
        self.TARGET_MAX_SPEED = 15
        
        # Agente Perseguidor (Frajola)
        self.PURSUER_SIZE = 45
        self.PURSUER_SPEED = 10
        self.PURSUER_REACTION_TIME = 5  # Frames até reagir
        
        # Detecção
        self.DETECTION_THRESHOLD = 30
        self.MOTION_THRESHOLD = 5
        
        # Interceptação
        self.CAPTURE_DISTANCE = 20
        
        # Estratégias de perseguição
        self.PURSUIT_STRATEGIES = [
            "direct",      # Perseguição direta
            "intercept",   # Interceptação preditiva
            "proportional" # Navegação proporcional
        ]
        
        # Nomes de exibição para as estratégias
        self.STRATEGY_DISPLAY_NAMES = {
            "direct": "PERSEGUIÇÃO DIRETA",
            "intercept": "INTERCEPTAÇÃO PREDITIVA", 
            "proportional": "NAVEGAÇÃO PROPORCIONAL"
        }
        
        self.current_strategy = "direct"
        
        # Configurações de imagens
        self.IMAGE_PATHS = {
            'target': 'assets/ligeirinho.png',
            'pursuer': 'assets/frajola.png'
        }
        
        # Rotação dos sprites
        self.ROTATE_SPRITES = True
        
        # Agente Alvo (Ligeirinho)
        self.TARGET_SIZE = 20
        self.TARGET_MIN_SPEED = 8
        self.TARGET_MAX_SPEED = 15
        
        # Agente Perseguidor (Frajola)
        self.PURSUER_SIZE = 45
        self.PURSUER_SPEED = 10
        self.PURSUER_REACTION_TIME = 5  # Frames até reagir
        
        # Detecção
        self.DETECTION_THRESHOLD = 30
        self.MOTION_THRESHOLD = 5
        
        # Interceptação
        self.CAPTURE_DISTANCE = 20
        
        # Estratégias de perseguição
        self.PURSUIT_STRATEGIES = [
            "direct",      # Perseguição direta
            "intercept",   # Interceptação preditiva
            "proportional" # Navegação proporcional
        ]
        self.current_strategy = "direct"