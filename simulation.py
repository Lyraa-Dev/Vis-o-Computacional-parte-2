# simulation.py
import pygame
import numpy as np
from agents import Target, Pursuer
from detection import MotionDetector, DetectionMetrics
from sprites import SpriteManager  # IMPORTANTE: Adicionar esta linha

class Simulation:
    def __init__(self, config):
        self.config = config
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("O Rato mais rápido de todo o México")
        
        # Inicializar gerenciador de sprites
        self.sprite_manager = SpriteManager(config)
        
        # Inicializar agentes com gerenciador de sprites
        self.target = Target(config, self.sprite_manager)
        self.pursuer = Pursuer(config, self.sprite_manager)
        
        # Sistema de detecção
        self.detector = MotionDetector(config)
        self.metrics = DetectionMetrics()
        
        # Estatísticas
        self.frame_count = 0
        self.capture_count = 0
        self.total_capture_time = 0
        self.current_capture_start = 0
        
        # Estado
        self.paused = False
        self.captured = False
        self.capture_display_time = 0
        self.capture_display_duration = 60  # Mostrar mensagem por 60 frames (1 segundo a 60 FPS)
        
        # Fontes para texto
        self.font = pygame.font.SysFont('Arial', 16)
        self.large_font = pygame.font.SysFont('Arial', 32)
        
    def update(self):
        if self.captured:
            self.capture_display_time += 1
            # Reiniciar automaticamente após mostrar a mensagem de captura
            if self.capture_display_time >= self.capture_display_duration:
                self.reset()
            return
            
        self.frame_count += 1
        
        # Atualizar alvo
        self.target.update()
        
        # Detectar alvo
        detected_position = self.detector.detect_target(
            self.target, self.pursuer, self.frame_count
        )
        
        # Atualizar métricas de detecção
        self.metrics.update(detected_position is not None, (self.target.x, self.target.y))
        
        # Atualizar perseguidor
        self.pursuer.update(detected_position, self.config.current_strategy)
        
        # Verificar captura
        distance = np.sqrt((self.target.x - self.pursuer.x)**2 + 
                          (self.target.y - self.pursuer.y)**2)
        
        if distance < self.config.CAPTURE_DISTANCE:
            self.captured = True
            self.capture_count += 1
            capture_time = self.frame_count - self.current_capture_start
            self.total_capture_time += capture_time
            self.capture_display_time = 0
    
    def handle_event(self, event):
        if event.type == pygame.USEREVENT and self.captured:
            self.reset()
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Cancelar timer
    
    def reset(self):
        self.target.reset()
        self.pursuer = Pursuer(self.config, self.sprite_manager)
        self.captured = False
        self.capture_display_time = 0
        self.current_capture_start = self.frame_count
    
    def render(self):
        # Fundo
        self.screen.fill(self.config.BG_COLOR)
        
        # Desenhar agentes
        self.target.draw(self.screen)
        self.pursuer.draw(self.screen)
        
        # Informações de debug
        self._draw_info()
        
        # Mensagem de captura
        if self.captured:
            self._draw_capture_message()
    
    def _draw_info(self):
        # Estatísticas
        precision, recall, f1 = self.metrics.get_metrics()
        avg_capture_time = self.total_capture_time / self.capture_count if self.capture_count > 0 else 0
        
        # Display da estratégia atual com destaque
        strategy_display = f"ESTRATÉGIA: {self.config.current_strategy.upper()}"
        strategy_text = self.font.render(strategy_display, True, (255, 255, 0))  # Amarelo para destaque
        self.screen.blit(strategy_text, (10, 10))
        
        info_lines = [
            f"Frames: {self.frame_count}",
            f"Capturas: {self.capture_count}",
            f"Tempo médio de captura: {avg_capture_time:.1f} frames",
            f"Detecção - Precisão: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}",
            f"Alvo detectado: {'SIM' if self.pursuer.target_detected else 'NÃO'}",
            f"Velocidade alvo: {self.target.speed:.1f}",
            f"Velocidade perseguidor: {self.pursuer.speed:.1f}",
            "",
            "Controles:",
            "R - Reiniciar (Reset completo)",
            "ESPAÇO - Pausar",
            "1 - Perseguição Direta",
            "2 - Interceptação Preditiva", 
            "3 - Navegação Proporcional",
            "T - Alternar rotação de sprites"
        ]
        
        for i, line in enumerate(info_lines):
            text = self.font.render(line, True, self.config.TEXT_COLOR)
            self.screen.blit(text, (10, 30 + i * 20))
    
    def _draw_capture_message(self):
        # Fundo semitransparente para a mensagem
        s = pygame.Surface((self.config.WIDTH, 100), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Preto semitransparente
        self.screen.blit(s, (0, (self.config.HEIGHT - 100) // 2))
        
        # Mensagem de captura
        font = pygame.font.SysFont('Arial', 48)
        text = font.render("CAPTURADO!", True, (255, 255, 0))
        text_rect = text.get_rect(center=(self.config.WIDTH/2, self.config.HEIGHT/2 - 20))
        self.screen.blit(text, text_rect)
        
        # Mensagem de reinício automático
        small_font = pygame.font.SysFont('Arial', 24)
        restart_text = small_font.render("Reiniciando automaticamente...", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.config.WIDTH/2, self.config.HEIGHT/2 + 30))
        self.screen.blit(restart_text, restart_rect)
    
    def reset_complete(self):
        """Reinicia completamente a simulação, incluindo estatísticas"""
        self.target.reset()
        self.pursuer = Pursuer(self.config, self.sprite_manager)
        self.captured = False
        self.capture_display_time = 0
        self.frame_count = 0
        self.capture_count = 0
        self.total_capture_time = 0
        self.current_capture_start = 0
        self.metrics = DetectionMetrics()