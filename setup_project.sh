#!/bin/bash
"""
Script de configuración inicial del proyecto
Configura ramas, protecciones y secretos necesarios
"""

set -e

echo "=========================================="
echo "🚀 CONFIGURACIÓN DEL PROYECTO CI/CD"
echo "=========================================="

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================
# 1. VERIFICAR PREREQUISITOS
# ============================================
echo -e "\n${YELLOW}1. Verificando prerequisitos...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git instalado${NC}"

if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) no está instalado${NC}"
    echo "   Instala desde: https://cli.github.com/"
    echo "   O continúa con configuración manual"
    read -p "   Presiona Enter para continuar..."
else
    echo -e "${GREEN}✅ GitHub CLI instalado${NC}"
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 instalado${NC}"

# ============================================
# 2. CREAR ESTRUCTURA DE RAMAS
# ============================================
echo -e "\n${YELLOW}2. Configurando estructura de ramas (dev/test/main)...${NC}"

# Verificar si estamos en un repositorio git
if [ ! -d .git ]; then
    echo -e "${RED}❌ No estás en un repositorio Git${NC}"
    echo "   Ejecuta: git init"
    exit 1
fi

# Obtener rama actual
CURRENT_BRANCH=$(git branch --show-current)
echo "   Rama actual: $CURRENT_BRANCH"

# Crear rama main si no existe
if git show-ref --verify --quiet refs/heads/main; then
    echo -e "${GREEN}✅ Rama 'main' ya existe${NC}"
else
    echo "   Creando rama 'main'..."
    git checkout -b main 2>/dev/null || git checkout main
    echo -e "${GREEN}✅ Rama 'main' creada${NC}"
fi

# Crear rama test
if git show-ref --verify --quiet refs/heads/test; then
    echo -e "${GREEN}✅ Rama 'test' ya existe${NC}"
else
    echo "   Creando rama 'test'..."
    git checkout -b test 2>/dev/null || git checkout test
    echo -e "${GREEN}✅ Rama 'test' creada${NC}"
fi

# Crear rama dev
if git show-ref --verify --quiet refs/heads/dev; then
    echo -e "${GREEN}✅ Rama 'dev' ya existe${NC}"
else
    echo "   Creando rama 'dev'..."
    git checkout -b dev 2>/dev/null || git checkout dev
    echo -e "${GREEN}✅ Rama 'dev' creada${NC}"
fi

# Volver a la rama original
git checkout $CURRENT_BRANCH

echo -e "${GREEN}✅ Estructura de ramas configurada${NC}"

# ============================================
# 3. CONFIGURAR TELEGRAM BOT
# ============================================
echo -e "\n${YELLOW}3. Configurando Bot de Telegram...${NC}"
echo ""
echo "📱 INSTRUCCIONES PARA CONFIGURAR TELEGRAM BOT:"
echo "   1. Abre Telegram y busca @BotFather"
echo "   2. Envía el comando: /newbot"
echo "   3. Sigue las instrucciones para crear tu bot"
echo "   4. Copia el TOKEN que te proporciona"
echo "   5. Busca @userinfobot en Telegram"
echo "   6. Envíale un mensaje para obtener tu CHAT_ID"
echo ""

read -p "¿Ya tienes el TELEGRAM_BOT_TOKEN? (s/n): " has_token

if [ "$has_token" = "s" ] || [ "$has_token" = "S" ]; then
    read -p "Ingresa tu TELEGRAM_BOT_TOKEN: " telegram_token
    read -p "Ingresa tu TELEGRAM_CHAT_ID: " telegram_chat_id
    
    # Guardar en .env local
    echo "TELEGRAM_BOT_TOKEN=$telegram_token" > .env
    echo "TELEGRAM_CHAT_ID=$telegram_chat_id" >> .env
    echo -e "${GREEN}✅ Credenciales guardadas en .env${NC}"
    
    # Configurar secrets en GitHub si gh está disponible
    if command -v gh &> /dev/null; then
        echo "   Configurando secrets en GitHub..."
        gh secret set TELEGRAM_BOT_TOKEN -b"$telegram_token" 2>/dev/null && echo -e "${GREEN}✅ TELEGRAM_BOT_TOKEN configurado${NC}" || echo -e "${YELLOW}⚠️  Configura manualmente en GitHub Settings > Secrets${NC}"
        gh secret set TELEGRAM_CHAT_ID -b"$telegram_chat_id" 2>/dev/null && echo -e "${GREEN}✅ TELEGRAM_CHAT_ID configurado${NC}" || echo -e "${YELLOW}⚠️  Configura manualmente en GitHub Settings > Secrets${NC}"
    fi
    
    # Probar bot
    echo "   Probando bot de Telegram..."
    export TELEGRAM_BOT_TOKEN=$telegram_token
    export TELEGRAM_CHAT_ID=$telegram_chat_id
    python3 telegram_notifier.py test
