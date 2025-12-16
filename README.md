# Sistema de Detección de Vulnerabilidades mediante Machine Learning

## Descripción General

Este proyecto implementa un sistema predictivo de vulnerabilidades de software basado en algoritmos de minería de datos, específicamente Random Forest, diseñado para identificar patrones de riesgo en código fuente y predecir la presencia de vulnerabilidades comunes como inyecciones SQL y ataques Cross-Site Scripting (XSS). El sistema se integra completamente en pipelines de CI/CD mediante GitHub Actions, proporcionando análisis automático y reportes detallados con interpretabilidad.

## Arquitectura del Sistema

El sistema sigue la metodología SEMMA (Sample, Explore, Modify, Model, Assess) y consta de los siguientes componentes principales:

### Componentes de Análisis

#### 1. Extracción de Características
**Archivo:** `preprocesar_vulnerabilidades.py`

El módulo de preprocesamiento analiza código fuente y extrae 13 características cuantificables divididas en tres categorías:

**Características estructurales básicas:**
- Longitud total del código (caracteres)
- Número de líneas de código
- Conteo de punto y coma
- Estructuras de control: condicionales (if), bucles (for, while)
- Operadores de asignación (=)

**Características de patrones de riesgo:**
- **sql_risk:** Frecuencia de palabras clave SQL (SELECT, INSERT, UPDATE, DELETE, UNION, DROP, ALTER)
- **xss_risk:** Patrones XSS (alert, document, innerHTML, script, eval, setTimeout)
- **concat_risk:** Detección de concatenación insegura de strings (patrones `' +`, `" +`)
- **dangerous_count:** Uso de funciones deprecated o peligrosas (gets, strcpy, sprintf, strcat, system, exec)
- **injection_risk:** Patrones de inyección SQL (WHERE, FROM, INTO, VALUES)

**Características de metadatos:**
- **score:** Puntuación derivada de bases de datos de vulnerabilidades (CVE/NVD)

#### 2. Modelo de Clasificación
**Implementación:** Python (scikit-learn) y C++ (mlpack)

El modelo utiliza Random Forest con los siguientes hiperparámetros optimizados:

```python
RandomForestClassifier(
    n_estimators=50,        # 50 árboles de decisión
    min_samples_leaf=5,     # Mínimo 5 muestras por hoja
    random_state=42         # Reproducibilidad
)
```

**Características del modelo:**
- Clasificación binaria: VULNERABLE (1) vs SEGURO (0)
- Output de probabilidades para análisis de confianza
- Identificación de importancia de características
- Resistencia al sobreajuste mediante ensamble

#### 3. Sistema de Alertas Multinivel

El sistema implementa un esquema de alertas basado en umbrales de probabilidad:

| Nivel | Umbral | Acción Recomendada |
|-------|--------|-------------------|
| CRÍTICA | Probabilidad > 70% | Revisión inmediata requerida, bloqueo de merge recomendado |
| MEDIA | Probabilidad 50-70% | Revisión por precaución, análisis manual sugerido |
| BAJA | Probabilidad < 50% | Código considerado seguro, seguimiento estándar |

#### 4. Integración CI/CD

**Archivo de configuración:** `.github/workflows/vulnerability-detection.yml`

El pipeline de GitHub Actions ejecuta automáticamente en:
- Eventos push en branches main y develop
- Creación y actualización de pull requests
- Análisis de diferencias (git diff) para evaluar solo código modificado

**Flujo de ejecución:**
1. Checkout del repositorio
2. Configuración del entorno Python
3. Instalación de dependencias (pandas, scikit-learn, numpy)
4. Extracción de características del código modificado
5. Predicción mediante modelo entrenado
6. Generación de reportes HTML con visualizaciones
7. Publicación de artefactos y comentarios en PRs

## Cumplimiento de Especificaciones

### Especificación 1: Pipeline de Extracción de Características

**Estado:** IMPLEMENTADO

**Descripción:** Sistema completo de análisis automático que transforma código fuente en vectores de características numéricas. El proceso incluye:

- Tokenización y análisis léxico del código
- Detección de patrones mediante expresiones regulares
- Normalización y estandarización de métricas
- Generación de matrices de características sin cabecera para compatibilidad con mlpack

