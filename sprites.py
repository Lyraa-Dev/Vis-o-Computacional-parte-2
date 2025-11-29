# sprites.py
import pygame
import os

class SpriteManager:
    def __init__(self, config):
        self.config = config
        self.sprites = {}
        self.load_sprites()
    
    def load_sprites(self):
        """Carrega e prepara todos os sprites"""
        try:
            # Carregar imagem do alvo (Ligeirinho)
            target_img = pygame.image.load(self.config.IMAGE_PATHS['target']).convert_alpha()
            # Redimensionar para o tamanho do agente
            target_size = (self.config.TARGET_SIZE, self.config.TARGET_SIZE)
            self.sprites['target'] = pygame.transform.smoothscale(target_img, target_size)
            
            # Carregar imagem do perseguidor (Frajola)
            pursuer_img = pygame.image.load(self.config.IMAGE_PATHS['pursuer']).convert_alpha()
            # Redimensionar para o tamanho do agente
            pursuer_size = (self.config.PURSUER_SIZE, self.config.PURSUER_SIZE)
            self.sprites['pursuer'] = pygame.transform.smoothscale(pursuer_img, pursuer_size)
            
            print("Sprites carregados com sucesso!")
            
        except pygame.error as e:
            print(f"Erro ao carregar sprites: {e}")
            print("Usando fallback para formas geométricas")
            self.sprites['target'] = None
            self.sprites['pursuer'] = None
    
    def get_rotated_sprite(self, sprite_type, angle):
        """Retorna um sprite rotacionado"""
        if self.sprites.get(sprite_type) is None:
            return None
        
        return pygame.transform.rotate(self.sprites[sprite_type], angle)
    
    def get_sprite(self, sprite_type):
        """Retorna o sprite original"""
        return self.sprites.get(sprite_type)