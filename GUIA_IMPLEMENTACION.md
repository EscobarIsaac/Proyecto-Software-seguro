# 🚀 GUÍA COMPLETA DE IMPLEMENTACIÓN
## Pipeline CI/CD Seguro con ML - Pasos para Aprobar

---

## ⏱️ TIEMPO ESTIMADO: 3-4 HORAS

---

## 📋 CHECKLIST DE TAREAS

### FASE 1: CONFIGURACIÓN INICIAL (30 min)
- [ ] Subir archivos al repositorio GitHub
- [ ] Ejecutar script de configuración
- [ ] Crear estructura de ramas
- [ ] Configurar bot de Telegram
- [ ] Verificar instalación de dependencias

### FASE 2: CONFIGURACIÓN GITHUB (20 min)
- [ ] Configurar GitHub Secrets
- [ ] Activar Branch Protection Rules
- [ ] Verificar que workflow está activo
- [ ] Realizar commit de prueba

### FASE 3: DESPLIEGUE EN RENDER (30 min)
- [ ] Crear cuenta en Render
- [ ] Conectar repositorio
- [ ] Configurar servicio web
- [ ] Verificar despliegue exitoso
- [ ] Probar URL de producción

### FASE 4: PRUEBAS DEL PIPELINE (1 hora)
- [ ] Probar código vulnerable (debe bloquear)
- [ ] Probar código seguro (debe aprobar)
- [ ] Verificar notificaciones Telegram
- [ ] Validar accuracy > 82%
- [ ] Ejecutar suite de pruebas

### FASE 5: DOCUMENTACIÓN (1 hora)
- [ ] Completar README con tu información
- [ ] Crear informe técnico en LaTeX
- [ ] Tomar capturas de pantalla
- [ ] Preparar presentación (8-12 min)

---

## 📝 INSTRUCCIONES DETALLADAS

### PASO 1: PREPARAR REPOSITORIO GITHUB

#### 1.1 Crear repositorio en GitHub

```bash
# En GitHub.com
1. Click en "+" → New repository
2. Nombre: "pipeline-cicd-seguro-ml"
3. Description: "Pipeline CI/CD seguro con detección de vulnerabilidades ML"
4. ✅ Public
5. ❌ NO agregar README, .gitignore, license
6. Click "Create repository"
```

#### 1.2 Subir archivos al repositorio

```bash
# En tu computadora

# 1. Inicializar git (si no lo has hecho)
cd ruta/de/tu/proyecto
git init

# 2. Agregar todos los archivos que te proporcioné
# (Asegúrate de tener todos estos archivos en tu directorio)

# 3. Configurar remote
git remote add origin https://github.com/TU-USUARIO/pipeline-cicd-seguro-ml.git

# 4. Hacer commit inicial
git add .
git commit -m "Configuración inicial del pipeline CI/CD con ML"

# 5. Push a main
git branch -M main
git push -u origin main
```

---

### PASO 2: EJECUTAR CONFIGURACIÓN AUTOMÁTICA

```bash
# Dar permisos de ejecución
chmod +x setup_project.sh

# Ejecutar script
./setup_project.sh
```

**El script te pedirá:**
1. ✅ Token del bot de Telegram
2. ✅ Chat ID de Telegram
3. ✅ Confirmación de configuración de branch protection

**Sigue las instrucciones en pantalla.**

---

### PASO 3: CONFIGURAR BOT DE TELEGRAM

#### 3.1 Crear el bot