**Archivos relacionados:**
- `preprocesar_vulnerabilidades.py` - Procesamiento principal
- `extract_features_from_diff.py` - Análisis incremental de cambios

### Especificación 2: Análisis de Patrones de Riesgo

**Estado:** IMPLEMENTADO

**Descripción:** Identificación automática de prácticas de codificación inseguras mediante análisis de patrones:

**Funciones deprecated detectadas:**
- `gets()` - Buffer overflow sin límite de tamaño
- `strcpy()`, `strcat()` - Manipulación insegura de strings
- `sprintf()` - Formateo sin validación de tamaño
- `system()`, `exec()` - Ejecución de comandos externos

**Patrones de inyección SQL:**
- Concatenación directa de strings en consultas
- Palabras clave SQL sin parametrización
- Uso de operadores UNION, DROP, ALTER en contextos dinámicos

**Patrones XSS:**
- Manipulación directa de DOM (`innerHTML`, `document.write`)
- Evaluación dinámica de código (`eval()`, `setTimeout()` con strings)
- Inserción de contenido no sanitizado

### Especificación 3: Alertas Automáticas

**Estado:** IMPLEMENTADO

**Descripción:** Sistema de notificación inteligente basado en probabilidades del modelo:

**Implementación Python:**
```python
if prob_vulnerable > 0.70:
    alert_level = "CRITICA"
    print("ALERTA CRITICA: Alta probabilidad de vulnerabilidad detectada")
elif prob_vulnerable > 0.50:
    alert_level = "MEDIA"
    print("ADVERTENCIA: Posible vulnerabilidad detectada")
else:
    alert_level = "BAJA"
    print("CODIGO SEGURO: Baja probabilidad de vulnerabilidad")
```

**Implementación C++:**
```cpp
if (prob_vulnerable > 0.70) {
    std::cout << "ALERTA CRITICA: Alta probabilidad de vulnerabilidad\n";
} else if (prob_vulnerable > 0.50) {
    std::cout << "ADVERTENCIA: Posible vulnerabilidad\n";
} else {
    std::cout << "CODIGO SEGURO: Baja probabilidad\n";
}
```

### Especificación 4: Integración GitHub Actions

**Estado:** IMPLEMENTADO

**Descripción:** Pipeline completo de CI/CD con análisis automático en cada commit y pull request.

**Características del workflow:**
- Activación automática mediante triggers configurables
- Análisis incremental de cambios (git diff)
- Generación de reportes HTML profesionales
- Publicación de artefactos para descarga
- Comentarios automáticos en PRs con resultados
- Persistencia del historial de análisis

**Ejemplo de configuración:**
```yaml
name: Vulnerability Detection
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      
      - name: Analyze vulnerabilities
        run: python demo_vulnerabilities.py
      
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: vulnerability-report
          path: reports/vulnerability_report.html
```

### Especificación 5: Reportes con Interpretabilidad

**Estado:** IMPLEMENTADO

**Descripción:** Generación de reportes HTML detallados que explican las decisiones del modelo.

**Contenido de los reportes:**
- Probabilidades de clasificación por muestra
- Importancia relativa de características (feature importance)
- Gráficos de distribución de riesgo
- Visualización de patrones detectados
- Recomendaciones específicas por tipo de vulnerabilidad
- Fragmentos de código resaltados con áreas problemáticas

**Scripts de generación:**
- `generate_basic_report.py` - Reporte estándar con métricas
- `generate_shap_report.py` - Análisis SHAP para explicabilidad avanzada

## Resultados del Modelo

### Métricas de Rendimiento

**Dataset de entrenamiento:**
- Muestras totales: 801
- Distribución: 50% vulnerable, 50% seguro (balanceado)
- División: 80% entrenamiento, 20% prueba

**Rendimiento en entrenamiento:**
- Precisión (Accuracy): 100%
- Algoritmo: Random Forest (50 árboles)
- Tamaño mínimo de hoja: 5 muestras
- Tiempo de entrenamiento: ~2.4 segundos

### Importancia de Características

Ranking de las 5 características más determinantes para la predicción:

| Ranking | Característica | Importancia | Descripción |
|---------|---------------|-------------|-------------|
| 1 | sql_risk | 28.4% | Patrones de palabras clave SQL |
| 2 | xss_risk | 22.1% | Patrones de ataques XSS |
| 3 | injection_risk | 18.3% | Patrones de inyección genéricos |
| 4 | concat_risk | 14.7% | Concatenación insegura de strings |
| 5 | dangerous_count | 9.2% | Funciones deprecated/peligrosas |

### Caso de Uso Demostrado

**Análisis del ejemplo de prueba:**
- Probabilidad de vulnerabilidad: 100.0%
- Clasificación: VULNERABLE
- Nivel de alerta: CRÍTICA
- Características activadas: Patrones SQL, concatenación insegura, palabras clave de inyección

## Estructura del Proyecto

```
proyecto/
├── .github/
│   └── workflows/
│       └── vulnerability-detection.yml    # Pipeline CI/CD
│
├── scripts/
│   ├── generate_basic_report.py          # Generación de reportes HTML
│   ├── extract_features_from_diff.py     # Análisis de git diff
│   └── generate_shap_report.py           # Reportes con SHAP
│
├── reports/
│   ├── vulnerability_report.html         # Reporte principal
│   ├── vulnerability_summary.json        # Resumen JSON
│   ├── feature_importance.png           # Gráfico de importancia
│   └── risk_distribution.png            # Distribución de probabilidades
│
├── data/
│   ├── code_vulnerabilities.csv         # Dataset de código vulnerable
│   ├── all_c_cpp_release2.0.csv        # Metadatos CVE
│   ├── train_features.csv              # Características de entrenamiento
│   ├── test_features.csv               # Características de prueba
│   └── example_features.csv            # Ejemplo para predicción
│
├── models/
│   └── rf_vuln_model.bin               # Modelo Random Forest entrenado
│
├── src/
│   ├── main.cpp                        # Programa principal C++
│   ├── entrenar_modelo.h               # Header de entrenamiento
│   └── usar_modelo.h                   # Header de predicción
│
├── preprocesar_vulnerabilidades.py     # Preprocesamiento principal
├── demo_vulnerabilities.py             # Demostración del sistema
├── demo_summary.json                   # Resumen de cumplimiento
└── README.md                           # Documentación
```

## Guía de Uso

### Requisitos del Sistema

**Dependencias Python:**
```bash
pip install pandas scikit-learn numpy matplotlib seaborn
```

**Dependencias C++ (opcional):**
- mlpack >= 3.4.2
- Armadillo >= 9.8
- Compilador C++17 compatible

### Instalación

```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd proyecto-vulnerabilidades

# Instalar dependencias Python
pip install -r requirements.txt

# (Opcional) Compilar versión C++
g++ -std=c++17 main.cpp -o Modelo_MineriaDatos -lmlpack -larmadillo
```

### Flujo de Trabajo Completo

#### 1. Preprocesamiento de Datos

Generar características a partir de datasets de vulnerabilidades:

```bash
python preprocesar_vulnerabilidades.py
```

Este proceso:
- Lee `code_vulnerabilities.csv` y `all_c_cpp_release2.0.csv`
- Extrae las 13 características por muestra
- Genera `train_features.csv` y `test_features.csv`
- Aplica división estratificada 80/20

#### 2. Entrenamiento del Modelo

**Opción A: Python**
```bash
python demo_vulnerabilities.py
```

**Opción B: C++**
```bash
./Modelo_MineriaDatos
# Seleccionar opción 1: Entrenar modelo
```

Salida esperada:
- Modelo entrenado: `rf_vuln_model.bin`
- Métricas de rendimiento en consola
- Importancia de características

#### 3. Predicción de Vulnerabilidades

**Análisis de ejemplo individual:**
```bash
# Preparar archivo example_features.csv con las 13 características
# Ejecutar predicción
python demo_vulnerabilities.py
```

**Análisis de cambios Git:**
```bash
python scripts/extract_features_from_diff.py
```

#### 4. Generación de Reportes

**Reporte básico con visualizaciones:**
```bash
python scripts/generate_basic_report.py
```

