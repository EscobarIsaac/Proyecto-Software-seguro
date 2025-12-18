# 📚 Documentación Única: Pipeline CI/CD Seguro con ML

Proyecto integral de detección de vulnerabilidades con Machine Learning (Random Forest), CI/CD completo, notificaciones por Telegram y despliegue en Render. Este es el único README: incluye configuración, uso, pipeline, despliegue y un apartado para la configuracion de C++ (si hay preguntas, porfavor contactar con el administrador).

---

## Índice

- Descripción y Objetivos
- Requisitos y Dependencias
- Instalación Rápida (Windows/Linux)
- Configuración (Telegram, Secrets, Ramas, Protección)
- Pipeline CI/CD (Jobs y criterios)
- Despliegue en Render
- API y Uso Local
- Pruebas y Métricas (Accuracy ≥ 82%)
- Apartado C++ (opcional)
- Problemas Comunes

---

## Descripción y Objetivos

- Detecta vulnerabilidades comunes: SQLi, XSS, funciones peligrosas, concatenación insegura.
- Integra análisis ML en PRs para bloquear código riesgoso automáticamente.
- Notifica por Telegram en cada fase del pipeline.
- Despliega automáticamente a producción en Render.

Archivos clave: [app.py](app.py), [preprocesar_vulnerabilidades.py](preprocesar_vulnerabilidades.py), [demo_vulnerabilities.py](demo_vulnerabilities.py), [telegram_notifier.py](telegram_notifier.py), [ci-cd-pipeline.yml](ci-cd-pipeline.yml), [Dockerfile](Dockerfile), [requirements.txt](requirements.txt).

---

## Requisitos y Dependencias

- Python 3.9+
- Git
- Opcional: Docker, GitHub CLI (`gh`)
- Datos: [train_features.csv](train_features.csv), [test_features.csv](test_features.csv)

Python (requirements): Flask, pandas, numpy, scikit-learn, requests, python-telegram-bot, pytest, gunicorn.

---

## Instalación Rápida

Windows (PowerShell):

```powershell
# Clonar
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# Entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Dependencias
pip install -r requirements.txt
```

Linux/macOS:

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuración

### Telegram

- Crear bot con `@BotFather` → `/newbot` → copia TOKEN.
- Obtener Chat ID con `@userinfobot`.

Probar localmente:

```powershell
$env:TELEGRAM_BOT_TOKEN="tu_token"
$env:TELEGRAM_CHAT_ID="tu_chat_id"
python telegram_notifier.py test
```

### GitHub Secrets

Con GitHub CLI:

```powershell
gh auth login
gh secret set TELEGRAM_BOT_TOKEN
gh secret set TELEGRAM_CHAT_ID
```

Manual: Settings → Secrets and variables → Actions → New repository secret.

### Ramas y Protección

- Ramas: `main` (prod), `test` (staging), `dev` (desarrollo).

Protección en GitHub:

- Regla `test`: Require status checks; seleccionar `security_analysis`.
- Regla `main`: Require status checks + reviews; seleccionar `security_analysis`, `merge_and_test`.

---

## Pipeline CI/CD

Jobs principales (ver [ci-cd-pipeline.yml](ci-cd-pipeline.yml)):

- security_analysis: ejecuta ML y bloquea si riesgo > 70%.
- merge_and_test: merge dev→test, corre `pytest`, valida accuracy ≥ 82%.
- deploy_to_production: build Docker y despliega a Render; health check.
- generate_report: artefactos y visualizaciones (opcional).

---

## Despliegue en Render

Configuración sugerida:

- Environment: Docker
- Branch: `main`
- Instance: Free
- Variables: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `PORT=5000`

Verificación:

```bash
curl https://tu-app.onrender.com/health
```

---

## API y Uso Local

Arrancar servidor:

```powershell
python app.py
# o
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

Health:

```bash
curl http://localhost:5000/health
```

Analizar código:

```bash
curl -X POST http://localhost:5000/analyze \
    -H "Content-Type: application/json" \
    -d '{"code": "query = \"SELECT * FROM users WHERE id = \" + user_input"}'
