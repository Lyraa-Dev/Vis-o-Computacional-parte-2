import pygame
import numpy as np

def change_strategy(config, strategy_index):
    """Muda a estratégia de perseguição"""
    if 0 <= strategy_index < len(config.PURSUIT_STRATEGIES):
        config.current_strategy = config.PURSUIT_STRATEGIES[strategy_index]
        return True
    return False

def calculate_performance_metrics(simulation):
    """Calcula métricas de desempenho"""
    capture_rate = simulation.capture_count / (simulation.frame_count / simulation.config.FPS) if simulation.frame_count > 0 else 0
    avg_capture_time = simulation.total_capture_time / simulation.capture_count if simulation.capture_count > 0 else float('inf')
    
    precision, recall, f1 = simulation.metrics.get_metrics()
    
    return {
        'capture_rate': capture_rate,
        'avg_capture_time': avg_capture_time,
        'detection_precision': precision,
        'detection_recall': recall,
        'detection_f1': f1,
        'total_captures': simulation.capture_count,
        'total_frames': simulation.frame_count,
        'current_strategy': simulation.config.current_strategy
    }

def save_results(results, filename="results.txt"):
    """Salva resultados em arquivo"""
    with open(filename, 'w') as f:
        for key, value in results.items():
            f.write(f"{key}: {value}\n")

def get_strategy_display_name(strategy):
    """Retorna o nome amigável da estratégia"""
    names = {
        "direct": "Perseguição Direta",
        "intercept": "Interceptação Preditiva",
        "proportional": "Navegação Proporcional"
    }
    return names.get(strategy, strategy)