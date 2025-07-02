import neat
import pygame
import os
from flappy_bird import run

# Variables globales
WIN = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Flappy Bird AI")
gen = 0

if __name__ == "__main__":
    # Determinar la ruta al archivo de configuración
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    
    # Configurar las variables globales necesarias para flappy_bird.py
    import flappy_bird
    flappy_bird.WIN = WIN
    flappy_bird.gen = gen
    
    # Ejecutar el entrenamiento
    run(config_path)
