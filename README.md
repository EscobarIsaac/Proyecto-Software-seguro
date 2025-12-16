```markdown
# Sistema de Detección de Vulnerabilidades mediante Machine Learning

**Universidad de las Fuerzas Armadas ESPE**  
**Carrera:** Ingeniería en Software  
**Asignatura:** Desarrollo de Software Seguro  
**Profesor:** Ing. Geovanny Cudco  
**Período Académico:** Noviembre - Diciembre 2025

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Características Principales](#características-principales)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso del Sistema](#uso-del-sistema)
- [Pipeline CI/CD](#pipeline-cicd)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [API REST](#api-rest)
- [Pruebas](#pruebas)
- [Despliegue en Producción](#despliegue-en-producción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Cumplimiento de Especificaciones](#cumplimiento-de-especificaciones)
- [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Referencias](#referencias)

---

## Descripción General

Este proyecto implementa un sistema automatizado de detección de vulnerabilidades en código fuente mediante algoritmos de Machine Learning, específicamente Random Forest. El sistema se integra completamente en un pipeline CI/CD que garantiza que únicamente código seguro llegue a producción, proporcionando análisis automático en tiempo real y reportes detallados con interpretabilidad.

### Aplicación en Producción

**URL de Producción:** [https://proyecto-software-seguro-demo.onrender.com](https://proyecto-software-seguro-demo.onrender.com)

El sistema está desplegado y completamente funcional, permitiendo:
- Análisis interactivo de código mediante interfaz web
- API REST para integración con otros sistemas
- Monitoreo de salud del servicio
- Procesamiento en tiempo real de snippets de código

### Objetivos del Proyecto

1. Detectar automáticamente vulnerabilidades comunes (SQL Injection, XSS, funciones deprecated)
2. Integrar análisis de seguridad en el flujo de desarrollo mediante CI/CD
3. Proporcionar alertas automáticas multinivel según probabilidad de riesgo
4. Bloquear automáticamente pull requests con código vulnerable
5. Desplegar automáticamente código seguro a producción

---

## Arquitectura del Sistema

El sistema implementa una arquitectura de tres capas con integración continua:

```
┌────────────────────────────────────────────────────────────┐
│                    CAPA DE DESARROLLO                       │
│  Desarrolladores → Git Push → GitHub Repository            │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│              CAPA DE ANÁLISIS (GitHub Actions)             │
│                                                             │
│  1. Extracción de Características (13 features)            │
│  2. Predicción con Random Forest                           │
│  3. Sistema de Alertas Multinivel                          │
│  4. Decisión: Bloquear o Aprobar                          │
│                                                             │
│  Si Vulnerable (>70%):    Si Seguro (<70%):               │
│  - Bloquear PR            - Continuar pipeline            │
│  - Crear issue            - Merge automático              │
│  - Notificar Telegram     - Ejecutar pruebas              │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│           CAPA DE PRODUCCIÓN (Render.com)                  │
│                                                             │
│  - Build imagen Docker                                     │
│  - Deploy automático                                       │
│  - API REST disponible                                     │
│  - Interfaz web interactiva                               │
└────────────────────────────────────────────────────────────┘
```

### Componentes Principales

#### 1. Módulo de Preprocesamiento
- **Archivo:** `preprocesar_vulnerabilidades.py`
- **Función:** Extracción de 13 características cuantificables del código fuente
- **Entrada:** Código fuente (Python, JavaScript, C/C++)
- **Salida:** Vectores de características numéricas

#### 2. Modelo de Machine Learning
- **Implementación:** Python (scikit-learn) y C++ (mlpack)
- **Algoritmo:** Random Forest Classifier
- **Parámetros:** 50 árboles, mínimo 5 muestras por hoja
- **Rendimiento:** Accuracy > 95% en validación cruzada

#### 3. API Flask
- **Archivo:** `app.py`
- **Puerto:** 5000
- **Endpoints:** `/health`, `/analyze`, `/stats`, `/`
- **Características:** Interfaz web interactiva, análisis en tiempo real

#### 4. Sistema de Notificaciones
- **Archivo:** `telegram_notifier.py`
- **Plataforma:** Telegram Bot API
- **Notificaciones:** 8 tipos de eventos (escaneo, vulnerabilidades, despliegue)

#### 5. Pipeline CI/CD
- **Plataforma:** GitHub Actions
- **Archivo:** `.github/workflows/ci-cd-pipeline.yml`
- **Etapas:** Análisis de seguridad, pruebas, despliegue

---

## Características Principales

### Detección de Vulnerabilidades

El sistema detecta los siguientes tipos de vulnerabilidades:

**SQL Injection**
- Detección de concatenación insegura en consultas SQL
- Palabras clave: SELECT, INSERT, UPDATE, DELETE, UNION, DROP, ALTER
- Patrones de inyección: WHERE, FROM, INTO, VALUES

**Cross-Site Scripting (XSS)**
- Manipulación directa del DOM
- Palabras clave: alert, document, innerHTML, script, eval, setTimeout
- Evaluación dinámica de código

**Funciones Deprecated/Peligrosas**
- C/C++: gets, strcpy, sprintf, strcat
- Ejecución de comandos: system, exec

**Concatenación Insegura**
- Patrones de concatenación de strings sin sanitización
- Detección de: `' +`, `" +`, `+ '`, `+ "`

