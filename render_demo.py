"""
Demo simplificado del proyecto Flappy Bird AI para Render
Versión de consola sin GUI
"""

import random
import time
import neat
import os

# Constantes del juego
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730

class SimpleBird:
    """Versión simplificada del pájaro para el demo"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.alive = True
        self.fitness = 0
        
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
        
    def is_alive(self):
        return self.y > 0 and self.y < FLOOR and self.alive

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
        
    def collide(self, bird):
        if bird.x > self.x and bird.x < self.x + 80:
            if bird.y < self.height or bird.y > self.height + self.gap:
                return True
        return False

def create_demo_ai():
    """Crear una IA de demostración con comportamiento predefinido"""
    class DemoAI:
        def __init__(self, strategy):
            self.strategy = strategy
            
        def decide(self, bird_y, pipe_height, pipe_distance):
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

def run_generation(generation_num):
    """Ejecutar una generación del demo"""
    print(f"\n🎮 GENERACIÓN {generation_num}")
    print("=" * 50)
    
    # Crear pájaros y AIs de demo
    birds = [SimpleBird(230, 350) for _ in range(5)]
    ais = create_demo_ai()
    pipes = [SimplePipe(700)]
    
    score = 0
    frame_count = 0
    max_frames = 1800  # Limitar duración
    
    while len(birds) > 0 and frame_count < max_frames:
        frame_count += 1
        
        # Encontrar tubería relevante
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + 80:
                pipe_ind = 1
        
        # Actualizar pájaros
        active_birds = []
        for i, bird in enumerate(birds):
            bird.move()
            bird.fitness += 1  # Fitness por estar vivo
            
            # IA decide si saltar
            if pipe_ind < len(pipes):
                should_jump = ais[i % len(ais)].decide(
                    bird.y, 
                    pipes[pipe_ind].height, 
                    pipes[pipe_ind].x - bird.x
                )
                if should_jump:
                    bird.jump()
            
            # Verificar si sigue vivo
            if bird.is_alive():
                # Verificar colisiones con tuberías
                collision = False
                for pipe in pipes:
                    if pipe.collide(bird):
                        collision = True
                        break
                
                if not collision:
                    active_birds.append(bird)
                else:
                    print(f"   🪦 Pájaro {i+1} eliminado por colisión (fitness: {bird.fitness})")
            else:
                print(f"   🪦 Pájaro {i+1} eliminado por límites (fitness: {bird.fitness})")
        
        birds = active_birds
        
        # Actualizar tuberías
        for pipe in pipes[:]:
            pipe.move()
            if pipe.x + 80 < 0:
                pipes.remove(pipe)
            elif not pipe.passed and pipe.x < 230:
                pipe.passed = True
                score += 1
                print(f"   🎯 ¡Tubería pasada! Puntuación: {score}")
        
        # Agregar nueva tubería
        if len(pipes) == 0 or pipes[-1].x < WIN_WIDTH - 300:
            pipes.append(SimplePipe(WIN_WIDTH))
        
        # Mostrar progreso cada 300 frames (10 segundos)
        if frame_count % 300 == 0:
            print(f"   📊 Frame {frame_count}, Pájaros vivos: {len(birds)}, Puntuación: {score}")
        
        # Pequeña pausa para no saturar la consola
        if frame_count % 10 == 0:
            time.sleep(0.01)
    
    print(f"\n📋 RESUMEN DE LA GENERACIÓN {generation_num}:")
    print(f"   • Puntuación final: {score}")
    print(f"   • Frames totales: {frame_count}")
    if birds:
        best_fitness = max(bird.fitness for bird in birds)
        print(f"   • Mejor fitness: {best_fitness}")
    
    return score

def main():
    """Función principal del demo"""
    print("🤖 FLAPPY BIRD AI - DEMO PARA RENDER")
    print("=" * 50)
    print("Simulando el entrenamiento de IA con NEAT...")
    print("(Versión simplificada sin interfaz gráfica)")
    
    best_score = 0
    generation = 0
    
    try:
        while generation < 10:  # Limitar a 10 generaciones para el demo
            generation += 1
            score = run_generation(generation)
            
            if score > best_score:
                best_score = score
                print(f"   🏆 ¡NUEVO RÉCORD! Mejor puntuación: {best_score}")
            
            print(f"\n⏳ Preparando siguiente generación...")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n⛔ Demo interrumpido por el usuario")
    
    print(f"\n🎉 DEMO COMPLETADO")
    print(f"   • Generaciones ejecutadas: {generation}")
    print(f"   • Mejor puntuación alcanzada: {best_score}")
    print(f"\n💡 En el juego real con NEAT, la IA mejora gradualmente")
    print("   aprendiendo a navegar entre las tuberías de forma autónoma.")
    
    # Mantener el servidor activo
    print(f"\n🔄 Manteniendo el servidor activo...")
    while True:
        time.sleep(60)
        print(f"   ⏰ Demo ejecutándose... Mejor puntuación: {best_score}")

if __name__ == "__main__":
    main()
