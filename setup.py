"""
Script de configuración inicial del proyecto
"""

import os
import shutil
from pathlib import Path
import yaml

def setup_project():
    """Configurar el proyecto por primera vez"""
    
    project_root = Path(__file__).parent
    config_dir = project_root / "config"
    
    print("🚀 Configurando Proyecto KPI Dashboard...")
    
    # 1. Crear directorio de logs
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ Directorio de logs creado: {logs_dir}")
    
    # 2. Copiar archivo de configuración si no existe
    config_file = config_dir / "config.yaml"
    config_example = config_dir / "config.example.yaml"
    
    if not config_file.exists() and config_example.exists():
        shutil.copy(config_example, config_file)
        print(f"✅ Archivo de configuración creado: {config_file}")
        print(f"⚠️  IMPORTANTE: Edita {config_file} con tus configuraciones reales")
    else:
        print(f"ℹ️  Archivo de configuración ya existe: {config_file}")
    
    # 3. Crear archivo .env para variables de entorno
    env_file = project_root / ".env"
    if not env_file.exists():
        env_content = """# Variables de entorno para KPI Dashboard
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kpi_database
DB_USERNAME=admin
DB_PASSWORD=password

# APIs
AVAYA_API_URL=https://avaya-api.company.com
AVAYA_USERNAME=avaya_user
AVAYA_PASSWORD=avaya_pass

TICKETS_API_URL=https://tickets-api.company.com
TICKETS_API_KEY=ticket_api_key

NPS_API_URL=https://nps-api.company.com
NPS_API_KEY=nps_api_key

# Dashboard
DASHBOARD_PORT=8050
DASHBOARD_DEBUG=true
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Archivo .env creado: {env_file}")
        print(f"⚠️  IMPORTANTE: Edita {env_file} con tus credenciales reales")
    
    # 4. Crear script de ejecución para Windows
    run_script = project_root / "run_dashboard.bat"
    if not run_script.exists():
        script_content = f"""@echo off
echo Iniciando KPI Dashboard...
cd /d "{project_root}"
python src/main.py --mode dashboard
pause
"""
        with open(run_script, 'w') as f:
            f.write(script_content)
        print(f"✅ Script de ejecución creado: {run_script}")
    
    # 5. Crear archivo de datos de ejemplo
    sample_data_dir = project_root / "data" / "sample"
    sample_data_dir.mkdir(exist_ok=True)
    
    sample_file = sample_data_dir / "README.md"
    if not sample_file.exists():
        sample_content = """# Datos de Ejemplo

Coloca aquí tus archivos de datos de ejemplo:

- `tickets_sample.xlsx` - Datos de tickets
- `asesores_sample.xlsx` - Información de asesores
- `avaya_sample.xlsx` - Datos de AVAYA
- `nps_sample.xlsx` - Datos de NPS

## Formato de Tickets (tickets_sample.xlsx)

Columnas requeridas:
- ticket_id: ID único del ticket
- operador: Nombre del operador/asesor
- producto: Tipo de producto (Internet, Telefonia, TV, etc.)
- segmento: Segmento del cliente (VIP, Premium, Standard, etc.)
- fecha_creacion: Fecha de creación del ticket
- fecha_resolucion: Fecha de resolución (puede ser vacía)
- estado: Estado actual (Abierto, Resuelto, Cerrado, etc.)
- causa: Descripción de la causa
- area_escalada: Área a la que se escaló (puede ser vacía)
- es_reaperturado: True/False si fue reaperturado
- tiempo_resolucion_minutos: Tiempo en minutos para resolver
- cliente_id: ID del cliente

## Formato de Asesores (asesores_sample.xlsx)

Columnas requeridas:
- asesor_id: ID único del asesor
- nombre: Nombre completo
- area: Área de trabajo
- nivel: Nivel del asesor (1, 2, 3)
- activo: True/False si está activo
"""
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"✅ Directorio de datos de ejemplo creado: {sample_data_dir}")
    
    print(f"\n🎉 ¡Configuración completada!")
    print(f"\n📋 Próximos pasos:")
    print(f"   1. Instalar dependencias: pip install -r requirements.txt")
    print(f"   2. Editar configuración: {config_file}")
    print(f"   3. Configurar variables de entorno: {env_file}")
    print(f"   4. Ejecutar dashboard: python src/main.py --mode dashboard")
    print(f"   5. O usar el script: {run_script}")
    print(f"\n📚 Documentación completa en: README.md")


if __name__ == "__main__":
    setup_project()