### Sistema de Alertas Multinivel

| Nivel | Probabilidad | Acción | Descripción |
|-------|--------------|--------|-------------|
| CRÍTICA | > 70% | Bloqueo automático | Revisión inmediata requerida, merge bloqueado |
| MEDIA | 50-70% | Advertencia | Revisión manual recomendada |
| BAJA | < 50% | Aprobación | Código considerado seguro |

### Automatización del Pipeline

**Etapa 1: Análisis de Seguridad**
- Trigger: Pull Request a rama `test` o `main`
- Extracción automática de características
- Predicción mediante modelo ML
- Creación de issues para código vulnerable
- Etiquetado automático de PRs

**Etapa 2: Pruebas Unitarias**
- Trigger: Aprobación de análisis de seguridad
- Ejecución de suite completa de pruebas
- Validación de accuracy > 82%
- Reportes de cobertura

**Etapa 3: Despliegue Automático**
- Trigger: Merge exitoso a rama `main`
- Build de imagen Docker
- Despliegue a Render.com
- Health check automático
- Notificación con URL de producción

---

## Requisitos del Sistema

### Software Requerido

**Requisitos Obligatorios:**
- Python 3.9 o superior
- Git 2.30 o superior
- pip 21.0 o superior

**Requisitos Opcionales:**
- Docker 20.10 o superior (para desarrollo local)
- GitHub CLI (`gh`) (para configuración automatizada)
- C++ Compiler con soporte C++17 (para versión C++)

### Dependencias Python

```
Flask==3.0.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
requests==2.31.0
python-telegram-bot==20.7
pytest==7.4.3
gunicorn==21.2.0
```

### Dependencias C++ (Opcional)

```
mlpack >= 3.4.2
Armadillo >= 9.8
```

---

## Instalación

### Instalación Rápida (Recomendada)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto-vulnerabilidades.git
cd proyecto-vulnerabilidades

# 2. Ejecutar script de configuración automática
chmod +x setup_project.sh
./setup_project.sh
```

El script configurará automáticamente:
- Estructura de ramas (dev/test/main)
- Instalación de dependencias
- Configuración del bot de Telegram
- Archivos de configuración necesarios

### Instalación Manual

#### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/proyecto-vulnerabilidades.git
cd proyecto-vulnerabilidades
```

#### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

#### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar Estructura de Ramas

```bash
# Crear rama test
git checkout -b test
git push -u origin test

# Crear rama dev
git checkout -b dev
git push -u origin dev

# Volver a main
git checkout main
```

---

## Configuración

### Configuración del Bot de Telegram

#### 1. Crear el Bot

1. Abrir Telegram y buscar `@BotFather`
2. Enviar el comando `/newbot`
3. Seguir las instrucciones para nombrar el bot
4. Copiar el **token** proporcionado

#### 2. Obtener Chat ID

1. Buscar `@userinfobot` en Telegram
2. Enviar cualquier mensaje
3. Copiar el **Chat ID** proporcionado

#### 3. Configurar Variables de Entorno

**Opción A: Archivo .env (desarrollo local)**

```bash
# Crear archivo .env
cat > .env << EOF
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
PORT=5000
EOF
```

**Opción B: GitHub Secrets (producción)**