1. Abre Telegram en tu teléfono o computadora
2. Busca: `@BotFather`
3. Envía: `/newbot`
4. Nombre del bot: "Pipeline CI/CD Monitor"
5. Username del bot: "tu_nombre_cicd_bot"
6. **Copia el TOKEN** que te da (algo como: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 3.2 Obtener Chat ID

1. Busca: `@userinfobot`
2. Envíale cualquier mensaje
3. **Copia tu Chat ID** (algo como: `123456789`)

#### 3.3 Probar el bot

```bash
# Configurar variables de entorno temporalmente
export TELEGRAM_BOT_TOKEN="tu_token_aqui"
export TELEGRAM_CHAT_ID="tu_chat_id_aqui"

# Probar
python3 telegram_notifier.py test
```

**Debes recibir un mensaje en Telegram que diga:** "🧪 Test de notificaciones - Bot de Telegram configurado correctamente!"

---

### PASO 4: CONFIGURAR GITHUB SECRETS

#### Opción A: Con GitHub CLI (Recomendado)

```bash
# Instalar GitHub CLI si no lo tienes
# macOS: brew install gh
# Linux: https://cli.github.com/
# Windows: https://cli.github.com/

# Autenticarse
gh auth login

# Configurar secrets
gh secret set TELEGRAM_BOT_TOKEN
# Pegar tu token y presionar Enter

gh secret set TELEGRAM_CHAT_ID
# Pegar tu chat ID y presionar Enter
```

#### Opción B: Manual en GitHub

1. Ve a tu repositorio en GitHub
2. `Settings` → `Secrets and variables` → `Actions`
3. Click `New repository secret`
4. Name: `TELEGRAM_BOT_TOKEN`
5. Secret: Pega tu token
6. Click `Add secret`
7. Repite para `TELEGRAM_CHAT_ID`

---

### PASO 5: CONFIGURAR BRANCH PROTECTION

En GitHub:

#### 5.1 Protección para rama `test`

1. `Settings` → `Branches` → `Add rule`
2. Branch name pattern: `test`
3. ✅ Require status checks to pass before merging
4. ✅ Require branches to be up to date before merging
5. En "Status checks", buscar y seleccionar: `security_analysis`
6. Click `Create`

#### 5.2 Protección para rama `main`

1. `Settings` → `Branches` → `Add rule`
2. Branch name pattern: `main`
3. ✅ Require status checks to pass before merging
4. ✅ Require pull request reviews before merging
5. En "Status checks", seleccionar: `security_analysis`, `merge_and_test`
6. Click `Create`

---

### PASO 6: CREAR ESTRUCTURA DE RAMAS

```bash
# Crear y push rama test
git checkout -b test
git push -u origin test

# Crear y push rama dev
git checkout -b dev
git push -u origin dev

# Volver a main
git checkout main

# Verificar ramas
git branch -a
```

**Debes ver:**
```
  dev
* main
  test
  remotes/origin/dev
  remotes/origin/main
  remotes/origin/test
```

---

### PASO 7: DESPLEGAR EN RENDER

#### 7.1 Crear cuenta

1. Ve a [render.com](https://render.com)
2. Click "Get Started"
3. Registrarse con GitHub (más fácil)

#### 7.2 Crear nuevo servicio

1. En Dashboard, click "New +"
2. Selecciona "Web Service"
3. Click "Connect account" si es tu primera vez
4. Busca tu repositorio: `pipeline-cicd-seguro-ml`
5. Click "Connect"

#### 7.3 Configurar servicio

**Basic:**
- Name: `vuln-detector-tuapellido`
- Region: `Oregon (US West)` (o el más cercano)
- Branch: `main`
- Root Directory: (dejar vacío)

**Build & Deploy:**
- Environment: `Docker`
- Auto-Deploy: `Yes`

**Instance Type:**
- Seleccionar: `Free` (0$/month)

**Environment Variables:**
Click "Add Environment Variable" dos veces:

1. Variable 1:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Tu token de Telegram

2. Variable 2:
   - Key: `TELEGRAM_CHAT_ID`
   - Value: Tu chat ID

3. Variable 3:
   - Key: `PORT`
   - Value: `5000`

#### 7.4 Deploy

1. Click "Create Web Service"
2. Esperar 5-10 minutos mientras construye
3. **Guardar la URL** (algo como: `https://vuln-detector-tuapellido.onrender.com`)

#### 7.5 Verificar despliegue

```bash
# Probar health endpoint
curl https://vuln-detector-tuapellido.onrender.com/health

# Debe responder:
# {"status":"healthy","model_loaded":true,...}
```

---

### PASO 8: PROBAR EL PIPELINE COMPLETO

#### 8.1 Prueba con CÓDIGO VULNERABLE (debe bloquear)

```bash
# Ir a rama dev
git checkout dev

# Crear archivo vulnerable
cat > test_vulnerable.py << 'EOF'
def buscar_usuario(user_id):
    """ESTE CÓDIGO ES VULNERABLE A SQL INJECTION"""
    query = "SELECT * FROM usuarios WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchone()
EOF

# Commit y push
git add test_vulnerable.py
git commit -m "Test: código vulnerable"
git push origin dev

# Crear Pull Request de dev → test
gh pr create --base test --head dev --title "Test: Código Vulnerable" --body "Prueba del sistema de detección"
```

**RESULTADO ESPERADO:**
- ❌ GitHub Actions falla el check `security_analysis`
- 🚨 Recibes notificación Telegram: "ALERTA CRÍTICA"
- 📝 Se crea issue automática
- 🏷️ PR etiquetado con "fixing-required"
- 🛑 PR bloqueado (no se puede hacer merge)

**Captura de pantalla de esto para tu informe.**

#### 8.2 Prueba con CÓDIGO SEGURO (debe aprobar)

```bash
# Cerrar PR anterior o crear nueva rama
git checkout dev
git branch -D dev-seguro 2>/dev/null
git checkout -b dev-seguro

# Crear archivo seguro
cat > calculadora.py << 'EOF'
def sumar(a, b):
    """Suma dos números de forma segura"""
    return a + b

def multiplicar(a, b):
    """Multiplica dos números"""
    return a * b
EOF

# Commit y push
git add calculadora.py
git commit -m "Feature: calculadora segura"
git push origin dev-seguro

# Crear Pull Request de dev-seguro → test
gh pr create --base test --head dev-seguro --title "Feature: Calculadora" --body "Código seguro"
```

**RESULTADO ESPERADO:**
- ✅ GitHub Actions pasa el check `security_analysis`
- ✅ Notificación Telegram: "Código seguro"
- 🔄 Merge automático a test
- 🧪 Pruebas ejecutadas: PASSED
- (Si configuras correctamente) 🔄 Merge a main
- 🚀 Despliegue automático a Render
- 🌐 Notificación Telegram con URL

**Captura de pantalla de esto para tu informe.**

---

### PASO 9: EJECUTAR Y VERIFICAR PRUEBAS

```bash
# Instalar dependencias de pruebas
pip install pytest pytest-cov

# Ejecutar suite completa
pytest tests/test_model.py -v

# Ejecutar solo prueba crítica de accuracy
pytest tests/test_model.py::TestVulnerabilityModel::test_model_accuracy_requirement -v
```

**RESULTADO ESPERADO:**
```
tests/test_model.py::TestVulnerabilityModel::test_model_accuracy_requirement PASSED

📊 Accuracy con validación cruzada 5-fold: 0.9520
   ✅ CUMPLE: Accuracy 95.20% >= 82%
```

**Toma captura de pantalla de esto.**

---

### PASO 10: PREPARAR DOCUMENTACIÓN FINAL

#### 10.1 Actualizar README

```bash
# Editar README_COMPLETO.md
# Cambiar las siguientes secciones:

1. Sección "Equipo":
   - Agregar tu nombre y el de tus compañeros
   - Agregar emails

2. Sección "Despliegue":
   - Actualizar con TU URL de Render

3. Sección "Demostración":
   - Agregar link a PR de código vulnerable
   - Agregar link a PR de código seguro

# Renombrar
mv README_COMPLETO.md README.md
```

#### 10.2 Capturas de pantalla necesarias

Toma capturas de:
1. ✅ PR bloqueado por vulnerabilidad
2. ✅ Notificación Telegram de alerta crítica
3. ✅ PR aprobado con código seguro
4. ✅ Pipeline completo ejecutado (3 etapas)
5. ✅ Aplicación desplegada en Render
6. ✅ Pruebas de accuracy > 82%
7. ✅ Bot de Telegram funcionando
8. ✅ Branch protection rules configuradas

#### 10.3 Crear informe en LaTeX

El profesor debe proporcionarte un formato. Incluye:

**Secciones mínimas:**
1. Introducción
2. Marco Teórico (Random Forest, CI/CD, DevSecOps)
3. Metodología
4. Implementación (con diagramas del pipeline)
5. Resultados (capturas de pantalla)
6. Conclusiones

---

### PASO 11: PREPARAR PRESENTACIÓN

#### Duración: 8-12 minutos

**Estructura sugerida:**

1. **Introducción (1 min)**
   - Problema a resolver
   - Objetivos del proyecto

2. **Demostración Código Vulnerable (3 min)**
   - Mostrar PR con código vulnerable
   - Explicar cómo se detecta
   - Mostrar bloqueo automático
   - Mostrar notificación Telegram

3. **Demostración Código Seguro (3 min)**
   - Mostrar PR con código seguro
   - Mostrar aprobación automática
   - Mostrar merge a test → main
   - Mostrar despliegue en Render
   - Acceder a la aplicación en producción

4. **Métricas del Modelo (2 min)**
   - Mostrar accuracy > 82%
   - Importancia de características
   - Explicar cómo funciona Random Forest

5. **Conclusiones (1 min)**
   - Cumplimiento de requisitos
   - Aprendizajes

---

## ⚠️ PROBLEMAS COMUNES Y SOLUCIONES

### Problema 1: GitHub Actions no se ejecuta

**Solución:**
1. Ve a tu repositorio → Actions
2. Si ves "Workflows aren't being run", click "Enable workflows"
3. Verifica que el archivo `.github/workflows/ci-cd-pipeline.yml` existe

### Problema 2: Bot de Telegram no envía mensajes

**Solución:**
```bash
# Verifica que los secrets están configurados
gh secret list

# Deben aparecer:
# TELEGRAM_BOT_TOKEN
# TELEGRAM_CHAT_ID

# Prueba el bot localmente
python3 telegram_notifier.py test
```

### Problema 3: Render no puede construir la imagen

**Solución:**
1. Verifica que `Dockerfile` existe en la raíz
2. Verifica que `requirements.txt` tiene todas las dependencias
3. Verifica que `train_features.csv` existe
4. Revisa los logs en Render Dashboard

### Problema 4: Branch protection no funciona

**Solución:**
1. Verifica que los nombres de checks en branch protection coincidan con los jobs del workflow
2. Los nombres deben ser EXACTOS:
   - Para test: `security_analysis`
   - Para main: `security_analysis`, `merge_and_test`

### Problema 5: Modelo no alcanza 82% accuracy

**Solución:**
```bash
# Verificar que tienes los datos correctos
ls -lh train_features.csv test_features.csv

# Re-entrenar el modelo
python preprocesar_vulnerabilidades.py
python demo_vulnerabilities.py

# Verificar accuracy
pytest tests/test_model.py::TestVulnerabilityModel::test_model_accuracy_requirement -v
```

---

## ✅ CHECKLIST FINAL ANTES DE ENTREGAR

### Repositorio GitHub
- [ ] Todos los archivos están commitados
- [ ] README.md está completo
- [ ] Ramas dev, test, main existen
- [ ] Branch protection configurado
- [ ] GitHub Secrets configurados
- [ ] Workflow ejecutándose correctamente

### Bot de Telegram
- [ ] Bot creado en BotFather
- [ ] Secrets configurados
- [ ] Mensajes de prueba recibidos
- [ ] Notificaciones funcionan en el pipeline

### Despliegue
- [ ] Aplicación desplegada en Render
- [ ] URL accesible públicamente
- [ ] Health endpoint responde
- [ ] Endpoint /analyze funciona

### Pruebas
- [ ] Suite de pruebas ejecutada
- [ ] Accuracy > 82% verificado
- [ ] Capturas de pantalla tomadas
- [ ] PRs de prueba creados (vulnerable y seguro)

### Documentación
- [ ] README con tu información
- [ ] Informe técnico en LaTeX
- [ ] Capturas de pantalla incluidas
- [ ] Presentación preparada (8-12 min)

### Demostración
- [ ] PR vulnerable que bloquea
- [ ] PR seguro que aprueba
- [ ] Flujo completo hasta producción
- [ ] Todas las notificaciones funcionan

---

## 🎯 PUNTOS CLAVE PARA LA PRESENTACIÓN

**Asegúrate de mostrar:**

1. ✅ Modelo entrenado por ti (NO LLM)
2. ✅ Accuracy > 82% demostrado
3. ✅ Pipeline de 3 etapas funcionando
4. ✅ Bloqueo automático de código vulnerable
5. ✅ Notificaciones Telegram en todas las fases
6. ✅ Aplicación desplegada y accesible
7. ✅ Branch protection rules activas
8. ✅ Merge automático funcionando

---

## 📅 TIMELINE SUGERIDO

### Día 1 (3 horas)
- Subir código a GitHub
- Configurar bot de Telegram
- Configurar GitHub Secrets
- Configurar branch protection
- Probar pipeline básico

### Día 2 (2 horas)
- Desplegar en Render
- Verificar despliegue
- Ejecutar pruebas completas
- Tomar capturas de pantalla

### Día 3 (2 horas)
- Completar README
- Crear informe en LaTeX
- Preparar presentación
- Ensayar demo

---

## 🆘 SI NECESITAS AYUDA

1. **Error en el código:** Revisa los logs de GitHub Actions
2. **Problema con Render:** Revisa los logs en Render Dashboard
3. **Bot no funciona:** Verifica tokens con @BotFather
4. **Accuracy bajo:** Verifica que los datos están completos

---

## 🎉 ¡ÉXITO!

Si completaste todos los pasos, tienes un proyecto funcional que cumple con TODOS los requisitos del documento:

✅ Modelo de minería de datos (Random Forest)  
✅ Pipeline CI/CD de 3 etapas  
✅ Notificaciones Telegram  
✅ Despliegue automático  
✅ Branch protection  
✅ Accuracy > 82%  
✅ Documentación completa  

**¡Estás listo para aprobar!** 🚀