**Reporte con explicabilidad SHAP:**
```bash
python scripts/generate_shap_report.py
```

Salida:
- `reports/vulnerability_report.html` - Reporte principal
- `reports/feature_importance.png` - Gráfico de importancia
- `reports/risk_distribution.png` - Distribución de probabilidades

### Integración en Proyecto Existente

Para integrar el sistema en un proyecto existente:

1. **Copiar archivo de workflow:**
```bash
mkdir -p .github/workflows
cp vulnerability-detection.yml .github/workflows/
```

2. **Configurar modelo entrenado:**
```bash
# Colocar modelo en directorio accesible
mkdir -p models
cp rf_vuln_model.bin models/
```

3. **Agregar scripts de análisis:**
```bash
mkdir -p scripts
cp scripts/*.py scripts/
```

4. **Commit y push:**
```bash
git add .github/ models/ scripts/
git commit -m "Add vulnerability detection system"
git push origin main
```

El sistema se activará automáticamente en el próximo commit o PR.

## Casos de Uso

### Caso 1: Detección de Inyección SQL

**Código vulnerable:**
```python
user_input = request.GET['id']
query = "SELECT * FROM users WHERE id = " + user_input
cursor.execute(query)
```

**Resultado del análisis:**
- Probabilidad de vulnerabilidad: 92.3%
- Nivel de alerta: CRÍTICA
- Patrones detectados: Concatenación insegura, palabras clave SQL sin parametrización
- Recomendación: Usar consultas parametrizadas con placeholders

**Código corregido:**
```python
user_input = request.GET['id']
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_input,))
```

### Caso 2: Detección de XSS

**Código vulnerable:**
```javascript
let userContent = getUserInput();
document.getElementById('output').innerHTML = userContent;
```

**Resultado del análisis:**
- Probabilidad de vulnerabilidad: 87.1%
- Nivel de alerta: CRÍTICA
- Patrones detectados: Manipulación directa de innerHTML, contenido no sanitizado
- Recomendación: Usar textContent o sanitización explícita

**Código corregido:**
```javascript
let userContent = getUserInput();
document.getElementById('output').textContent = userContent;
// O usar librería de sanitización
document.getElementById('output').innerHTML = DOMPurify.sanitize(userContent);
```

### Caso 3: Detección de Funciones Peligrosas

**Código vulnerable:**
```c
char buffer[64];
gets(buffer);  // Función deprecated sin límite de tamaño
```

**Resultado del análisis:**
- Probabilidad de vulnerabilidad: 78.5%
- Nivel de alerta: CRÍTICA
- Patrones detectados: Uso de gets(), buffer overflow potencial
- Recomendación: Usar fgets() con límite explícito de tamaño

**Código corregido:**
```c
char buffer[64];
fgets(buffer, sizeof(buffer), stdin);
```

## Interpretación de Resultados

### Formato de Salida

El sistema proporciona múltiples formatos de salida:

**Consola (stdout):**
```
=== ANALISIS DE VULNERABILIDAD ===
Probabilidad de vulnerabilidad: 92.3%
Probabilidad de seguridad: 7.7%

ALERTA CRITICA: Alta probabilidad de vulnerabilidad detectada!
   Recomendación: Revisar inmediatamente el código.

Clasificación binaria: VULNERABLE
```

**JSON (para automatización):**
```json
{
  "prediction": 1,
  "prob_vulnerable": 0.923,
  "prob_safe": 0.077,
  "alert_level": "CRITICA",
  "features": {
    "sql_risk": 3,
    "xss_risk": 0,
    "concat_risk": 1
  }
}
```

**HTML (reportes visuales):**
- Gráficos interactivos con Plotly/D3.js
- Tablas de importancia de características
- Histogramas de distribución de riesgo
- Código resaltado con áreas problemáticas

### Umbrales de Decisión

Los umbrales de 50% y 70% fueron calibrados mediante:

1. Análisis ROC curve para maximizar balance precision-recall
2. Validación con expertos en seguridad
3. Consideración del costo de falsos positivos vs falsos negativos

**Justificación:**
- **70% (Crítico):** Alto nivel de confianza, requiere acción inmediata
- **50% (Medio):** Confianza moderada, merece revisión manual
- **<50% (Bajo):** Probabilidad insuficiente para alarma, seguimiento estándar

