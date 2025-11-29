import pygame
import numpy as np
import random
import math

class Target:
    def __init__(self, config, sprite_manager):
        self.config = config
        self.sprite_manager = sprite_manager
        self.size = config.TARGET_SIZE
        self.color = config.TARGET_COLOR
        self.angle = 0  # Ângulo para rotação do sprite
        
        # Inicializar dx e dy como 0
        self.dx = 0
        self.dy = 0
        
        self.reset()
        
    def reset(self):
        # Posição inicial em uma borda aleatória
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            self.x = random.uniform(0, self.config.WIDTH)
            self.y = 0
        elif side == 'bottom':
            self.x = random.uniform(0, self.config.WIDTH)
            self.y = self.config.HEIGHT
        elif side == 'left':
            self.x = 0
            self.y = random.uniform(0, self.config.HEIGHT)
        else:  # right
            self.x = self.config.WIDTH
            self.y = random.uniform(0, self.config.HEIGHT)
        
        # Direção aleatória apontando para dentro do canvas
        center_x, center_y = self.config.WIDTH / 2, self.config.HEIGHT / 2
        angle = np.arctan2(center_y - self.y, center_x - self.x)
        angle += random.uniform(-np.pi/4, np.pi/4)  # Variação de ±45 graus
        
        # Velocidade
        self.speed = random.uniform(
            self.config.TARGET_MIN_SPEED, 
            self.config.TARGET_MAX_SPEED
        )
        
        # Vetor de direção (AGORA DEFINIMOS dx e dy ANTES de calcular o ângulo)
        self.dx = np.cos(angle) * self.speed
        self.dy = np.sin(angle) * self.speed
        
        # Calcular ângulo inicial baseado na direção (AGORA dx e dy já estão definidos)
        self.angle = math.degrees(math.atan2(-self.dy, self.dx)) - 90
        
        # Histórico para detecção de movimento
        self.position_history = []
        
    def update(self):
        # Salvar posição anterior para cálculo de rotação
        old_x, old_y = self.x, self.y
        
        # Atualizar posição
        self.x += self.dx
        self.y += self.dy
        
        # Verificar colisão com bordas e refletir
        if self.x <= 0 or self.x >= self.config.WIDTH:
            self.dx = -self.dx
            self.x = max(0, min(self.x, self.config.WIDTH))
        
        if self.y <= 0 or self.y >= self.config.HEIGHT:
            self.dy = -self.dy
            self.y = max(0, min(self.y, self.config.HEIGHT))
        
        # Atualizar ângulo baseado na direção do movimento
        if self.dx != 0 or self.dy != 0:
            self.angle = math.degrees(math.atan2(-self.dy, self.dx)) - 90
        
        # Manter histórico de posições
        self.position_history.append((self.x, self.y))
        if len(self.position_history) > 10:  # Manter apenas últimas 10 posições
            self.position_history.pop(0)
    
    def draw(self, screen):
        sprite = self.sprite_manager.get_sprite('target')
        
        if sprite and self.config.ROTATE_SPRITES:
            # Usar sprite rotacionado
            rotated_sprite = self.sprite_manager.get_rotated_sprite('target', self.angle)
            if rotated_sprite:
                rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(rotated_sprite, rect)
                return
        
        if sprite:
            # Usar sprite normal
            rect = sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(sprite, rect)
        else:
            # Fallback para forma geométrica
            pygame.draw.rect(screen, self.color, 
                            (self.x - self.size/2, self.y - self.size/2, 
                             self.size, self.size))

class Pursuer:
    def __init__(self, config, sprite_manager):
        self.config = config
        self.sprite_manager = sprite_manager
        self.size = config.PURSUER_SIZE
        self.color = config.PURSUER_COLOR
        self.speed = config.PURSUER_SPEED
        self.reaction_counter = 0
        self.angle = 0  # Ângulo para rotação do sprite
        
        # Posição inicial no centro
        self.x = config.WIDTH / 2
        self.y = config.HEIGHT / 2
        
        # Estado de detecção
        self.target_detected = False
        self.last_known_position = None
        self.predicted_position = None
        
    def update(self, target_position, strategy="direct"):
        if target_position is None:
            self.target_detected = False
            return
        
        self.target_detected = True
        self.last_known_position = target_position
        
        # Atraso de reação
        if self.reaction_counter < self.config.PURSUER_REACTION_TIME:
            self.reaction_counter += 1
            return
        
        self.reaction_counter = 0
        
        # Salvar posição anterior
        old_x, old_y = self.x, self.y
        
        # Aplicar estratégia de perseguição
        if strategy == "direct":
            self._direct_pursuit(target_position)
        elif strategy == "intercept":
            self._intercept_pursuit(target_position)
        elif strategy == "proportional":
            self._proportional_navigation(target_position)
        
        # Atualizar ângulo baseado na direção do movimento
        dx = self.x - old_x
        dy = self.y - old_y
        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(-dy, dx)) - 90
    
    def _direct_pursuit(self, target_pos):
        tx, ty = target_pos
        
        # Calcular direção
        dx = tx - self.x
        dy = ty - self.y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalizar e aplicar velocidade
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def _intercept_pursuit(self, target_pos):
        # Predição de interceptação (simplificada)
        tx, ty = target_pos
        
        # Estimativa de posição futura baseada na velocidade atual
        future_x = tx
        future_y = ty
        
        # Calcular direção para o ponto de interceptação
        dx = future_x - self.x
        dy = future_y - self.y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalizar e aplicar velocidade
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def _proportional_navigation(self, target_pos):
        # Navegação proporcional (simplificada)
        tx, ty = target_pos
        
        # Calcular linha de visão
        dx = tx - self.x
        dy = ty - self.y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Adicionar componente proporcional à taxa de giro da linha de visão
            # (simplificado como um pequeno ajuste angular)
            angle_adjustment = 0.1  # Fator de ajuste
            
            # Calcular ângulo atual
            current_angle = np.arctan2(dy, dx)
            
            # Aplicar pequeno ajuste aleatório para simular navegação proporcional
            adjusted_angle = current_angle + random.uniform(-angle_adjustment, angle_adjustment)
            
            # Mover na direção ajustada
            self.x += np.cos(adjusted_angle) * self.speed
            self.y += np.sin(adjusted_angle) * self.speed
    
    def draw(self, screen):
        sprite = self.sprite_manager.get_sprite('pursuer')
        
        if sprite and self.config.ROTATE_SPRITES:
            # Usar sprite rotacionado
            rotated_sprite = self.sprite_manager.get_rotated_sprite('pursuer', self.angle)
            if rotated_sprite:
                rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(rotated_sprite, rect)
        elif sprite:
            # Usar sprite normal
            rect = sprite.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(sprite, rect)
        else:
            # Fallback para forma geométrica
            pygame.draw.rect(screen, self.color, 
                            (self.x - self.size/2, self.y - self.size/2, 
                             self.size, self.size))
        
        # Indicador de detecção (sobreposto à imagem)
        if self.target_detected:
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(self.x), int(self.y)), 
                             self.size + 5, 2)