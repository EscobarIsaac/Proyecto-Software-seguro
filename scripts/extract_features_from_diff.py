#!/usr/bin/env python3
"""
Script para extraer características de cambios en commits/pull requests
Analiza las diferencias de código para detectar vulnerabilidades introducidas
"""

import subprocess
import re
import pandas as pd
import os
import sys


def get_git_diff():
    """Obtiene las diferencias del último commit o cambios staged"""
    try:
        # Intentar obtener diff del último commit
        result = subprocess.run(["git", "diff", "HEAD~1", "HEAD"],
                                capture_output=True,
                                text=True,
                                check=True)
        if result.stdout.strip():
            return result.stdout

        # Si no hay diff en commit, obtener cambios staged
        result = subprocess.run(["git", "diff", "--cached"],
                                capture_output=True,
                                text=True,
                                check=True)
        if result.stdout.strip():
            return result.stdout

        # Si no hay cambios staged, obtener cambios no staged
        result = subprocess.run(["git", "diff"],
                                capture_output=True,
                                text=True,
                                check=True)
        return result.stdout

    except subprocess.CalledProcessError:
        print("⚠️ No se pudo obtener git diff. Usando archivos de ejemplo...")
        return ""


def extract_added_lines(diff_content):
    """Extrae líneas agregadas del diff"""
    added_lines = []

    for line in diff_content.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            # Remover el '+' del inicio y limpiar
            code_line = line[1:].strip()
            if code_line:  # Ignorar líneas vacías
                added_lines.append(code_line)

    return added_lines


def analyze_code_changes(added_lines):
    """Analiza las líneas de código agregadas buscando patrones de vulnerabilidades"""

    if not added_lines:
        print("ℹ️ No se encontraron líneas agregadas para analizar")
        return []

    results = []

    for i, line in enumerate(added_lines):
        line_lower = line.lower()

        # Extraer características usando la misma función que en preprocesar_vulnerabilidades.py
        features = extract_line_features(line)

        # Añadir información de contexto
        features.update({
            'line_number': i + 1,
            'original_line': line[:100],  # Limitar para logging
        })

        results.append(features)

    return results


def extract_line_features(code_line):
    """Extrae características de una línea de código individual"""
    text = str(code_line).lower()

    # Características básicas
    length = len(text)
    num_semi = text.count(";")
    num_equal = text.count("=")

    # Patrones de riesgo específicos
    sql_patterns = [
        "select", "insert", "update", "delete", "union", "drop", "alter"
    ]
    sql_risk = sum([text.count(pattern) for pattern in sql_patterns])

    xss_patterns = [
        "alert", "document", "innerhtml", "script", "eval", "settimeout"
    ]
    xss_risk = sum([text.count(pattern) for pattern in xss_patterns])

    # Concatenación insegura
    concat_risk = text.count("' +") + text.count('" +') + text.count(
        "+ '") + text.count('+ "')

    # Funciones peligrosas
    dangerous_funcs = ["gets", "strcpy", "sprintf", "strcat", "system", "exec"]
    dangerous_count = sum([text.count(func) for func in dangerous_funcs])

    # Patrones de inyección
    injection_patterns = ["where", "from", "into", "values"]
    injection_risk = sum(
        [text.count(pattern) for pattern in injection_patterns])

    # Calcular score de riesgo general
    risk_score = (sql_risk * 2) + (xss_risk * 2) + (concat_risk * 3) + (
        dangerous_count * 4) + injection_risk

    return {
        'len': length,
        'num_lines': 1,  # Es una línea individual
        'num_semi': num_semi,
        'num_if': text.count("if"),
        'num_for': text.count("for"),
        'num_while': text.count("while"),
        'num_equal': num_equal,
        'sql_risk': sql_risk,
        'xss_risk': xss_risk,
        'concat_risk': concat_risk,
        'dangerous_count': dangerous_count,
        'injection_risk': injection_risk,
        'risk_score': risk_score
    }


def save_analysis_results(results):
    """Guarda los resultados del análisis para usar con el modelo"""

    if not results:
        print("ℹ️ No hay resultados para guardar")
        return

    # Crear DataFrame
    df = pd.DataFrame(results)

    # Crear directorio de reportes
    os.makedirs("reports", exist_ok=True)

    # Guardar características para el modelo (sin label, será predicha)
    feature_columns = [
        'len', 'num_lines', 'num_semi', 'num_if', 'num_for', 'num_while',
        'num_equal', 'sql_risk', 'xss_risk', 'concat_risk', 'dangerous_count',
        'injection_risk'
    ]

    # Agregar score promedio como última característica
    mean_score = 5.52572202166065  # Usar el mismo valor que en entrenamiento

    features_df = df[feature_columns].copy()
    features_df['score'] = mean_score

    # Guardar para que el modelo lo pueda usar
    features_df.to_csv("diff_features.csv", index=False, header=False)

    # Guardar reporte detallado
    detailed_report = df[['line_number', 'original_line', 'risk_score'] +
                         feature_columns]
    detailed_report.to_csv("reports/diff_analysis.csv", index=False)

    # Crear resumen JSON
    high_risk_lines = df[df['risk_score'] > 5]
    medium_risk_lines = df[(df['risk_score'] > 2) & (df['risk_score'] <= 5)]

    summary = {
        "total_lines_analyzed":
        len(df),
        "high_risk_lines":
        len(high_risk_lines),
        "medium_risk_lines":
        len(medium_risk_lines),
        "max_risk_score":
        float(df['risk_score'].max()) if len(df) > 0 else 0,
        "avg_risk_score":
        float(df['risk_score'].mean()) if len(df) > 0 else 0,
        "risky_lines": [{
            "line": row['original_line'],
            "risk_score": float(row['risk_score']),
            "line_number": int(row['line_number'])
        } for _, row in high_risk_lines.iterrows()]
    }

    import json
    with open("reports/diff_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"📄 Análisis completado:")
    print(f"   - {len(df)} líneas analizadas")
    print(f"   - {len(high_risk_lines)} líneas de alto riesgo")
    print(f"   - {len(medium_risk_lines)} líneas de riesgo medio")

    return "diff_features.csv"


def main():
    """Función principal para análisis de diferencias Git"""

    print("🔍 Analizando cambios en el código...")

    # Obtener diferencias de Git
    diff_content = get_git_diff()

    if not diff_content.strip():
        print("ℹ️ No se encontraron cambios. Creando archivo de ejemplo...")
        # Crear un ejemplo de características para testing
        example_features = [
            42, 1, 1, 0, 0, 0, 2, 1, 0, 2, 0, 1, 5.52572202166065
        ]
        pd.DataFrame([example_features]).to_csv("diff_features.csv",
                                                index=False,
                                                header=False)
        return "diff_features.csv"

    # Extraer líneas agregadas
    added_lines = extract_added_lines(diff_content)

    if not added_lines:
        print("ℹ️ No se encontraron líneas nuevas agregadas")
        return None

    # Analizar cambios
    results = analyze_code_changes(added_lines)

    # Guardar resultados
    return save_analysis_results(results)


if __name__ == "__main__":
    output_file = main()
    if output_file:
        print(f"✅ Características guardadas en {output_file}")
    else:
        print("❌ No se pudieron extraer características")
        sys.exit(1)
