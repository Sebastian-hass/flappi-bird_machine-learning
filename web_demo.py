"""
Demo web del proyecto Flappy Bird AI
Versión simplificada para mostrar online
"""

import random
import os
import neat
import asyncio
import pygame

# Para compatibilidad web
try:
    import asyncio
    import platform
    WEB_MODE = platform.system() == "Emscripten"
except:
    WEB_MODE = False

# Constantes del juego
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730

# Inicializar pygame
pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI - Demo")

# Variables globales para el demo
demo_generation = 0
demo_best_score = 0
demo_current_score = 0
demo_birds_alive = 0

class SimpleBird:
    """Versión simplificada del pájaro para el demo"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.alive = True
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        
    def move(self):
        self.tick_count += 1
        displacement = self.vel * self.tick_count + 0.5 * 3 * (self.tick_count ** 2)
        
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2
            
        self.y = self.y + displacement
        
    def draw(self, win):
        # Dibujar pájaro simple como círculo
        color = (255, 255, 0) if self.alive else (128, 128, 128)
        pygame.draw.circle(win, color, (int(self.x), int(self.y)), 15)
        
    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 30)

class SimplePipe:
    """Versión simplificada de tubería para el demo"""
    def __init__(self, x):
        self.x = x
        self.height = random.randrange(150, 450)
        self.gap = 200
        self.vel = 5
        self.passed = False
        
    def move(self):
        self.x -= self.vel
        
    def draw(self, win):
        # Tubería superior
        pygame.draw.rect(win, (0, 255, 0), (self.x, 0, 80, self.height))
        # Tubería inferior
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.height + self.gap, 80, WIN_HEIGHT - self.height - self.gap))
        
    def collide(self, bird):
        bird_rect = bird.get_rect()
        top_rect = pygame.Rect(self.x, 0, 80, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + self.gap, 80, WIN_HEIGHT - self.height - self.gap)
        
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

def create_demo_ai():
    """Crear una IA de demostración con comportamiento predefinido"""
    class DemoAI:
        def __init__(self, strategy):
            self.strategy = strategy
            
        def decide(self, bird_y, pipe_height, pipe_bottom):
            if self.strategy == "random":
                return random.random() > 0.7
            elif self.strategy == "simple":
                return bird_y > pipe_height + 100
            elif self.strategy == "smart":
                target = pipe_height + 100
                return abs(bird_y - target) > 50 and bird_y > target
            return False
    
    # Crear diferentes estrategias de IA
    strategies = ["random", "simple", "smart", "smart", "smart"]
    return [DemoAI(strategy) for strategy in strategies]

async def run_demo():
    """Ejecutar demo principal"""
    global demo_generation, demo_best_score, demo_current_score, demo_birds_alive
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Crear pájaros y AIs de demo
    birds = [SimpleBird(230, 350) for _ in range(5)]
    ais = create_demo_ai()
    pipes = [SimplePipe(700)]
    
    demo_generation += 1
    demo_current_score = 0
    demo_birds_alive = len(birds)
    
    frame_count = 0
    
    while len(birds) > 0:
        # Para compatibilidad web
        if WEB_MODE:
            await asyncio.sleep(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
        # Encontrar tubería relevante
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + 80:
                pipe_ind = 1
        
        # Actualizar pájaros
        for i, bird in enumerate(birds[:]):
            bird.move()
            
            # IA decide si saltar
            if pipe_ind < len(pipes):
                should_jump = ais[i % len(ais)].decide(
                    bird.y, 
                    pipes[pipe_ind].height, 
                    pipes[pipe_ind].height + pipes[pipe_ind].gap
                )
                if should_jump:
                    bird.jump()
            
            # Verificar colisiones
            if bird.y > FLOOR or bird.y < 0:
                birds.remove(bird)
            else:
                for pipe in pipes:
                    if pipe.collide(bird):
                        birds.remove(bird)
                        break
        
        # Actualizar tuberías
        for pipe in pipes[:]:
            pipe.move()
            if pipe.x + 80 < 0:
                pipes.remove(pipe)
            elif not pipe.passed and pipe.x < 230:
                pipe.passed = True
                demo_current_score += 1
                if demo_current_score > demo_best_score:
                    demo_best_score = demo_current_score
        
        # Agregar nueva tubería
        if len(pipes) == 0 or pipes[-1].x < WIN_WIDTH - 300:
            pipes.append(SimplePipe(WIN_WIDTH))
        
        # Dibujar todo
        WIN.fill((135, 206, 235))  # Cielo azul
        
        for pipe in pipes:
            pipe.draw(WIN)
            
        for bird in birds:
            bird.draw(WIN)
        
        # Dibujar suelo
        pygame.draw.rect(WIN, (222, 216, 149), (0, FLOOR, WIN_WIDTH, WIN_HEIGHT - FLOOR))
        
        # Dibujar información
        demo_birds_alive = len(birds)
        texts = [
            f"Generación: {demo_generation}",
            f"Puntuación: {demo_current_score}",
            f"Mejor: {demo_best_score}",
            f"Vivos: {demo_birds_alive}",
            "",
            "Demo de IA aprendiendo",
            "Flappy Bird con NEAT"
        ]
        
        for i, text in enumerate(texts):
            if text:
                text_surface = font.render(text, True, (255, 255, 255))
                WIN.blit(text_surface, (10, 10 + i * 30))
        
        pygame.display.flip()
        clock.tick(30)
        
        frame_count += 1
        
        # Reiniciar demo después de un tiempo
        if frame_count > 1800:  # 60 segundos a 30 FPS
            break
    
    return True

async def main():
    """Función principal del demo"""
    running = True
    while running:
        running = await run_demo()
        if running:
            # Pequeña pausa entre generaciones
            for _ in range(60):  # 2 segundos
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
            if not running:
                break

        print("Preparando nueva generación...")
        await asyncio.sleep(2)
        
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