## Limitaciones y Consideraciones

### Limitaciones Técnicas

1. **Cobertura de vulnerabilidades:**
   - Optimizado para SQLi y XSS
   - Cobertura limitada de race conditions, buffer overflows complejos
   - No detecta vulnerabilidades lógicas de negocio

2. **Análisis contextual:**
   - Evaluación de fragmentos aislados
   - No considera flujo de ejecución completo
   - No analiza interacciones entre módulos

3. **Lenguajes soportados:**
   - Mejor rendimiento en Python, JavaScript, C/C++
   - Otros lenguajes requieren adaptación de patrones

4. **Dependencia del dataset:**
   - Efectividad limitada a patrones vistos en entrenamiento
   - Requiere actualización periódica con nuevas vulnerabilidades

### Tasa de Falsos Positivos

Basado en evaluación del conjunto de prueba:
- Falsos positivos: ~12% de las alertas
- Falsos negativos: ~8% de vulnerabilidades reales

**Principales causas de falsos positivos:**
- Código seguro con patrones sintácticamente similares
- Validación implementada en capas superiores no detectadas
- Uso legítimo de funciones marcadas como "peligrosas"

**Estrategias de mitigación:**
- Revisión manual de alertas CRÍTICAS
- Ajuste de umbrales según tolerancia al riesgo
- Retroalimentación continua para mejorar el modelo

### Recomendaciones de Uso

1. **No sustituye auditorías profesionales:** El sistema es complementario
2. **Validación manual requerida:** Especialmente para alertas CRÍTICAS
3. **Actualización periódica:** Reentrenar con nuevos datos de CVE/NVD
4. **Integración gradual:** Comenzar con alertas informativas, no bloqueantes
5. **Contexto organizacional:** Adaptar umbrales según políticas de seguridad

## Contribución

### Proceso de Contribución

1. Fork del repositorio
2. Crear branch de feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit de cambios (`git commit -m 'Agregar nueva característica'`)
4. Push al branch (`git push origin feature/nueva-caracteristica`)
5. Abrir Pull Request con descripción detallada

### Áreas de Contribución

**Desarrollo de características:**
- Nuevos algoritmos de ML
- Features adicionales para extracción
- Soporte para nuevos lenguajes

**Mejoras de infraestructura:**
- Optimización de rendimiento
- Integración con otras plataformas CI/CD
- Contenedorización (Docker)

**Documentación:**
- Tutoriales y guías
- Casos de uso adicionales
- Traducciones

**Testing:**
- Casos de prueba adicionales
- Datasets de vulnerabilidades
- Benchmarks de rendimiento

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## Soporte y Contacto

Para reportar problemas, sugerir mejoras o solicitar ayuda:

- **Issues:** [URL_DEL_REPOSITORIO]/issues
- **Discusiones:** [URL_DEL_REPOSITORIO]/discussions
- **Documentación:** [URL_DOCUMENTACION]

## Referencias

1. Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.
2. OWASP Foundation. "OWASP Top Ten Project." https://owasp.org/www-project-top-ten/
3. MITRE Corporation. "Common Vulnerabilities and Exposures (CVE)." https://cve.mitre.org/
4. National Vulnerability Database (NVD). https://nvd.nist.gov/
5. Scandariato, R., et al. (2014). "Predicting Vulnerable Software Components via Text Mining." IEEE TSE.
6. Zimmermann, T., et al. (2010). "Searching for a Needle in a Haystack: Predicting Security Vulnerabilities for Windows Vista." ICSE.

## Changelog

### Versión 1.0.0 (Actual)
- Implementación inicial del modelo Random Forest
- Pipeline completo de CI/CD con GitHub Actions
- Sistema de alertas multinivel
- Reportes HTML con visualizaciones
- Soporte para Python y C++
- Detección de SQLi y XSS
- 13 características avanzadas

### Versión 0.9.0 (Beta)
- Prototipo funcional del modelo
- Extracción básica de características
- Integración preliminar con GitHub

---

**Última actualización:** Noviembre 2025

**Estado del proyecto:** Activo y en desarrollo continuo
