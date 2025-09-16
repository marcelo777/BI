#!/bin/bash
# Script de preparación para deployment en Streamlit Cloud

echo "🚀 Preparando Dashboard Enterprise para deployment..."

# Crear .gitignore
cat > .gitignore << EOF
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF

echo "✅ .gitignore creado"

# Verificar archivos necesarios
echo "🔍 Verificando archivos necesarios..."

files_needed=(
    "dashboard_enterprise.py"
    "requirements.txt"
    "config/config.yaml"
    "data/samples/sample_tickets.csv"
    "data/samples/sample_avaya.csv"
    "data/samples/sample_nps.csv"
    "data/samples/sample_asesores.csv"
)

all_good=true
for file in "${files_needed[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file - OK"
    else
        echo "❌ $file - FALTA"
        all_good=false
    fi
done

if [ "$all_good" = true ]; then
    echo ""
    echo "🎉 ¡Todos los archivos están listos!"
    echo ""
    echo "📋 PRÓXIMOS PASOS:"
    echo "1. Crea un repositorio en GitHub llamado 'kpi-dashboard-enterprise'"
    echo "2. Sube todos estos archivos al repositorio"
    echo "3. Ve a https://share.streamlit.io/"
    echo "4. Conecta tu repositorio y deploy"
    echo ""
    echo "🌐 Tu dashboard estará público en minutos!"
else
    echo ""
    echo "⚠️  Faltan algunos archivos. Ejecuta primero:"
    echo "python create_sample_data.py"
fi