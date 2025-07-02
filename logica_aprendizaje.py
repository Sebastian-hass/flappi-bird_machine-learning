"""
LÓGICA DE APRENDIZAJE: Cómo funciona NEAT paso a paso

El programador implementó un ciclo evolutivo que imita la selección natural:
"""

print("🧬 LÓGICA DE APRENDIZAJE - PROCESO PASO A PASO")
print("="*60)

print("\n🎯 PASO 1: CREAR POBLACIÓN INICIAL")
print("Pregunta: ¿Cómo empezamos?")
print("Respuesta: Crear 20 pájaros con 'cerebros' aleatorios")
print("""
# En el código:
nets = []     # Lista de 'cerebros' (redes neuronales)
birds = []    # Lista de pájaros físicos
ge = []       # Lista de 'DNA' (genomas)

for genome_id, genome in genomes:
    genome.fitness = 0  # Todos empiezan con puntuación 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)  # Crear 'cerebro'
    nets.append(net)           # Agregar cerebro a la lista
    birds.append(Bird(230,350)) # Crear pájaro físico
    ge.append(genome)          # Agregar DNA a la lista
""")

print("\n🎮 PASO 2: SIMULAR EL JUEGO")
print("Pregunta: ¿Cómo jugamos?")
print("Respuesta: Cada pájaro juega usando su propio cerebro")
print("""
# Bucle principal del juego:
while run and len(birds) > 0:  # Mientras haya pájaros vivos
    
    for x, bird in enumerate(birds):  # Para cada pájaro:
        
        # 2.1: DAR INFORMACIÓN AL CEREBRO
        inputs = (bird.y,                              # Dónde estoy
                 abs(bird.y - pipes[pipe_ind].height), # Distancia al hueco
                 abs(bird.y - pipes[pipe_ind].bottom))  # Distancia al suelo
        
        # 2.2: EL CEREBRO DECIDE
        output = nets[birds.index(bird)].activate(inputs)
        
        # 2.3: EJECUTAR LA DECISIÓN
        if output[0] > 0.5:  # Si el cerebro dice "salta"
            bird.jump()      # Ejecutar el salto
""")

print("\n📊 PASO 3: SISTEMA DE PUNTUACIÓN (FITNESS)")
print("Pregunta: ¿Cómo medimos qué tan bien lo hace cada pájaro?")
print("Respuesta: Sistema de recompensas y castigos")
print("""
# Recompensas (aumentan fitness):
ge[x].fitness += 0.1        # Por cada frame que sobrevive
genome.fitness += 5         # Por cada tubería que pasa

# Castigos (reducen fitness):
ge[birds.index(bird)].fitness -= 1  # Por chocar

# Muerte (eliminación):
if pipe.collide(bird, win):  # Si choca
    nets.pop(birds.index(bird))     # Eliminar cerebro
    ge.pop(birds.index(bird))       # Eliminar DNA
    birds.pop(birds.index(bird))    # Eliminar pájaro físico
""")

print("\n🔄 PASO 4: EVOLUCIÓN ENTRE GENERACIONES")
print("Pregunta: ¿Cómo mejoran los pájaros?")
print("Respuesta: NEAT maneja automáticamente la evolución")
print("""
# En función run():
winner = p.run(eval_genomes, 50)  # Ejecutar 50 generaciones

# NEAT automáticamente:
# 1. Evalúa el fitness de todos los genomas
# 2. Selecciona los mejores para reproducción
# 3. Crea variaciones (mutaciones) de los mejores
# 4. Forma la nueva generación
# 5. Repite el proceso
""")

print("\n🎯 PASO 5: PROCESO MENTAL DEL PROGRAMADOR")
print("¿Cómo diseñó el sistema de aprendizaje?")
print("""
PROBLEMA: "¿Cómo hacer que aprendan sin programar las reglas?"
SOLUCIÓN: "Usar selección natural artificial"

DISEÑO:
1. Crear muchos intentos diferentes
2. Medir qué tan bien lo hace cada uno
3. Los mejores se reproducen
4. Agregar variaciones aleatorias
5. Repetir hasta obtener expertos

IMPLEMENTACIÓN:
- eval_genomes(): Evalúa una generación completa
- Sistema de fitness: Mide el desempeño
- NEAT: Maneja la evolución automáticamente
- Bucle principal: Conecta todo junto
""")

print("\n🚀 RESULTADO:")
print("Un sistema que mejora automáticamente sin intervención humana")
print("¡La computadora aprende estrategias que ni siquiera el programador imaginó!")
