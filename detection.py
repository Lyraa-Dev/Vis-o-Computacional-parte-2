import numpy as np
import cv2
from collections import deque

class MotionDetector:
    def __init__(self, config):
        self.config = config
        self.frame_buffer = deque(maxlen=3)  # Buffer para diferença de quadros
        self.detection_threshold = config.DETECTION_THRESHOLD
        self.motion_threshold = config.MOTION_THRESHOLD
        
    def detect_target(self, target, pursuer, frame_count):
        """Detecta o alvo usando múltiplas técnicas"""
        
        # Técnica 1: Detecção por diferença de quadros
        detection1 = self._frame_difference_detection(target)
        
        # Técnica 2: Detecção por limiarização adaptativa
        detection2 = self._adaptive_threshold_detection(target, pursuer)
        
        # Técnica 3: Detecção baseada em centroides
        detection3 = self._centroid_detection(target)
        
        # Combinar detecções (lógica OR)
        if detection1 or detection2 or detection3:
            return (target.x, target.y)
        
        return None
    
    def _frame_difference_detection(self, target):
        """Detecção por diferença entre quadros consecutivos"""
        if len(target.position_history) < 2:
            return False
        
        # Calcular movimento baseado no histórico de posições
        current_pos = target.position_history[-1]
        prev_pos = target.position_history[0] if len(target.position_history) > 1 else current_pos
        
        movement = np.sqrt((current_pos[0] - prev_pos[0])**2 + 
                          (current_pos[1] - prev_pos[1])**2)
        
        return movement > self.motion_threshold
    
    def _adaptive_threshold_detection(self, target, pursuer):
        """Detecção por limiarização adaptativa (simulada)"""
        # Em uma implementação real, isso processaria a imagem
        # Aqui simulamos com base na distância e velocidade
        
        # Fator de visibilidade baseado na velocidade
        visibility = min(1.0, target.speed / self.config.TARGET_MAX_SPEED)
        
        # Fator baseado na distância do perseguidor
        if pursuer.target_detected:
            distance = np.sqrt((target.x - pursuer.x)**2 + (target.y - pursuer.y)**2)
            distance_factor = max(0, 1 - distance / (self.config.WIDTH / 2))
        else:
            distance_factor = 1.0
        
        # Limiar adaptativo
        adaptive_threshold = self.detection_threshold * (1 - visibility * 0.5) * distance_factor
        
        # Detecção aleatória baseada no limiar adaptativo
        detection_prob = min(0.9, adaptive_threshold / 50)
        return np.random.random() < detection_prob
    
    def _centroid_detection(self, target):
        """Detecção baseada em centroides (simulada)"""
        # Em uma implementação real, calcularíamos centroides de regiões em movimento
        # Aqui usamos uma abordagem probabilística baseada no movimento
        
        if len(target.position_history) < 3:
            return False
        
        # Calcular aceleração (mudança na velocidade)
        pos1 = target.position_history[-3]
        pos2 = target.position_history[-2]
        pos3 = target.position_history[-1]
        
        v1 = np.array([pos2[0] - pos1[0], pos2[1] - pos1[1]])
        v2 = np.array([pos3[0] - pos2[0], pos3[1] - pos2[1]])
        
        acceleration = np.linalg.norm(v2 - v1)
        
        # Maior aceleração = mais fácil de detectar
        detection_prob = min(0.8, acceleration / 10)
        return np.random.random() < detection_prob

class DetectionMetrics:
    def __init__(self):
        self.detection_history = []
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        
    def update(self, detected, actual_position):
        self.detection_history.append((detected, actual_position))
        
        if detected and actual_position is not None:
            self.true_positives += 1
        elif detected and actual_position is None:
            self.false_positives += 1
        elif not detected and actual_position is not None:
            self.false_negatives += 1
    
    def get_metrics(self):
        total = self.true_positives + self.false_positives + self.false_negatives
        if total == 0:
            return 0, 0, 0
        
        precision = self.true_positives / (self.true_positives + self.false_positives) if (self.true_positives + self.false_positives) > 0 else 0
        recall = self.true_positives / (self.true_positives + self.false_negatives) if (self.true_positives + self.false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return precision, recall, f1_score