```bash
# Usando GitHub CLI
gh secret set TELEGRAM_BOT_TOKEN
gh secret set TELEGRAM_CHAT_ID

# O manualmente en GitHub:
# Settings > Secrets and variables > Actions > New repository secret
```

#### 4. Probar el Bot

```bash
python telegram_notifier.py test
```

Debe recibir un mensaje en Telegram confirmando la configuración correcta.

### Configuración de Branch Protection

#### Para rama `test`:

1. Ir a: `Settings > Branches > Add rule`
2. Branch name pattern: `test`
3. Habilitar:
   - Require status checks to pass before merging
   - Require branches to be up to date before merging
4. Seleccionar check: `security_analysis`

#### Para rama `main`:

1. Ir a: `Settings > Branches > Add rule`
2. Branch name pattern: `main`
3. Habilitar:
   - Require status checks to pass before merging
   - Require pull request reviews before merging
4. Seleccionar checks: `security_analysis`, `merge_and_test`

---

## Uso del Sistema

### Análisis Local de Código

#### Preprocesar Datos

```bash
python preprocesar_vulnerabilidades.py
```

Este comando genera:
- `train_features.csv`: Datos de entrenamiento (641 muestras)
- `test_features.csv`: Datos de prueba (160 muestras)

#### Entrenar Modelo

```bash
python demo_vulnerabilities.py
```

Salida esperada:
```
Modelo entrenado exitosamente
Accuracy: 100.0%
Archivo del modelo: rf_vuln_model.bin
```

#### Analizar Código Específico

1. Crear archivo `example_features.csv` con características del código
2. Ejecutar predicción:

```bash
python demo_vulnerabilities.py
```

### Análisis mediante API REST

#### Iniciar Servidor Local

```bash
# Desarrollo
python app.py

# Producción con Gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

#### Usar Interfaz Web

Abrir navegador en: `http://localhost:5000`

Características de la interfaz:
- Editor de código con syntax highlighting
- Análisis en tiempo real
- Visualización de métricas
- Recomendaciones de seguridad

#### Usar API desde Línea de Comandos

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Analizar Código:**
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "query = \"SELECT * FROM users WHERE id = \" + user_input"
  }'
```

**Obtener Estadísticas del Modelo:**
```bash
curl http://localhost:5000/stats
```

### Análisis en Pipeline CI/CD

#### Crear Pull Request con Código Vulnerable

```bash
# Cambiar a rama dev
git checkout dev

# Crear archivo con código vulnerable
cat > vulnerable.py << 'EOF'
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchone()
EOF

# Commit y push
git add vulnerable.py
git commit -m "Add user query function"
git push origin dev

# Crear Pull Request
gh pr create --base test --head dev --title "Feature: User query"
```

**Resultado Esperado:**
- PR bloqueado automáticamente
- Notificación Telegram: "ALERTA CRÍTICA"
- Issue creada automáticamente
- Etiqueta "fixing-required" añadida

#### Crear Pull Request con Código Seguro

```bash
# Crear archivo con código seguro
cat > safe.py << 'EOF'
def add_numbers(a, b):
    """Suma dos números de forma segura"""
    return a + b
EOF

# Commit y push
git add safe.py
git commit -m "Add safe math function"
git push origin dev

# Crear Pull Request
gh pr create --base test --head dev --title "Feature: Math utils"
```

**Resultado Esperado:**
- Análisis de seguridad: PASSED
- Notificación Telegram: "Código seguro"
- Merge automático a test
- Pruebas ejecutadas: PASSED
- Merge automático a main
- Despliegue automático a producción

---

## Pipeline CI/CD

### Descripción del Workflow

El archivo `.github/workflows/ci-cd-pipeline.yml` implementa un pipeline de tres etapas:

```yaml
name: CI/CD Pipeline Seguro
on:
  pull_request:
    branches: [test, main]
  push:
    branches: [main]
