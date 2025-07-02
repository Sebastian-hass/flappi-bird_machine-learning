# Flappy Bird AI con NEAT

Este proyecto implementa una IA que aprende a jugar Flappy Bird usando el algoritmo NEAT (NeuroEvolution of Augmenting Topologies).

## Estructura del Proyecto

```
flappi-bird_machine-learning/
├── images/                 # Imágenes del juego (bird1.png, bird2.png, bird3.png, pipe.png, base.png, bg.png)
├── saved_models/           # Modelos entrenados guardados
├── main.py                # Archivo principal para ejecutar
├── flappy_bird.py         # Lógica del juego y integración con NEAT
├── config-feedforward.txt # Configuración del algoritmo NEAT
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Para entrenar la IA:
```bash
python main.py
```

## Cómo Funciona

### Red Neuronal
- **Entradas (3)**: 
  - Posición Y del pájaro
  - Distancia al hueco de la tubería (altura)
  - Distancia al borde inferior de la tubería
- **Salida (1)**: Decisión de saltar (>0.5) o no saltar (<=0.5)

### Algoritmo NEAT
- **Población**: 20 individuos por generación
- **Fitness**: Basado en la distancia recorrida y tuberías pasadas
- **Generaciones**: Máximo 50 generaciones
- **Función de activación**: tanh

### Parámetros del Juego
- **Ventana**: 600x800 píxeles
- **Velocidad**: 30 FPS
- **Gap entre tuberías**: 200 píxeles
- **Velocidad de tuberías**: 5 píxeles/frame

## Personalización

Puedes modificar los parámetros en:
- `config-feedforward.txt`: Configuración del algoritmo NEAT
- `flappy_bird.py`: Parámetros del juego (velocidad, tamaño, etc.)

## Requisitos de Imágenes

Asegúrate de tener las siguientes imágenes en la carpeta `images/`:
- `bird1.png`, `bird2.png`, `bird3.png`: Frames de animación del pájaro
- `pipe.png`: Imagen de la tubería
- `base.png`: Imagen del suelo
- `bg.png`: Imagen de fondo

## Resultados

Durante el entrenamiento verás:
- **Score**: Puntuación actual
- **Gens**: Número de generación actual
- **Alive**: Número de pájaros vivos en la generación

El mejor genoma se mostrará al final del entrenamiento.
