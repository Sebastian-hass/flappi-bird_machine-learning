"""
Aplicación web simple para mostrar el proyecto Flappy Bird AI
Sin dependencias gráficas para deployment en servidores
"""

from flask import Flask, render_template_string, jsonify
import threading
import time
import random
import os

app = Flask(__name__)

# Estado del simulador de entrenamiento
training_state = {
    'generation': 1,
    'best_score': 0,
    'current_score': 0,
    'birds_alive': 20,
    'is_training': True,
    'total_generations': 50
}

# Template HTML simple
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flappy Bird AI - NEAT Training</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        .header {
            margin-bottom: 40px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .progress-bar {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            height: 20px;
            margin: 20px 0;
            overflow: hidden;
        }
        .progress-fill {
            background: #4CAF50;
            height: 100%;
            transition: width 0.5s ease;
        }
        .info-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            text-align: left;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            margin: 20px 0;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 Flappy Bird AI Training</h1>
            <h2>Algoritmo NEAT en vivo</h2>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Generación</h3>
                <div class="stat-value" id="generation">{{ generation }}</div>
            </div>
            <div class="stat-card">
                <h3>Mejor Puntuación</h3>
                <div class="stat-value" id="best-score">{{ best_score }}</div>
            </div>
            <div class="stat-card">
                <h3>Puntuación Actual</h3>
                <div class="stat-value" id="current-score">{{ current_score }}</div>
            </div>
            <div class="stat-card">
                <h3>Pájaros Vivos</h3>
                <div class="stat-value" id="birds-alive">{{ birds_alive }}</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ (generation / total_generations * 100) }}%"></div>
        </div>
        <p>Progreso: {{ generation }}/{{ total_generations }} generaciones</p>
        
        <button class="refresh-btn" onclick="updateStats()">🔄 Actualizar</button>
        
        <div class="info-section">
            <h3>📊 Sobre el Proyecto</h3>
            <p><strong>NEAT (NeuroEvolution of Augmenting Topologies)</strong> es un algoritmo de evolución que optimiza tanto la topología como los pesos de las redes neuronales.</p>
            
            <h4>🧠 Red Neuronal:</h4>
            <ul>
                <li><strong>Entradas (3):</strong> Posición Y del pájaro, distancia al hueco, distancia al borde inferior</li>
                <li><strong>Salida (1):</strong> Decisión de saltar (>0.5) o no saltar (≤0.5)</li>
                <li><strong>Función de activación:</strong> tanh</li>
            </ul>
            
            <h4>🎮 Parámetros del Juego:</h4>
            <ul>
                <li><strong>Población:</strong> 20 individuos por generación</li>
                <li><strong>Fitness:</strong> Basado en distancia recorrida y tuberías pasadas</li>
                <li><strong>Generaciones máximas:</strong> 50</li>
                <li><strong>Velocidad:</strong> 30 FPS</li>
            </ul>
        </div>
        
        <div class="info-section">
            <h3>🚀 Tecnologías Utilizadas</h3>
            <p><strong>Python</strong> • <strong>NEAT-Python</strong> • <strong>Pygame</strong> • <strong>Flask</strong></p>
            <p>Proyecto desarrollado para demostrar técnicas de machine learning aplicadas a videojuegos.</p>
        </div>
    </div>
    
    <script>
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('generation').textContent = data.generation;
                document.getElementById('best-score').textContent = data.best_score;
                document.getElementById('current-score').textContent = data.current_score;
                document.getElementById('birds-alive').textContent = data.birds_alive;
                
                const progressFill = document.querySelector('.progress-fill');
                progressFill.style.width = (data.generation / data.total_generations * 100) + '%';
            } catch (error) {
                console.error('Error updating stats:', error);
            }
        }
        
        // Auto-update every 2 seconds
        setInterval(updateStats, 2000);
    </script>
</body>
</html>
"""

def simulate_training():
    """Simular el proceso de entrenamiento en segundo plano"""
    while True:
        # Simular una generación de entrenamiento
        training_state['birds_alive'] = 20
        
        # Simular el proceso de vida de los pájaros
        for _ in range(random.randint(30, 100)):
            if training_state['birds_alive'] > 0:
                # Algunos pájaros mueren
                if random.random() < 0.1:
                    training_state['birds_alive'] = max(0, training_state['birds_alive'] - random.randint(1, 3))
                
                # Incrementar puntuación actual ocasionalmente
                if random.random() < 0.3:
                    training_state['current_score'] += 1
                
                time.sleep(0.5)
            else:
                break
        
        # Al final de la generación
        if training_state['current_score'] > training_state['best_score']:
            training_state['best_score'] = training_state['current_score']
        
        training_state['current_score'] = 0
        training_state['generation'] += 1
        
        # Reiniciar después de 50 generaciones
        if training_state['generation'] > training_state['total_generations']:
            training_state['generation'] = 1
            training_state['best_score'] = 0
        
        time.sleep(2)  # Pausa entre generaciones

@app.route('/')
def home():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE, **training_state)

@app.route('/api/stats')
def get_stats():
    """API para obtener estadísticas actuales"""
    return jsonify(training_state)

@app.route('/health')
def health_check():
    """Health check para el deployment"""
    return {"status": "healthy", "service": "Flappy Bird AI"}

if __name__ == '__main__':
    # Iniciar simulador en segundo plano
    training_thread = threading.Thread(target=simulate_training, daemon=True)
    training_thread.start()
    
    # Configurar puerto para deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
