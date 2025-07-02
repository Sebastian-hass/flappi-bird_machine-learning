import pygame
import random
import os
import numpy as np
import neat

# Inicializar pygame
pygame.init()

# Constantes del juego
WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

# Cargar imágenes
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg (1).png")))

class Bird:
    """Representa al pájaro en el juego"""
    MAX_ROTATION = 25
    IMGS = BIRD_IMGS
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # Grados de inclinación
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """Hacer que el pájaro salte"""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """Mover el pájaro"""
        self.tick_count += 1

        # Calcular desplazamiento
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2

        # Velocidad terminal
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        # Inclinación del pájaro
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """Dibujar el pájaro"""
        self.img_count += 1

        # Animación del aleteo
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Si está cayendo no aletea
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Rotar la imagen
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        """Obtener la máscara para detección de colisiones"""
        return pygame.mask.from_surface(self.img)

class Pipe:
    """Representa las tuberías en el juego"""
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        # Donde están la parte superior e inferior de la tubería
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        """Establecer la altura de la tubería"""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Mover la tubería"""
        self.x -= self.VEL

    def draw(self, win):
        """Dibujar la tubería superior e inferior"""
        # Dibujar la tubería superior
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # Dibujar la tubería inferior
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        """Ver si un pájaro colisiona con la tubería"""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False

class Base:
    """Representa el suelo en movimiento del juego"""
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """Mover el suelo para que parezca que se desplaza"""
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """Dibujar el suelo"""
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def blitRotateCenter(surf, image, topleft, angle):
    """Rotar una superficie y blit en una nueva posición"""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    """Dibujar la ventana del juego"""
    if gen == 0:
        gen = 1
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)
    
    base.draw(win)
    
    # Puntuación
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # Generaciones
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # Vivos
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()

def eval_genomes(genomes, config):
    """
    Ejecuta la simulación de la población actual de
    pájaros y establece su fitness basado en la distancia que viajaron
    en el juego.
    """
    global WIN, gen
    win = WIN
    gen += 1

    # Empezar por crear listas que contengan el genoma,
    # la red neuronal asociada al genoma y el objeto pájaro que usa esa red para jugar
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # empezar con fitness de 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1                                                                 

        for x, bird in enumerate(birds):  # dar a cada pájaro un fitness por moverse
            ge[x].fitness += 0.1
            bird.move()

            # enviar información del pájaro a la red neuronal y determinar si saltar o no
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # usamos una función de activación tanh, por lo que el resultado estará entre -1 y 1. si es mayor que 0.5, salta
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # verificar colisión
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

def run(config_file):
    """
    ejecuta el algoritmo NEAT para entrenar una red neuronal para jugar flappy bird.
    :param config_file: ubicación del archivo de configuración
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Crear la población, que es el objeto de nivel superior para una ejecución NEAT.
    p = neat.Population(config)

    # Agregar un reportero de salida estándar para mostrar el progreso en el terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Ejecutar por hasta 50 generaciones.
    winner = p.run(eval_genomes, 50)

    # mostrar las estadísticas finales
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determinar la ruta al archivo de configuración. Esta ruta es relativa a
    # el directorio de trabajo actual.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
