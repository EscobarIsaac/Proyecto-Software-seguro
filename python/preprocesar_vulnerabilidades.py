import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from pathlib import Path

# 1. Cargar datasets (desde carpeta csvs)
CSV_DIR = Path(__file__).resolve().parent.parent / "csvs"
code_df = pd.read_csv(CSV_DIR / "code_vulnerabilities.csv")
meta_df = pd.read_csv(CSV_DIR / "all_c_cpp_release2.0.csv")

# 2. Limpiar nombres de columnas esperados
# Ajusta si tus columnas tienen nombres algo distintos
code_col = "Code Snippet"
type_col = "Vulnerability Type"

# 3. Codificar etiqueta binaria: 1 = vulnerable, 0 = no vulnerable
# En este dataset ambos tipos son vulnerables, así que usaremos:
# 1 = SQLi, 0 = XSS, solo como ejemplo de clasificación binaria.
code_df[type_col] = code_df[type_col].str.strip()
code_df["label"] = (code_df[type_col] == "SQLi").astype(int)


# 4. Extraer features avanzadas para detectar patrones de riesgo
def extract_features(snippet: str):
    text = str(snippet).lower()

    # Características básicas
    length = len(text)
    num_lines = text.count("\n") + 1
    num_semi = text.count(";")
    num_if = text.count("if")
    num_for = text.count("for")
    num_while = text.count("while")
    num_equal = text.count("=")

    # Patrones de riesgo específicos para vulnerabilidades
    # SQL Injection patterns
    sql_patterns = [
        "select", "insert", "update", "delete", "union", "drop", "alter"
    ]
    sql_risk = sum([text.count(pattern) for pattern in sql_patterns])

    # XSS patterns
    xss_patterns = [
        "alert", "document", "innerhtml", "script", "eval", "settimeout"
    ]
    xss_risk = sum([text.count(pattern) for pattern in xss_patterns])

    # Concatenación insegura (patrón común en ambas vulnerabilidades)
    concat_risk = text.count("' +") + text.count('" +') + text.count(
        "+ '") + text.count('+ "')

    # Funciones deprecated o peligrosas
    dangerous_funcs = ["gets", "strcpy", "sprintf", "strcat", "system", "exec"]
    dangerous_count = sum([text.count(func) for func in dangerous_funcs])

    # Patrones de inyección
    injection_patterns = ["where", "from", "into", "values"]
    injection_risk = sum(
        [text.count(pattern) for pattern in injection_patterns])

    return pd.Series(
        [
            length, num_lines, num_semi, num_if, num_for, num_while, num_equal,
            sql_risk, xss_risk, concat_risk, dangerous_count, injection_risk
        ],
        index=[
            "len", "num_lines", "num_semi", "num_if", "num_for", "num_while",
            "num_equal", "sql_risk", "xss_risk", "concat_risk",
            "dangerous_count", "injection_risk"
        ],
    )


features = code_df[code_col].apply(extract_features)

# 5. (Opcional) unir alguna columna numérica de all_c_cpp_release2.0.csv
# Aquí se muestra cómo añadir el 'score' medio como ejemplo simple.
# Si tienes alguna clave común (por ejemplo cve_id) puedes hacer un merge real.
if "score" in meta_df.columns:
    # Usamos el score medio para todo, solo para tener una columna extra numérica.
    mean_score = meta_df["score"].fillna(0).mean()
    features["score"] = mean_score
else:
    features["score"] = 0.0

# 6. Construir matriz final: features + label al final (como espera mlpack)
final_df = features.copy()
final_df["label"] = code_df["label"]

# 7. Dividir en train y test
train_df, test_df = train_test_split(
    final_df,
    test_size=0.2,
    random_state=42,
    shuffle=True,
)

# 8. Guardar en CSV sin cabecera (para que mlpack lea solo números)
train_df.to_csv(CSV_DIR / "train_features.csv", index=False, header=False)
test_df.to_csv(CSV_DIR / "test_features.csv", index=False, header=False)
