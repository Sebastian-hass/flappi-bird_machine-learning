"""
¿CÓMO FUNCIONA NEAT INTERNAMENTE?

El programador usa NEAT como una "caja negra" que evoluciona automáticamente.
Pero ¿qué pasa dentro de esa caja?
"""

print("🧬 CÓMO FUNCIONA NEAT INTERNAMENTE")
print("="*50)

print("\n🔄 EL CICLO EVOLUTIVO DE NEAT:")
print("""
GENERACIÓN 0: (20 pájaros con cerebros aleatorios)
┌─────────┬─────────┬─────────┬─────────┐
│ Pájaro1 │ Pájaro2 │ Pájaro3 │ ...     │
│ Net: ??? │ Net: ??? │ Net: ??? │ ...     │
│ Fit: 0   │ Fit: 0   │ Fit: 0   │ ...     │
└─────────┴─────────┴─────────┴─────────┘
         ↓
    JUEGAN FLAPPY BIRD
         ↓
┌─────────┬─────────┬─────────┬─────────┐
│ Pájaro1 │ Pájaro2 │ Pájaro3 │ ...     │
│ Net: ??? │ Net: ??? │ Net: ??? │ ...     │
│ Fit: 2.3 │ Fit: 15.7│ Fit: 0.8│ ...     │
└─────────┴─────────┴─────────┴─────────┘
         ↓
    NEAT EVALÚA Y EVOLUCIONA
         ↓
GENERACIÓN 1: (Nuevos pájaros basados en los mejores)
""")

print("\n🏆 PROCESO DE SELECCIÓN:")
print("""
1. NEAT ordena por fitness:
   Pájaro2: 15.7 ← CAMPEÓN
   Pájaro5: 12.1 ← BUENO  
   Pájaro1: 2.3  ← MEDIOCRE
   Pájaro3: 0.8  ← MALO

2. NEAT decide quién se reproduce:
   - Los mejores (fitness alto) → MÁS probabilidad de reproducirse
   - Los peores (fitness bajo) → MENOS probabilidad o eliminación

3. NEAT crea la nueva generación:
   - Copiar a los campeones (elitismo)
   - Cruzar DNA de los mejores (crossover)
   - Mutar copias para crear variedad
""")

print("\n🧬 TIPOS DE MUTACIONES QUE HACE NEAT:")
print("""
MUTACIÓN 1: CAMBIAR PESOS
Antes: Input1 --[0.5]--> Output
Después: Input1 --[0.8]--> Output  # Peso cambió de 0.5 a 0.8

MUTACIÓN 2: AGREGAR CONEXIÓN
Antes: Input1 ──────────> Output
       Input2 (no conectado)
Después: Input1 ──────────> Output
         Input2 ──[0.3]──> Output  # Nueva conexión

MUTACIÓN 3: AGREGAR NODO
Antes: Input1 --[0.5]--> Output
Después: Input1 --[0.5]--> [Nodo] --[1.0]--> Output  # Nodo en el medio

MUTACIÓN 4: CAMBIAR ACTIVACIÓN
Antes: Nodo usa función tanh
Después: Nodo usa función sigmoid
""")

print("\n🎯 ¿POR QUÉ FUNCIONA ESTO?")
print("""
PRINCIPIO CLAVE: "Selección Natural Artificial"

1. VARIEDAD: Cada pájaro tiene un cerebro diferente
2. SUPERVIVENCIA: Solo los mejores sobreviven
3. REPRODUCCIÓN: Los mejores crean descendencia
4. MUTACIÓN: Los descendientes tienen pequeños cambios
5. REPETICIÓN: El proceso se repite generación tras generación

RESULTADO: Los cerebros gradualmente se vuelven mejores en el juego
""")

print("\n🧠 DECISIONES DEL PROGRAMADOR:")
print("""
EL PROGRAMADOR SOLO TUVO QUE DECIDIR:

1. ¿Qué información darle a la IA? 
   → Posición del pájaro y tuberías

2. ¿Cómo medir el éxito?
   → Fitness por supervivencia y progreso

3. ¿Qué acción puede tomar la IA?
   → Saltar o no saltar

¡NEAT HACE TODO LO DEMÁS AUTOMÁTICAMENTE!

- Crea las redes neuronales
- Las hace evolucionar
- Maneja la reproducción
- Aplica las mutaciones
- Gestiona las especies
- Evita la convergencia prematura
""")

print("\n🎮 EJEMPLO DE EVOLUCIÓN:")
print("""
GENERACIÓN 1: "Saltar aleatoriamente"
  → Fitness promedio: 3.2

GENERACIÓN 5: "Saltar cuando hay tubería cerca"  
  → Fitness promedio: 8.7

GENERACIÓN 15: "Calcular timing básico"
  → Fitness promedio: 25.3

GENERACIÓN 30: "Estrategias sofisticadas"
  → Fitness promedio: 89.1

GENERACIÓN 50: "Expertos en Flappy Bird"
  → Fitness promedio: 150+
""")

print("\n🚀 CONCLUSIÓN:")
print("NEAT permite crear IA sin programar comportamientos específicos.")
print("El programador solo define el problema, NEAT encuentra la solución.")
print("¡Es como tener un equipo de ingenieros trabajando automáticamente!")