```

---

## Pruebas y Métricas

```powershell
pip install pytest pytest-cov
pytest tests/test_dummy.py -v
# Si tienes suite avanzada:
# pytest tests/test_model.py::TestVulnerabilityModel::test_model_accuracy_requirement -v
```

Objetivo: Accuracy en validación cruzada ≥ 82% (típicamente ≈ 95%).

---

## Apartado C++

Archivos: [main.cpp](main.cpp), [entrenar_modelo.h](entrenar_modelo.h), [usar_modelo.h](usar_modelo.h).

Dependencias sugeridas:

- Compilador C++17 (g++, MSVC, clang)
- Opcional: mlpack + Armadillo (para Random Forest en C++)

Windows / Embarcadero dev c++:

```powershell
# Configuracion, compilacion y ejecucion para el entrenamiento del modelo
1) Descargar e instalar vcpkg o hacer pull desde su github, recomendable hacerlo en el apartado raiz del sistema (C:\)
2) Crear un nuevo proyecto dentro de embarcadero dev c++
3) Crear los archivos necesarios y enlazarlos al proyecto (main.cpp, entrenar_modelo.h, usar_modelo.h)
4) Configurar el apartado de librerias:
* Entrar a las opciones del proyecto en la pestaño Proyecto
* Ir al apartado de archivos/directorios
* En el directorio de librerias colocar las rutas de las carpetas lib y bin en este apartado, por parte de vcpkg
* Ir al apartado de directorios de include, colocar la ruta de la carpeta include por parte del vcpkg 
* Ir al apartado de Argumentos del programa, y en el recuadro de C++ compiler colocar: std=c++17, para configurarlo a c++ 17
* Guardar cambios y colocar el codigo en los respectivos archivos
```

Si usas mlpack en `entrenar_modelo.h`/`usar_modelo.h`, enlaza bibliotecas según tu entorno (incluye headers y libs de Armadillo/mlpack).

---

## Problemas Comunes

- Actions no corre: habilita workflows en GitHub y verifica [ci-cd-pipeline.yml](ci-cd-pipeline.yml).
- Telegram no envía: revisa secrets y prueba [telegram_notifier.py](telegram_notifier.py) con variables locales.
- Render falla build: confirma [Dockerfile](Dockerfile) y [requirements.txt](requirements.txt), presencia de datasets.
- Accuracy bajo: re-generar features ([preprocesar_vulnerabilidades.py](preprocesar_vulnerabilidades.py)) y re-entrenar ([demo_vulnerabilities.py](demo_vulnerabilities.py)).

---

## Flujo de Trabajo (PRs)

- PR dev→test con código vulnerable: se bloquea, issue y alerta Telegram.
- PR dev→test con código seguro: aprueba, merge a test, pruebas OK, merge a main y despliegue.

---

## Créditos

Universidad de las Fuerzas Armadas ESPE · Desarrollo de Software Seguro · Diciembre 2025.

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

### Modelado en C++ y Python

- **mlpack 3.4.2:** Machine Learning en C++
- **Armadillo 9.8:** Álgebra lineal

---

## Cumplimiento de Especificaciones

### Requisitos Funcionales

| Requisito                       | Estado   | Evidencia                    |
| ------------------------------- | -------- | ---------------------------- |
| Modelo de Minería de Datos     | CUMPLIDO | Random Forest implementado   |
| Accuracy >= 82%                 | CUMPLIDO | 95.2% en validación cruzada |
| Pipeline CI/CD de 3 etapas      | CUMPLIDO | Security, Test, Deploy       |
| Notificaciones Telegram         | CUMPLIDO | 8 tipos de notificaciones    |
| Despliegue Automático          | CUMPLIDO | Deploy a Render.com          |
| Branch Protection               | CUMPLIDO | Configurado en test y main   |
| Detección SQL Injection        | CUMPLIDO | Feature sql_risk             |
| Detección XSS                  | CUMPLIDO | Feature xss_risk             |
| Detección Funciones Deprecated | CUMPLIDO | Feature dangerous_count      |

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

Este proyecto se distribuye bajo la licencia KAUSA.

## Referencias

### Artículos Académicos

1. Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.
2. Scandariato, R., et al. (2014). "Predicting Vulnerable Software Components via Text Mining." IEEE Transactions on Software Engineering.
3. Zimmermann, T., et al. (2010). "Searching for a Needle in a Haystack: Predicting Security Vulnerabilities for Windows Vista." International Conference on Software Engineering (ICSE).

### Bases de Datos y Estándares

4. OWASP Foundation. "OWASP Top Ten Project."URL: https://owasp.org/www-project-top-ten/
5. MITRE Corporation. "Common Vulnerabilities and Exposures (CVE)."URL: https://cve.mitre.org/
6. National Vulnerability Database (NVD).
   URL: https://nvd.nist.gov/

### Documentación Técnica

7. scikit-learn Documentation. "Random Forest Classifier."URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
8. GitHub Actions Documentation.URL: https://docs.github.com/en/actions
9. Telegram Bot API Documentation.URL: https://core.telegram.org/bots/api
10. Docker Documentation.
    URL: https://docs.docker.com/

---

## Contacto y Soporte

**Pana richie y sus kausas**

Para consultas sobre el proyecto:

- Issues del repositorio: [GitHub Issues]
- Documentación adicional: [Wiki del proyecto]

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.2
**Estado:** Completado y desplegado

```

```
