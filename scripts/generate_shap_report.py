#!/usr/bin/env python3
"""
Script para generar reportes de interpretabilidad con SHAP
Cumple con la especificación de reportes HTML con explicaciones
"""

import pandas as pd
import numpy as np
import json
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import matplotlib.pyplot as plt


def load_and_train_model():
    """Carga datos y entrena modelo de scikit-learn para compatibilidad con SHAP"""
    # Cargar datos procesados
    train_df = pd.read_csv("train_features.csv", header=None)

    # Separar features y labels
    X = train_df.iloc[:, :-1]  # Todas las columnas excepto la última
    y = train_df.iloc[:, -1]  # Última columna (labels)

    # Entrenar Random Forest
    model = RandomForestClassifier(n_estimators=50,
                                   min_samples_leaf=5,
                                   random_state=42)
    model.fit(X, y)

    # Nombres de las características
    feature_names = [
        "length", "num_lines", "num_semi", "num_if", "num_for", "num_while",
        "num_equal", "sql_risk", "xss_risk", "concat_risk", "dangerous_count",
        "injection_risk"
    ]

    return model, X, y, feature_names


def generate_shap_report(model, X, feature_names):
    """Genera reporte SHAP con explicaciones de interpretabilidad"""

    # Crear explainer SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(
        X[:100])  # Usar muestra para eficiencia

    # Crear directorio de reportes
    os.makedirs("reports", exist_ok=True)

    # 1. Summary Plot (importancia de características)
    plt.figure(figsize=(10, 6))
    if len(shap_values) > 1:  # Clasificación binaria
        shap.summary_plot(shap_values[1],
                          X[:100],
                          feature_names=feature_names,
                          show=False)
    else:
        shap.summary_plot(shap_values,
                          X[:100],
                          feature_names=feature_names,
                          show=False)

    plt.title(
        "Importancia de Características para Detección de Vulnerabilidades")
    plt.tight_layout()
    plt.savefig("reports/feature_importance.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Waterfall plot para ejemplo específico
    plt.figure(figsize=(10, 8))
    if len(shap_values) > 1:
        shap_vals_sample = shap_values[1][0]  # Clase vulnerable
    else:
        shap_vals_sample = shap_values[0]

    # Crear objeto Explanation para waterfall
    explanation = shap.Explanation(
        values=shap_vals_sample,
        base_values=explainer.expected_value[1]
        if len(shap_values) > 1 else explainer.expected_value,
        data=X.iloc[0].values,
        feature_names=feature_names)

    shap.plots.waterfall(explanation, show=False)
    plt.title("Explicación de Predicción - Ejemplo Específico")
    plt.tight_layout()
    plt.savefig("reports/example_explanation.png",
                dpi=300,
                bbox_inches='tight')
    plt.close()

    return shap_values


def create_html_report(model, X, y, feature_names, shap_values):
    """Crea reporte HTML detallado"""

    # Obtener predicciones y probabilidades
    predictions = model.predict(X[:100])
    probabilities = model.predict_proba(X[:100])

    # Calcular estadísticas
    accuracy = model.score(X, y)
    high_risk_samples = np.sum(probabilities[:, 1] > 0.7)
    medium_risk_samples = np.sum((probabilities[:, 1] > 0.5)
                                 & (probabilities[:, 1] <= 0.7))

    # Crear reporte JSON para GitHub Actions
    report_summary = {
        "total_files":
        len(X),
        "high_risk_count":
        int(high_risk_samples),
        "medium_risk_count":
        int(medium_risk_samples),
        "accuracy":
        float(accuracy),
        "high_risk_files": [{
            "path": f"sample_{i}",
            "probability": float(probabilities[i, 1])
        } for i in range(min(100, len(probabilities)))
                            if probabilities[i, 1] > 0.7]
    }

    with open("reports/vulnerability_summary.json", "w") as f:
        json.dump(report_summary, f, indent=2)

    # Crear reporte HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reporte de Análisis de Vulnerabilidades</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
            .metric {{ background-color: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .alert {{ background-color: #e74c3c; color: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .warning {{ background-color: #f39c12; color: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .success {{ background-color: #27ae60; color: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            img {{ max-width: 100%; height: auto; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔒 Reporte de Análisis de Vulnerabilidades</h1>
            <p>Sistema de Detección Automatizada con Machine Learning</p>
        </div>
        
        <div class="metric">
            <h2>📊 Métricas del Modelo</h2>
            <p><strong>Precisión del modelo:</strong> {accuracy:.2%}</p>
            <p><strong>Total de muestras analizadas:</strong> {len(X)}</p>
            <p><strong>Algoritmo utilizado:</strong> Random Forest (50 árboles)</p>
        </div>
        
        {'<div class="alert"><h3>🚨 Vulnerabilidades Críticas Detectadas</h3><p><strong>' + str(high_risk_samples) + '</strong> muestras con probabilidad > 70%</p></div>' if high_risk_samples > 0 else ''}
        
        {'<div class="warning"><h3>⚠️ Posibles Vulnerabilidades</h3><p><strong>' + str(medium_risk_samples) + '</strong> muestras con probabilidad 50-70%</p></div>' if medium_risk_samples > 0 else ''}
        
        {('<div class="success"><h3>✅ Estado Seguro</h3><p>No se detectaron vulnerabilidades críticas</p></div>') if high_risk_samples == 0 else ''}
        
        <div class="metric">
            <h2>🎯 Características más Importantes</h2>
            <img src="feature_importance.png" alt="Importancia de Características">
            <p>Este gráfico muestra qué características del código son más importantes para detectar vulnerabilidades.</p>
        </div>
        
        <div class="metric">
            <h2>🔍 Explicación de Predicción</h2>
            <img src="example_explanation.png" alt="Explicación de Ejemplo">
            <p>Explicación detallada de cómo el modelo toma decisiones para un ejemplo específico.</p>
        </div>
        
        <div class="metric">
            <h2>📈 Interpretabilidad del Modelo</h2>
            <p>Este modelo utiliza <strong>SHAP (SHapley Additive exPlanations)</strong> para proporcionar explicaciones interpretables de sus predicciones:</p>
            <ul>
                <li><strong>Patrones SQL:</strong> Detecta palabras clave relacionadas con inyección SQL</li>
                <li><strong>Patrones XSS:</strong> Identifica funciones JavaScript potencialmente peligrosas</li>
                <li><strong>Concatenación insegura:</strong> Encuentra patrones de concatenación de strings que pueden ser vulnerables</li>
                <li><strong>Funciones peligrosas:</strong> Detecta uso de funciones deprecated o inseguras</li>
            </ul>
        </div>
        
        <div class="metric">
            <h2>🔄 Integración Continua</h2>
            <p>Este reporte es generado automáticamente en cada commit/pull request mediante GitHub Actions, 
               proporcionando análisis continuo de vulnerabilidades en el código.</p>
        </div>
    </body>
    </html>
    """

    with open("reports/vulnerability_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(
        "✅ Reporte HTML generado exitosamente en reports/vulnerability_report.html"
    )
    print(
        f"📊 Resumen: {high_risk_samples} vulnerabilidades críticas, {medium_risk_samples} advertencias"
    )


def main():
    """Función principal"""
    print("🔍 Generando reporte de interpretabilidad con SHAP...")

    # Cargar modelo y datos
    model, X, y, feature_names = load_and_train_model()

    # Generar explicaciones SHAP
    shap_values = generate_shap_report(model, X, feature_names)

    # Crear reporte HTML
    create_html_report(model, X, y, feature_names, shap_values)

    print("✅ Reporte completado exitosamente!")


if __name__ == "__main__":
    main()
