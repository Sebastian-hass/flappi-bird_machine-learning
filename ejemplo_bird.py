# EJEMPLO VISUAL: ¿Cómo funciona la clase Bird?

class Bird:
    def __init__(self, x, y):
        print(f"🐦 Creando pájaro en posición ({x}, {y})")
        self.x = x          # Posición horizontal (nunca cambia)
        self.y = y          # Posición vertical (sube y baja)
        self.vel = 0        # Velocidad (negativa=sube, positiva=baja)
        self.tick_count = 0 # Tiempo desde último salto
    
    def jump(self):
        print("🚀 ¡SALTO! Velocidad inicial: -10.5")
        self.vel = -10.5    # Impulso hacia arriba
        self.tick_count = 0 # Reiniciar contador
    
    def move(self):
        self.tick_count += 1
        
        # FÍSICA: distancia = velocidad_inicial * tiempo + 0.5 * gravedad * tiempo²
        displacement = self.vel * self.tick_count + 0.5 * 3 * (self.tick_count ** 2)
        
        print(f"Frame {self.tick_count}: desplazamiento = {displacement:.1f}")
        
        # Aplicar el movimiento
        self.y = self.y + displacement
        print(f"Nueva posición Y: {self.y:.1f}")

# DEMO: Veamos qué pasa cuando un pájaro salta
print("=== SIMULACIÓN DE SALTO ===")
pajaro = Bird(100, 400)  # Crear pájaro en x=100, y=400

pajaro.jump()           # Saltar
for frame in range(8):  # Simular 8 frames
    print(f"\n--- Frame {frame+1} ---")
    pajaro.move()
