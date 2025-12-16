#!/usr/bin/env python3
"""
API Flask para análisis de vulnerabilidades en producción
Proyecto: Pipeline CI/CD Seguro con ML
"""

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Variable global para el modelo
model = None
feature_names = [
    "length", "num_lines", "num_semi", "num_if", "num_for", "num_while",
    "num_equal", "sql_risk", "xss_risk", "concat_risk", "dangerous_count",
    "injection_risk", "score"
]

def load_model():
    """Carga y entrena el modelo al iniciar la aplicación"""
    global model
    try:
        if os.path.exists("train_features.csv"):
            train_df = pd.read_csv("train_features.csv", header=None)
            X = train_df.iloc[:, :-1]
            y = train_df.iloc[:, -1]
            
            model = RandomForestClassifier(
                n_estimators=50,
                min_samples_leaf=5,
                random_state=42
            )
            model.fit(X, y)
            logging.info("✅ Modelo cargado y entrenado exitosamente")
        else:
            logging.warning("⚠️ No se encontró train_features.csv, usando modelo mock")
            model = None
    except Exception as e:
        logging.error(f"❌ Error cargando modelo: {e}")
        model = None

def extract_features(code_snippet):
    """Extrae características de un snippet de código"""
    text = str(code_snippet).lower()
    
    # Características básicas
    length = len(text)
    num_lines = text.count("\n") + 1
    num_semi = text.count(";")
    num_if = text.count("if")
    num_for = text.count("for")
    num_while = text.count("while")
    num_equal = text.count("=")
    
    # Patrones de riesgo SQL
    sql_patterns = ["select", "insert", "update", "delete", "union", "drop", "alter"]
    sql_risk = sum([text.count(pattern) for pattern in sql_patterns])
    
    # Patrones XSS
    xss_patterns = ["alert", "document", "innerhtml", "script", "eval", "settimeout"]
    xss_risk = sum([text.count(pattern) for pattern in xss_patterns])
    
    # Concatenación insegura
    concat_risk = text.count("' +") + text.count('" +') + text.count("+ '") + text.count('+ "')
    
    # Funciones peligrosas
    dangerous_funcs = ["gets", "strcpy", "sprintf", "strcat", "system", "exec"]
    dangerous_count = sum([text.count(func) for func in dangerous_funcs])
    
    # Patrones de inyección
    injection_patterns = ["where", "from", "into", "values"]
    injection_risk = sum([text.count(pattern) for pattern in injection_patterns])
    
    # Score promedio
    score = 5.52572202166065
    
    return [length, num_lines, num_semi, num_if, num_for, num_while, 
            num_equal, sql_risk, xss_risk, concat_risk, dangerous_count, 
            injection_risk, score]

