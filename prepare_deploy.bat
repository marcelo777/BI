@echo off
REM Script de preparación para deployment en Windows

echo 🚀 Preparando Dashboard Enterprise para deployment...

REM Crear .gitignore
(
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo MANIFEST
echo.
echo # PyInstaller
echo *.manifest
echo *.spec
echo.
echo # Unit test / coverage reports
echo htmlcov/
echo .tox/
echo .coverage
echo .coverage.*
echo .cache
echo nosetests.xml
echo coverage.xml
echo *.cover
echo .hypothesis/
echo .pytest_cache/
echo.
echo # Environments
echo .env
echo .venv
echo env/
echo venv/
echo ENV/
echo env.bak/
echo venv.bak/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Logs
echo *.log
echo.
echo # Temporary files
echo *.tmp
echo *.temp
) > .gitignore

echo ✅ .gitignore creado

REM Verificar archivos necesarios
echo 🔍 Verificando archivos necesarios...

set "all_good=true"

if exist "dashboard_enterprise.py" (
    echo ✅ dashboard_enterprise.py - OK
) else (
    echo ❌ dashboard_enterprise.py - FALTA
    set "all_good=false"
)

if exist "requirements.txt" (
    echo ✅ requirements.txt - OK
) else (
    echo ❌ requirements.txt - FALTA
    set "all_good=false"
)

if exist "config\config.yaml" (
    echo ✅ config/config.yaml - OK
) else (
    echo ❌ config/config.yaml - FALTA
    set "all_good=false"
)

if exist "data\samples\sample_tickets.csv" (
    echo ✅ data/samples/sample_tickets.csv - OK
) else (
    echo ❌ data/samples/sample_tickets.csv - FALTA
    set "all_good=false"
)

if exist "data\samples\sample_avaya.csv" (
    echo ✅ data/samples/sample_avaya.csv - OK
) else (
    echo ❌ data/samples/sample_avaya.csv - FALTA
    set "all_good=false"
)

if exist "data\samples\sample_nps.csv" (
    echo ✅ data/samples/sample_nps.csv - OK
) else (
    echo ❌ data/samples/sample_nps.csv - FALTA
    set "all_good=false"
)

if exist "data\samples\sample_asesores.csv" (
    echo ✅ data/samples/sample_asesores.csv - OK
) else (
    echo ❌ data/samples/sample_asesores.csv - FALTA
    set "all_good=false"
)

echo.

if "%all_good%"=="true" (
    echo 🎉 ¡Todos los archivos están listos!
    echo.
    echo 📋 PRÓXIMOS PASOS:
    echo 1. Crea un repositorio en GitHub llamado 'kpi-dashboard-enterprise'
    echo 2. Sube todos estos archivos al repositorio
    echo 3. Ve a https://share.streamlit.io/
    echo 4. Conecta tu repositorio y deploy
    echo.
    echo 🌐 Tu dashboard estará público en minutos!
) else (
    echo ⚠️  Faltan algunos archivos. Ejecuta primero:
    echo python create_sample_data.py
)

pause