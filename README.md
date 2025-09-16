# KPI Dashboard - Sistema de Análisis de Customer Service

**Dashboard Interactivo para Análisis de KPIs de Customer Service**  
**Visualización de Datos en Tiempo Real con Streamlit**  
**Análisis de Asesores, Tickets, NPS y Datos Avaya**

## Características Principales

- **Dashboard Interactivo**: Visualización profesional de KPIs clave
- **Análisis Multi-fuente**: Asesores, Tickets, NPS, Avaya
- **Datos de Ejemplo**: Sistema completo con datos sintéticos
- **Deployment Listo**: Configurado para Streamlit Cloud, Heroku, Docker
- **Arquitectura Modular**: Código limpio y fácil de mantener

## Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone https://github.com/marcelo777/BI.git
cd BI

# Instalar dependencias
pip install -r requirements.txt

# Generar datos de ejemplo
python create_sample_data.py
```

### 2. Ejecutar Dashboard

```bash
# Lanzar dashboard interactivo
streamlit run dashboard_enterprise.py
```

El dashboard estará disponible en: `http://localhost:8501`

## KPIs Incluidos

### Customer Service

- **MTTR** (Mean Time To Resolution): Tiempo promedio de resolución
- **Tasa de Resolución**: % de tickets resueltos exitosamente
- **Satisfacción del Cliente**: Métricas basadas en NPS
- **Tendencias**: Análisis temporal de rendimiento

### Asesores

- **Ranking de Performance**: Top performers por KPIs
- **Tickets por Asesor**: Volumen y distribución de trabajo
- **Tiempo de Respuesta**: Análisis de eficiencia
- **Satisfacción por Asesor**: NPS individual

### Avaya (Call Center)

- **Volumen de Llamadas**: Análisis de tráfico
- **Tiempo de Espera**: Métricas de calidad de servicio
- **Distribución Temporal**: Patrones horarios y diarios

## Estructura del Proyecto

```text
proyecto_kpi_dashboard/
├── dashboard_enterprise.py      # Dashboard principal de Streamlit
├── create_sample_data.py       # Generador de datos de ejemplo
├── requirements.txt            # Dependencias del proyecto
├── config/
│   ├── config.yaml            # Configuración principal
│   └── config_sample_data.yaml # Config para datos de ejemplo
├── data/samples/              # Datos CSV de ejemplo
├── src/                       # Código fuente modular
│   ├── data/                 # Extractors y processors
│   ├── dashboard/            # Lógica del dashboard
│   ├── analysis/             # Análisis de KPIs
│   ├── models/               # Modelos de datos
│   └── utils/                # Utilidades y configuración
├── exports/                   # Reportes generados
└── .streamlit/               # Configuración de Streamlit
```

## Configuración

### Archivo config.yaml

```yaml
# Modo de datos (sample/production)
data_mode: 'sample'

# Configuración de archivos
data_sources:
  asesores: 'data/samples/sample_asesores.csv'
  tickets: 'data/samples/sample_tickets.csv'
  nps: 'data/samples/sample_nps.csv'
  avaya: 'data/samples/sample_avaya.csv'

# Configuración del dashboard
dashboard:
  title: "KPI Dashboard - Customer Service"
  page_title: "Dashboard Empresarial"
  layout: "wide"
```

## Deployment

### Streamlit Cloud (Recomendado)

1. **Fork/Clone** este repositorio en GitHub
2. **Conectar** a [share.streamlit.io](https://share.streamlit.io)
3. **Configurar**:
   - Repository: `marcelo777/BI`
   - Branch: `main`
   - Main file: `dashboard_enterprise.py`
4. **Deploy** automáticamente

### Heroku

```bash
# Instalar Heroku CLI y ejecutar
git init
git add .
git commit -m "Initial commit"
heroku create tu-app-name
git push heroku main
```

### Docker

```bash
# Construir imagen
docker build -t kpi-dashboard .

# Ejecutar contenedor
docker run -p 8501:8501 kpi-dashboard
```

**Guías Detalladas**: Ver `DEPLOYMENT_GUIDE.md` para instrucciones completas.

## Datos de Ejemplo

El sistema incluye un generador completo de datos sintéticos:

```bash
# Regenerar todos los datos de ejemplo
python create_sample_data.py

# Los archivos generados incluyen:
# - sample_asesores.csv    (100 asesores)
# - sample_tickets.csv     (1000 tickets)
# - sample_nps.csv         (500 encuestas NPS)
# - sample_avaya.csv       (1000 llamadas)
```

## Desarrollo

### Agregar Nuevos KPIs

1. **Definir modelo** en `src/models/kpi_models.py`
2. **Implementar análisis** en `src/analysis/`
3. **Agregar visualización** en `dashboard_enterprise.py`
4. **Actualizar configuración** en `config.yaml`

### Estructura Modular

- **`src/data/`**: Extractores y procesadores de datos
- **`src/analysis/`**: Lógica de análisis de KPIs
- **`src/dashboard/`**: Componentes del dashboard
- **`src/models/`**: Modelos de datos y KPIs
- **`src/utils/`**: Utilidades y configuración

## Requisitos

- **Python**: 3.7+
- **Dependencias**: Ver `requirements.txt`
- **Datos**: CSV files o conexión a base de datos
- **Browser**: Chrome, Firefox, Safari (para dashboard)

## Scripts de Deployment

```bash
# Windows
prepare_deploy.bat

# Linux/Mac
bash prepare_deploy.sh
```

## Features

- **Dashboard Interactivo**: Streamlit profesional
- **Múltiples KPIs**: Customer Service, Asesores, Avaya, NPS
- **Datos Sintéticos**: Sistema completo con datos de ejemplo
- **Export de Reportes**: JSON y visualizaciones
- **Configuración Flexible**: YAML configuration
- **Deployment Ready**: Streamlit Cloud, Heroku, Docker
- **Código Documentado**: Comentarios detallados
- **Arquitectura Modular**: Fácil de extender

## Contribución

1. **Fork** el proyecto
2. **Crear** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** cambios (`git commit -m 'Add AmazingFeature'`)
4. **Push** a la branch (`git push origin feature/AmazingFeature`)
5. **Abrir** Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para detalles.

## Links Útiles

- **[Streamlit Documentation](https://docs.streamlit.io/)**
- **[Plotly Documentation](https://plotly.com/python/)**
- **[Pandas Documentation](https://pandas.pydata.org/docs/)**

## Soporte

Para soporte y preguntas:

- **Issues**: Crear issue en GitHub
- **Documentation**: Ver `DEPLOYMENT_GUIDE.md`
- **Quick Start**: Ver `DEPLOY_RAPIDO.md`

---

**¡Listo para Deployment!** - Este proyecto está completamente configurado y listo para ser publicado en cualquier plataforma de hosting.