@app.route('/')
def home():
    """Página principal con interfaz web"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔒 Analizador de Vulnerabilidades ML</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            textarea {
                width: 100%;
                min-height: 200px;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                resize: vertical;
                margin-bottom: 20px;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            #result {
                margin-top: 30px;
                padding: 20px;
                border-radius: 10px;
                display: none;
            }
            .vulnerable {
                background: #fee;
                border-left: 5px solid #f44336;
            }
            .safe {
                background: #efe;
                border-left: 5px solid #4caf50;
            }
            .warning {
                background: #fff3cd;
                border-left: 5px solid #ff9800;
            }
            .result-title {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .metric {
                background: #f5f5f5;
                padding: 15px;
                border-radius: 8px;
            }
            .metric-label {
                color: #666;
                font-size: 0.9em;
                margin-bottom: 5px;
            }
            .metric-value {
                font-size: 1.5em;
                font-weight: bold;
                color: #333;
            }
            .info-box {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                border-left: 5px solid #2196f3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 Analizador de Vulnerabilidades</h1>
            <p class="subtitle">Sistema de detección automática con Machine Learning</p>
            
            <textarea id="codeInput" placeholder="Pega tu código aquí para análisis de vulnerabilidades...&#10;&#10;Ejemplo:&#10;user_input = request.GET['id']&#10;query = 'SELECT * FROM users WHERE id = ' + user_input&#10;cursor.execute(query)"></textarea>
            
            <button onclick="analyzeCode()">🔍 Analizar Código</button>
            
            <div id="result"></div>
            
            <div class="info-box">
                <strong>💡 API Endpoints disponibles:</strong><br>
                • <code>GET /</code> - Esta interfaz web<br>
                • <code>GET /health</code> - Estado del servicio<br>
                • <code>POST /analyze</code> - Análisis de código (JSON)<br>
                • <code>GET /stats</code> - Estadísticas del modelo
            </div>
        </div>
        
        <script>
            async function analyzeCode() {
                const code = document.getElementById('codeInput').value;
                const resultDiv = document.getElementById('result');
                
                if (!code.trim()) {
                    alert('Por favor ingresa código para analizar');
                    return;
                }
                
                resultDiv.innerHTML = '<p style="text-align:center;">⏳ Analizando código...</p>';
                resultDiv.style.display = 'block';
                resultDiv.className = '';
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ code: code })
                    });
                    
                    const data = await response.json();
                    
                    let className = 'safe';
                    let icon = '✅';
                    let title = 'Código Seguro';
                    
                    if (data.alert_level === 'CRITICA') {
                        className = 'vulnerable';
                        icon = '🚨';
                        title = 'ALERTA CRÍTICA';
                    } else if (data.alert_level === 'MEDIA') {
                        className = 'warning';
                        icon = '⚠️';
                        title = 'Advertencia';
                    }
                    
                    resultDiv.className = className;
                    resultDiv.innerHTML = `
                        <div class="result-title">${icon} ${title}</div>
                        <p>${data.message}</p>
                        <div class="metrics">
                            <div class="metric">
                                <div class="metric-label">Probabilidad Vulnerable</div>
                                <div class="metric-value">${(data.prob_vulnerable * 100).toFixed(1)}%</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Probabilidad Seguro</div>
                                <div class="metric-value">${(data.prob_safe * 100).toFixed(1)}%</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Clasificación</div>
                                <div class="metric-value">${data.prediction === 1 ? 'VULNERABLE' : 'SEGURO'}</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Nivel de Alerta</div>
                                <div class="metric-value">${data.alert_level}</div>
                            </div>
                        </div>
                        ${data.patterns_detected.length > 0 ? `
                        <div style="margin-top: 20px;">
                            <strong>🔍 Patrones detectados:</strong>
                            <ul style="margin-top: 10px; margin-left: 20px;">
                                ${data.patterns_detected.map(p => `<li>${p}</li>`).join('')}
                            </ul>
                        </div>
                        ` : ''}
                    `;
                } catch (error) {
                    resultDiv.className = 'vulnerable';
                    resultDiv.innerHTML = '<div class="result-title">❌ Error</div><p>Error al analizar el código. Intenta nuevamente.</p>';
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud para monitoreo"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "service": "Vulnerability Detection API",
        "version": "1.0.0"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint principal para análisis de código"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                "error": "Se requiere el campo 'code' en el JSON"
            }), 400
        
        code = data['code']
        
        # Extraer características
        features = extract_features(code)
        X = np.array([features])
        
        # Predicción
        if model is not None:
            prediction = model.predict(X)[0]
            probabilities = model.predict_proba(X)[0]
            prob_safe = float(probabilities[0])
            prob_vulnerable = float(probabilities[1])
        else:
            # Modo mock si no hay modelo
            prediction = 1 if any(p in code.lower() for p in ['select', 'insert', 'eval', 'exec']) else 0
            prob_vulnerable = 0.85 if prediction == 1 else 0.15
            prob_safe = 1 - prob_vulnerable
        
        # Determinar nivel de alerta
        if prob_vulnerable > 0.70:
            alert_level = "CRITICA"
            message = "Alta probabilidad de vulnerabilidad detectada. Se requiere revisión inmediata."
        elif prob_vulnerable > 0.50:
            alert_level = "MEDIA"
            message = "Posible vulnerabilidad detectada. Se recomienda revisión manual."
        else:
            alert_level = "BAJA"
            message = "Código seguro. Baja probabilidad de vulnerabilidad."
        
        # Detectar patrones específicos
        patterns_detected = []
        code_lower = code.lower()
        
        if any(p in code_lower for p in ['select', 'insert', 'update', 'delete']):
            patterns_detected.append("Patrones SQL detectados")
        if any(p in code_lower for p in ['alert', 'document', 'innerhtml', 'eval']):
            patterns_detected.append("Patrones XSS detectados")
        if "' +" in code or '" +' in code:
            patterns_detected.append("Concatenación insegura de strings")
        if any(f in code_lower for f in ['gets', 'strcpy', 'system', 'exec']):
            patterns_detected.append("Funciones peligrosas/deprecated")
        
        return jsonify({
            "prediction": int(prediction),
            "prob_vulnerable": prob_vulnerable,
            "prob_safe": prob_safe,
            "alert_level": alert_level,
            "message": message,
            "patterns_detected": patterns_detected,
            "features": dict(zip(feature_names, features))
        })
    
    except Exception as e:
        logging.error(f"Error en /analyze: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Estadísticas del modelo"""
    if model is not None:
        return jsonify({
            "model_type": "RandomForestClassifier",
            "n_estimators": 50,
            "features": feature_names,
            "n_features": len(feature_names),
            "trained": True
        })
    else:
        return jsonify({
            "model_type": "Mock",
            "trained": False,
            "message": "Modelo en modo demo"
        })

# Cargar modelo al iniciar
load_model()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
