import pygame
import sys
import numpy as np
from simulation import Simulation
from config import Config
from utils import change_strategy  # Adicionar esta importação

def main():
    pygame.init()
    
    # Configurações
    config = Config()
    
    # Verificar se assets directory existe
    import os
    if not os.path.exists('assets'):
        print("Criando diretório 'assets' para imagens...")
        os.makedirs('assets')
        print("Por favor, adicione as imagens 'ligeirinho.png' e 'frajola.png' na pasta 'assets'")
    
    # Inicializar simulação
    simulation = Simulation(config)
    
    # Loop principal
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reinício completo - resetar todas as estatísticas
                    simulation.reset_complete()
                elif event.key == pygame.K_SPACE:
                    simulation.paused = not simulation.paused
                elif event.key == pygame.K_1:
                    config.current_strategy = "direct"
                elif event.key == pygame.K_2:
                    config.current_strategy = "intercept"
                elif event.key == pygame.K_3:
                    config.current_strategy = "proportional"
                elif event.key == pygame.K_t:
                    # Alternar rotação de sprites
                    config.ROTATE_SPRITES = not config.ROTATE_SPRITES
        
        if not simulation.paused:
            simulation.update()
        
        simulation.render()
        pygame.display.flip()
        clock.tick(config.FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()