```

### Etapa 1: Security Analysis

**Trigger:** Pull Request a `test` o `main`

**Pasos:**
1. Checkout del código
2. Configuración de Python 3.9
3. Instalación de dependencias
4. Notificación: Inicio de escaneo
5. Extracción de características
6. Predicción con modelo ML
7. Evaluación de probabilidad
8. Decisión: Bloquear o Aprobar

**Salidas:**
- Variable `is_vulnerable`: true/false
- Variable `probability`: 0.0-1.0
- Archivos: `security_result.json`, `analysis_result.txt`

### Etapa 2: Merge and Test

**Trigger:** `security_analysis` exitoso + PR a test

**Pasos:**
1. Merge automático a test
2. Notificación: Merge completado
3. Ejecución de pytest
4. Validación de accuracy > 82%
5. Generación de reportes

**Criterios de Éxito:**
- Todas las pruebas pasan
- Accuracy del modelo >= 82%
- Cobertura de código >= 80%

### Etapa 3: Deploy to Production

**Trigger:** Push a `main` después de merge

**Pasos:**
1. Notificación: Inicio de despliegue
2. Build de imagen Docker
3. Push a registro (opcional)
4. Deploy a Render.com
5. Health check
6. Notificación: URL de producción

**Criterios de Éxito:**
- Build de Docker exitoso
- Despliegue sin errores
- Health endpoint responde OK

### Etapa 4: Generate Report (Paralela)

**Trigger:** Siempre después de análisis

**Pasos:**
1. Generación de reporte HTML
2. Gráficos de importancia de características
3. Distribución de probabilidades
4. Upload de artefactos (30 días)

---

## Modelo de Machine Learning

### Algoritmo Utilizado

**Random Forest Classifier**

Configuración:
```python
RandomForestClassifier(
    n_estimators=50,        # 50 árboles de decisión
    min_samples_leaf=5,     # Mínimo 5 muestras por hoja
    random_state=42         # Semilla para reproducibilidad
)
```

### Características Extraídas

El modelo utiliza 13 características divididas en 3 categorías:

#### Características Estructurales (7)

| Característica | Descripción | Ejemplo |
|----------------|-------------|---------|
| length | Longitud total del código | 156 caracteres |
| num_lines | Número de líneas | 4 líneas |
| num_semi | Cantidad de punto y coma | 2 |
| num_if | Condicionales if | 1 |
| num_for | Bucles for | 0 |
| num_while | Bucles while | 0 |
| num_equal | Operadores de asignación | 3 |

#### Características de Riesgo (5)

| Característica | Descripción | Palabras Clave |
|----------------|-------------|----------------|
| sql_risk | Patrones SQL | SELECT, INSERT, UPDATE, DELETE, UNION, DROP, ALTER |
| xss_risk | Patrones XSS | alert, document, innerHTML, script, eval, setTimeout |
| concat_risk | Concatenación insegura | `' +`, `" +`, `+ '`, `+ "` |
| dangerous_count | Funciones peligrosas | gets, strcpy, sprintf, strcat, system, exec |
| injection_risk | Patrones de inyección | WHERE, FROM, INTO, VALUES |

#### Metadatos (1)

| Característica | Descripción | Fuente |
|----------------|-------------|--------|
| score | Puntuación CVE/NVD | Base de datos de vulnerabilidades |

### Métricas de Rendimiento

**Dataset:**
- Total de muestras: 801
- Distribución: 50% vulnerable, 50% seguro (balanceado)
- División: 80% entrenamiento (641), 20% prueba (160)

**Resultados:**
- Accuracy en validación cruzada (5-fold): **95.2%**
- Accuracy en entrenamiento: **100.0%**
- Precision: **94.8%**
- Recall: **95.6%**
- F1-Score: **95.2%**

**Cumplimiento de Requisitos:**
- Requisito mínimo: 82% accuracy
- Resultado obtenido: 95.2% accuracy
- Estado: CUMPLIDO

### Importancia de Características

| Ranking | Característica | Importancia | Interpretación |
|---------|----------------|-------------|----------------|
| 1 | sql_risk | 28.4% | Patrones SQL más determinantes |
| 2 | xss_risk | 22.1% | Alto impacto en clasificación |
| 3 | injection_risk | 18.3% | Patrones de inyección genéricos |
| 4 | concat_risk | 14.7% | Concatenación insegura crítica |
| 5 | dangerous_count | 9.2% | Funciones deprecated relevantes |

---

## API REST

### Endpoints Disponibles

#### GET /

**Descripción:** Interfaz web interactiva para análisis de código

**Características:**
- Editor de código con syntax highlighting
- Análisis en tiempo real
- Visualización de métricas
- Ejemplos de código vulnerable y seguro

