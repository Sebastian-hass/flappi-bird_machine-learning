"""
ANÁLISIS LÍNEA POR LÍNEA: eval_genomes()

Esta función es donde ocurre toda la magia del aprendizaje.
Vamos a entender cada decisión del programador.
"""

print("🔬 ANÁLISIS DETALLADO DE eval_genomes()")
print("="*50)

print("\n📋 LÍNEAS 225-235: PREPARACIÓN DE LA POBLACIÓN")
print("¿Qué hace el programador aquí?")
print("""
nets = []    # Lista de cerebros
birds = []   # Lista de cuerpos físicos  
ge = []      # Lista de información genética

for genome_id, genome in genomes:
    genome.fitness = 0  # ← DECISIÓN: Todos empiezan iguales
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    nets.append(net)
    birds.append(Bird(230,350))  # ← DECISIÓN: Misma posición inicial
    ge.append(genome)

PENSAMIENTO DEL PROGRAMADOR:
"Necesito mantener 3 listas sincronizadas:
 - nets[0] controla birds[0] que tiene DNA ge[0]
 - nets[1] controla birds[1] que tiene DNA ge[1]
 - etc..."
""")

print("\n🎮 LÍNEAS 244-267: BUCLE PRINCIPAL DEL JUEGO")
print("¿Cómo maneja múltiples pájaros simultáneamente?")
print("""
while run and len(birds) > 0:  # ← DECISIÓN: Continuar mientras haya sobrevivientes
    
    for x, bird in enumerate(birds):  # ← DECISIÓN: Procesar cada pájaro
        ge[x].fitness += 0.1          # ← DECISIÓN: Recompensar supervivencia
        bird.move()                   # ← DECISIÓN: Física para todos
        
        # LA PARTE MÁS IMPORTANTE:
        output = nets[birds.index(bird)].activate(
            (bird.y, 
             abs(bird.y - pipes[pipe_ind].height), 
             abs(bird.y - pipes[pipe_ind].bottom))
        )
        
        if output[0] > 0.5:
            bird.jump()

PENSAMIENTO DEL PROGRAMADOR:
"Cada pájaro necesita:
 1. Información de su situación actual
 2. Su cerebro procesa esa información
 3. Toma una decisión basada en el resultado
 4. Ejecuta esa decisión en el mundo físico"
""")

print("\n💀 LÍNEAS 275-281: MANEJO DE COLISIONES")
print("¿Cómo elimina a los pájaros que fallan?")
print("""
for pipe in pipes:
    for bird in birds:
        if pipe.collide(bird, win):
            ge[birds.index(bird)].fitness -= 1  # ← DECISIÓN: Castigar errores
            nets.pop(birds.index(bird))         # ← DECISIÓN: Eliminar cerebro
            ge.pop(birds.index(bird))           # ← DECISIÓN: Eliminar DNA
            birds.pop(birds.index(bird))        # ← DECISIÓN: Eliminar cuerpo

PENSAMIENTO DEL PROGRAMADOR:
"Cuando un pájaro muere, debo:
 1. Castigarlo reduciendo su fitness
 2. Eliminar TODAS sus referencias de TODAS las listas
 3. Mantener las listas sincronizadas"
""")

print("\n🏆 LÍNEAS 290-294: SISTEMA DE RECOMPENSAS")
print("¿Cómo premia el éxito?")
print("""
if add_pipe:  # ← Cuando se pasa una tubería
    score += 1
    for genome in ge:  # ← DECISIÓN: Todos los supervivientes se benefician
        genome.fitness += 5

PENSAMIENTO DEL PROGRAMADOR:
"Pasar una tubería es un logro mayor que solo sobrevivir.
 Le doy 5 puntos vs 0.1 por frame.
 Esto significa que pasar 1 tubería = sobrevivir 50 frames"
""")

print("\n🧠 DECISIONES DE DISEÑO CLAVE:")
print("""
1. ENTRADAS DE LA RED NEURONAL:
   - bird.y: Posición absoluta
   - abs(bird.y - pipes[pipe_ind].height): Distancia al centro
   - abs(bird.y - pipes[pipe_ind].bottom): Distancia al borde
   
   ¿Por qué estas 3?
   - La IA necesita saber dónde está
   - Necesita saber dónde apuntar
   - Necesita saber qué evitar

2. UMBRAL DE DECISIÓN:
   - if output[0] > 0.5: saltar
   
   ¿Por qué 0.5?
   - Es el punto medio entre -1 y 1 (rango de tanh)
   - Permite decisiones balanceadas

3. SISTEMA DE FITNESS:
   - +0.1 por sobrevivir
   - +5.0 por pasar tubería
   - -1.0 por chocar
   
   ¿Por qué estos valores?
   - Supervivencia importa, pero el progreso importa más
   - Los errores deben tener consecuencias
""")

print("\n🎯 RESULTADO DEL DISEÑO:")
print("Un sistema donde cada pájaro:")
print("1. Recibe información sensorial")
print("2. Procesa con su cerebro único")
print("3. Toma decisiones autónomas")
print("4. Es evaluado objetivamente")
print("5. Contribuye a la evolución del grupo")
