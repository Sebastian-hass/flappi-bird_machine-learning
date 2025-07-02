# EJEMPLO VISUAL: ¿Cómo decide la red neuronal?

import random
import math

class RedNeuronalSimple:
    """Red neuronal súper simple para entender el concepto"""
    
    def __init__(self):
        # Pesos aleatorios iniciales (esto es lo que NEAT evoluciona)
        self.peso1 = random.uniform(-1, 1)  # Para posición del pájaro
        self.peso2 = random.uniform(-1, 1)  # Para distancia al hueco
        self.peso3 = random.uniform(-1, 1)  # Para distancia al suelo de tubería
        self.bias = random.uniform(-1, 1)   # Sesgo
        
        print(f"🧠 Red creada con pesos:")
        print(f"   Peso1 (posición): {self.peso1:.2f}")
        print(f"   Peso2 (hueco): {self.peso2:.2f}")
        print(f"   Peso3 (suelo tubería): {self.peso3:.2f}")
        print(f"   Bias: {self.bias:.2f}")
    
    def tanh(self, x):
        """Función de activación tanh (convierte cualquier número a -1 a 1)"""
        return math.tanh(x)
    
    def decidir(self, pos_pajaro, dist_hueco, dist_suelo):
        """Toma la decisión: ¿saltar o no?"""
        
        print(f"\n📥 ENTRADAS:")
        print(f"   Posición pájaro: {pos_pajaro}")
        print(f"   Distancia al hueco: {dist_hueco}")
        print(f"   Distancia al suelo tubería: {dist_suelo}")
        
        # PASO 1: Multiplicar entradas por pesos
        calc1 = pos_pajaro * self.peso1
        calc2 = dist_hueco * self.peso2
        calc3 = dist_suelo * self.peso3
        
        print(f"\n🔢 CÁLCULOS:")
        print(f"   {pos_pajaro} × {self.peso1:.2f} = {calc1:.2f}")
        print(f"   {dist_hueco} × {self.peso2:.2f} = {calc2:.2f}")
        print(f"   {dist_suelo} × {self.peso3:.2f} = {calc3:.2f}")
        
        # PASO 2: Sumar todo + bias
        suma = calc1 + calc2 + calc3 + self.bias
        print(f"   Suma total: {suma:.2f}")
        
        # PASO 3: Aplicar función de activación
        resultado = self.tanh(suma)
        print(f"   Después de tanh: {resultado:.2f}")
        
        # PASO 4: Decidir basado en el resultado
        if resultado > 0.5:
            decision = "🚀 SALTAR"
        else:
            decision = "⬇️ NO SALTAR"
            
        print(f"\n🎯 DECISIÓN: {decision}")
        return resultado > 0.5

# DEMO: Simulemos diferentes situaciones
print("=== SIMULACIÓN DE DECISIONES ===")
red = RedNeuronalSimple()

print("\n" + "="*50)
print("SITUACIÓN 1: Pájaro alto, tubería lejos")
red.decidir(pos_pajaro=100, dist_hueco=300, dist_suelo=400)

print("\n" + "="*50)
print("SITUACIÓN 2: Pájaro bajo, tubería cerca")
red.decidir(pos_pajaro=600, dist_hueco=50, dist_suelo=100)

print("\n" + "="*50)
print("SITUACIÓN 3: Pájaro en medio, tubería media distancia")
red.decidir(pos_pajaro=350, dist_hueco=150, dist_suelo=200)