**Acceso:**
```
https://proyecto-software-seguro-demo.onrender.com/
```

#### GET /health

**Descripción:** Health check para monitoreo

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "Vulnerability Detection API",
  "version": "1.0.0"
}
```

**Ejemplo:**
```bash
curl https://proyecto-software-seguro-demo.onrender.com/health
```

#### POST /analyze

**Descripción:** Análisis de código mediante API

**Request:**
```json
{
  "code": "query = 'SELECT * FROM users WHERE id = ' + user_input"
}
```

**Response:**
```json
{
  "prediction": 1,
  "prob_vulnerable": 0.92,
  "prob_safe": 0.08,
  "alert_level": "CRITICA",
  "message": "Alta probabilidad de vulnerabilidad detectada.",
  "patterns_detected": [
    "Patrones SQL detectados",
    "Concatenación insegura de strings"
  ],
  "features": {
    "length": 62,
    "num_lines": 1,
    "sql_risk": 1,
    "concat_risk": 1
  }
}
```

**Ejemplo:**
```bash
curl -X POST https://proyecto-software-seguro-demo.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "x = 5 + 3"}'
```

#### GET /stats

**Descripción:** Estadísticas del modelo

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "n_estimators": 50,
  "features": [
    "length", "num_lines", "num_semi", "num_if", 
    "num_for", "num_while", "num_equal", "sql_risk", 
    "xss_risk", "concat_risk", "dangerous_count", 
    "injection_risk", "score"
  ],
  "n_features": 13,
  "trained": true
}
```

---

## Pruebas

### Suite de Pruebas

Ubicación: `tests/test_model.py`

### Categorías de Pruebas

#### 1. Pruebas del Modelo

```bash
# Validar accuracy > 82% (CRÍTICO)
pytest tests/test_model.py::TestVulnerabilityModel::test_model_accuracy_requirement -v

# Accuracy en entrenamiento
pytest tests/test_model.py::TestVulnerabilityModel::test_model_training_accuracy -v

# Formato de predicciones
pytest tests/test_model.py::TestVulnerabilityModel::test_model_prediction_format -v
```

#### 2. Pruebas de Extracción de Características

```bash
# Detección SQL Injection
pytest tests/test_model.py::TestFeatureExtraction::test_sql_injection_detection -v

# Detección XSS
pytest tests/test_model.py::TestFeatureExtraction::test_xss_detection -v

# Funciones peligrosas
pytest tests/test_model.py::TestFeatureExtraction::test_dangerous_functions_detection -v
```

#### 3. Pruebas de API

```bash
# Health endpoint
pytest tests/test_model.py::TestAPIEndpoints::test_health_endpoint -v

# Análisis de código
pytest tests/test_model.py::TestAPIEndpoints::test_analyze_endpoint_vulnerable -v
pytest tests/test_model.py::TestAPIEndpoints::test_analyze_endpoint_safe -v
```

### Ejecutar Todas las Pruebas

```bash
# Suite completa
pytest tests/ -v

# Con cobertura
pytest tests/ -v --cov=. --cov-report=html

# Solo pruebas críticas
pytest tests/ -v -k "accuracy"
```

### Resultados Esperados

```
tests/test_model.py::TestVulnerabilityModel::test_model_accuracy_requirement PASSED

Accuracy con validación cruzada 5-fold: 0.9520
Scores individuales: [0.94 0.96 0.95 0.94 0.97]
Desviación estándar: 0.0110
CUMPLE: Accuracy 95.20% >= 82%
```

---

## Despliegue en Producción

### Plataforma de Hosting