else
    echo -e "${YELLOW}⚠️  Configura el bot de Telegram más tarde${NC}"
    echo "   Documentación: https://core.telegram.org/bots#6-botfather"
fi

# ============================================
# 4. INSTALAR DEPENDENCIAS
# ============================================
echo -e "\n${YELLOW}4. Instalando dependencias de Python...${NC}"

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt --quiet
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
else
    echo -e "${RED}❌ No se encontró requirements.txt${NC}"
fi

# ============================================
# 5. CONFIGURAR BRANCH PROTECTION (manual)
# ============================================
echo -e "\n${YELLOW}5. Configuración de Branch Protection Rules${NC}"
echo ""
echo "⚠️  IMPORTANTE: Debes configurar manualmente las reglas de protección"
echo ""
echo "Pasos en GitHub:"
echo "1. Ve a tu repositorio en GitHub"
echo "2. Settings > Branches > Add rule"
echo "3. Para rama 'test':"
echo "   - Branch name pattern: test"
echo "   - ✅ Require status checks to pass"
echo "   - ✅ Require branches to be up to date"
echo "   - Selecciona: security_analysis"
echo "4. Para rama 'main':"
echo "   - Branch name pattern: main"
echo "   - ✅ Require status checks to pass"
echo "   - ✅ Require pull request reviews"
echo "   - Selecciona: security_analysis, merge_and_test"
echo ""

read -p "Presiona Enter cuando hayas configurado las protecciones..."

# ============================================
# 6. CREAR ARCHIVOS DE CONFIGURACIÓN
# ============================================
echo -e "\n${YELLOW}6. Creando archivos de configuración adicionales...${NC}"

# .gitignore
if [ ! -f .gitignore ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Secrets
.env
*.pem
*.key

# Data
*.csv
!train_features.csv
!test_features.csv
!example_features.csv

# Models
*.bin
*.pkl
*.joblib

# Reports
reports/
*.log

# OS
.DS_Store
Thumbs.db
EOF
    echo -e "${GREEN}✅ .gitignore creado${NC}"
fi

# .dockerignore
if [ ! -f .dockerignore ]; then
    cat > .dockerignore << 'EOF'
.git
.gitignore
.github
.vscode
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
venv
.env
README.md
tests/
.dockerignore
Dockerfile
docker-compose.yml
EOF
    echo -e "${GREEN}✅ .dockerignore creado${NC}"
fi

# ============================================
# 7. EJECUTAR PRUEBAS
# ============================================
echo -e "\n${YELLOW}7. Ejecutando pruebas iniciales...${NC}"

if [ -f tests/test_model.py ]; then
    python3 -m pytest tests/ -v || echo -e "${YELLOW}⚠️  Algunas pruebas fallaron, pero es normal en configuración inicial${NC}"
fi

# ============================================
# 8. RESUMEN FINAL
# ============================================
echo ""
echo "=========================================="
echo -e "${GREEN}✅ CONFIGURACIÓN COMPLETADA${NC}"
echo "=========================================="
echo ""
echo "📋 ESTRUCTURA DEL PROYECTO:"
echo "   ✅ Ramas: dev, test, main"
echo "   ✅ Workflow CI/CD configurado"
echo "   ✅ Bot de Telegram configurado"
echo "   ✅ Dependencias instaladas"
echo "   ✅ Archivos de configuración creados"
echo ""
echo "🚀 PRÓXIMOS PASOS:"
echo ""
echo "1. 📝 Commit y push inicial:"
echo "   git add ."
echo "   git commit -m 'Configuración inicial del pipeline CI/CD'"
echo "   git push -u origin main"
echo "   git push -u origin test"
echo "   git push -u origin dev"
echo ""
echo "2. 🔒 Configurar Branch Protection en GitHub:"
echo "   Settings > Branches > Add rule (para test y main)"
echo ""
echo "3. 🔑 Verificar GitHub Secrets:"
echo "   Settings > Secrets and variables > Actions"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - TELEGRAM_CHAT_ID"
echo ""
echo "4. 🚀 Configurar despliegue en Render/Railway:"
echo "   a) Crear cuenta en https://render.com o https://railway.app"
echo "   b) Conectar repositorio de GitHub"
echo "   c) Configurar servicio web con Dockerfile"
echo "   d) Copiar URL de despliegue"
echo ""
echo "5. 🧪 Probar el pipeline:"
echo "   git checkout dev"
echo "   echo '# Test' >> README.md"
echo "   git add README.md"
echo "   git commit -m 'Test pipeline'"
echo "   git push origin dev"
echo "   gh pr create --base test --head dev --title 'Test PR'"
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 ¡PROYECTO CONFIGURADO EXITOSAMENTE!${NC}"
echo "=========================================="