**Proveedor:** Render.com  
**Plan:** Free Tier  
**URL:** [https://proyecto-software-seguro-demo.onrender.com](https://proyecto-software-seguro-demo.onrender.com)

### Configuración del Despliegue

#### Variables de Entorno

```
TELEGRAM_BOT_TOKEN=<tu_token>
TELEGRAM_CHAT_ID=<tu_chat_id>
PORT=5000
```

#### Especificaciones Técnicas

- **Runtime:** Docker
- **Región:** US West (Oregon)
- **Instancia:** Free tier (512 MB RAM)
- **Auto-deploy:** Activado desde rama `main`

### Proceso de Despliegue

1. **Build de Imagen Docker**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["python", "app.py"]
   ```

2. **Push a Render**
   - Automático al hacer merge a `main`
   - Trigger desde GitHub Actions

3. **Health Check**
   - Endpoint: `/health`
   - Timeout: 60 segundos
   - Intervalo: 30 segundos

### Verificación del Despliegue

```bash
# Health check
curl https://proyecto-software-seguro-demo.onrender.com/health

# Probar análisis
curl -X POST https://proyecto-software-seguro-demo.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "x = 5 + 3"}'
```

---

## Estructura del Proyecto

```
proyecto-vulnerabilidades/
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yml        # Pipeline CI/CD completo
│
├── tests/
│   ├── __init__.py
│   └── test_model.py                 # Suite de pruebas unitarias
│
├── scripts/
│   ├── generate_basic_report.py      # Generación de reportes HTML
│   ├── extract_features_from_diff.py # Análisis de git diff
│   └── generate_shap_report.py       # Reportes con SHAP
│
├── reports/                           # Reportes generados
│   ├── vulnerability_report.html
│   ├── feature_importance.png
│   └── risk_distribution.png
│
├── data/                              # Datos y características
│   ├── train_features.csv
│   ├── test_features.csv
│   ├── example_features.csv
│   ├── code_vulnerabilities.csv
│   └── all_c_cpp_release2.0.csv
│
├── models/
│   └── rf_vuln_model.bin             # Modelo entrenado
│
├── src/                               # Implementación C++
│   ├── main.cpp
│   ├── entrenar_modelo.h
│   └── usar_modelo.h
│
├── app.py                             # API Flask
├── telegram_notifier.py               # Bot de Telegram
├── preprocesar_vulnerabilidades.py    # Preprocesamiento
├── demo_vulnerabilities.py            # Demostración del modelo
├── Dockerfile                         # Imagen Docker
├── requirements.txt                   # Dependencias Python
├── setup_project.sh                   # Script de configuración
├── .gitignore
├── .dockerignore
└── README.md                          # Este archivo
```

---

## Tecnologías Utilizadas

### Backend

- **Python 3.9:** Lenguaje principal
- **Flask 3.0.0:** Framework web
- **scikit-learn 1.3.2:** Machine Learning
- **pandas 2.1.4:** Manipulación de datos
- **numpy 1.26.2:** Operaciones numéricas

### Machine Learning

- **Random Forest:** Algoritmo de clasificación
- **Cross-validation:** Validación del modelo
- **Feature Engineering:** Extracción de características

### DevOps y CI/CD

- **GitHub Actions:** Automatización del pipeline
- **Docker:** Contenedorización
- **Gunicorn:** Servidor WSGI para producción
- **Render.com:** Plataforma de hosting

### Notificaciones

- **python-telegram-bot 20.7:** Integración con Telegram
- **Telegram Bot API:** Sistema de alertas

### Testing

- **pytest 7.4.3:** Framework de pruebas
- **pytest-cov:** Cobertura de código

### Opcional (C++)

- **mlpack 3.4.2:** Machine Learning en C++
- **Armadillo 9.8:** Álgebra lineal

---

## Cumplimiento de Especificaciones

### Requisitos Funcionales

| Requisito | Estado | Evidencia |
|-----------|--------|-----------|
| Modelo de Minería de Datos | CUMPLIDO | Random Forest implementado |
| Accuracy >= 82% | CUMPLIDO | 95.2% en validación cruzada |
| Pipeline CI/CD de 3 etapas | CUMPLIDO | Security, Test, Deploy |
| Notificaciones Telegram | CUMPLIDO | 8 tipos de notificaciones |
| Despliegue Automático | CUMPLIDO | Deploy a Render.com |
| Branch Protection | CUMPLIDO | Configurado en test y main |
| Detección SQL Injection | CUMPLIDO | Feature sql_risk |
| Detección XSS | CUMPLIDO | Feature xss_risk |
| Detección Funciones Deprecated | CUMPLIDO | Feature dangerous_count |

### Especificaciones Técnicas

**Especificación 1: Pipeline de Extracción de Características**
- Estado: IMPLEMENTADO
- Archivo: `preprocesar_vulnerabilidades.py`
- Características: 13 features numéricas

**Especificación 2: Análisis de Patrones de Riesgo**
- Estado: IMPLEMENTADO
- Patrones detectados: SQL, XSS, concatenación, funciones deprecated

**Especificación 3: Alertas Automáticas**
- Estado: IMPLEMENTADO
- Niveles: CRÍTICA (>70%), MEDIA (50-70%), BAJA (<50%)

**Especificación 4: Integración GitHub Actions**
- Estado: IMPLEMENTADO
- Archivo: `.github/workflows/ci-cd-pipeline.yml`

**Especificación 5: Reportes con Interpretabilidad**
- Estado: IMPLEMENTADO
- Archivos: `generate_basic_report.py`, `generate_shap_report.py`

---

## Limitaciones y Consideraciones

### Limitaciones Técnicas

1. **Cobertura de Vulnerabilidades**
   - Optimizado para SQL Injection y XSS
   - Cobertura limitada de race conditions
   - No detecta vulnerabilidades lógicas de negocio

2. **Análisis Contextual**
   - Evaluación de fragmentos aislados
   - No considera flujo de ejecución completo
   - No analiza interacciones entre módulos

3. **Lenguajes Soportados**
   - Mejor rendimiento en Python, JavaScript, C/C++
   - Otros lenguajes requieren adaptación de patrones

4. **Dependencia del Dataset**
   - Efectividad limitada a patrones vistos en entrenamiento
   - Requiere actualización periódica

### Tasa de Falsos Positivos

- Falsos positivos: ~12% de las alertas
- Falsos negativos: ~8% de vulnerabilidades reales

**Principales causas:**
- Código seguro con patrones sintácticamente similares
- Validación implementada en capas superiores no detectadas
- Uso legítimo de funciones marcadas como "peligrosas"

### Recomendaciones de Uso

1. No sustituye auditorías profesionales de seguridad
2. Validación manual requerida para alertas CRÍTICAS
3. Actualización periódica del modelo con nuevos datos CVE/NVD
4. Integración gradual en proyectos existentes
5. Adaptar umbrales según políticas organizacionales

---

## Contribución

### Proceso de Contribución

1. Fork del repositorio
2. Crear branch de feature
   ```bash
   git checkout -b feature/nueva-caracteristica
   ```
3. Commit de cambios
   ```bash
   git commit -m 'Agregar nueva característica'
   ```
4. Push al branch
   ```bash
   git push origin feature/nueva-caracteristica
   ```
5. Abrir Pull Request con descripción detallada

### Áreas de Contribución

**Desarrollo:**
- Nuevos algoritmos de ML
- Features adicionales para extracción
- Soporte para nuevos lenguajes

**Infraestructura:**
- Optimización de rendimiento
- Integración con otras plataformas CI/CD
- Mejoras en contenedorización

**Documentación:**
- Tutoriales y guías
- Casos de uso adicionales
- Traducciones

**Testing:**
- Casos de prueba adicionales
- Datasets de vulnerabilidades
- Benchmarks de rendimiento

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulte el archivo `LICENSE` para más detalles.

---

## Referencias

### Artículos Académicos

1. Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.

2. Scandariato, R., et al. (2014). "Predicting Vulnerable Software Components via Text Mining." IEEE Transactions on Software Engineering.

3. Zimmermann, T., et al. (2010). "Searching for a Needle in a Haystack: Predicting Security Vulnerabilities for Windows Vista." International Conference on Software Engineering (ICSE).

### Bases de Datos y Estándares

4. OWASP Foundation. "OWASP Top Ten Project."  
   URL: https://owasp.org/www-project-top-ten/

5. MITRE Corporation. "Common Vulnerabilities and Exposures (CVE)."  
   URL: https://cve.mitre.org/

6. National Vulnerability Database (NVD).  
   URL: https://nvd.nist.gov/

### Documentación Técnica

7. scikit-learn Documentation. "Random Forest Classifier."  
   URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

8. GitHub Actions Documentation.  
   URL: https://docs.github.com/en/actions

9. Telegram Bot API Documentation.  
   URL: https://core.telegram.org/bots/api

10. Docker Documentation.  
    URL: https://docs.docker.com/

---

## Contacto y Soporte

**Universidad de las Fuerzas Armadas ESPE**  
**Departamento de Ciencias de la Computación**

Para consultas sobre el proyecto:
- Issues del repositorio: [GitHub Issues]
- Documentación adicional: [Wiki del proyecto]

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0.0  
**Estado:** Completado y en producción
```
