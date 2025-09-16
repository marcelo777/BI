# KPI Dashboard Enterprise - Customer Service Analytics

## NUEVO: Dashboard Enterprise Edition

¡Dashboard de nivel **Power BI / Looker Studio** completamente funcional!

### Inicio Rápido

```bash
# 1. Instalar dependencias esenciales
pip install -r requirements_enterprise.txt

# 2. Generar datos de ejemplo
python create_sample_data.py

# 3. Ejecutar Dashboard Enterprise
python -m streamlit run dashboard_enterprise.py
```

**URL del Dashboard:** http://localhost:8502

---

## ✨ Características Enterprise

### 🎨 Diseño Profesional
- **Interfaz tipo Power BI**: Diseño moderno y corporativo
- **Tema oscuro premium**: Gradientes y colores empresariales
- **Layout responsive**: Adaptable a cualquier pantalla
- **Tipografía optimizada**: Fuentes profesionales

### Gráficos Avanzados
- ** Gráficos Gauge**: Indicadores circulares con umbrales
- ** Mapas de calor**: Análisis de patrones temporales
- ** Gráficos waterfall**: Análisis de impacto por categorías
- **🔮 Tendencias con pronóstico**: Predicciones automáticas
- **🎲 Scatter plots**: Análisis de correlaciones

### Panel de Control Avanzado
- **📅 Filtros temporales**: Rangos de fechas personalizables
- ** Filtros de negocio**: Por producto y segmento
- ** Umbrales configurables**: Alertas personalizadas
- ** Exportación**: PDF y Excel (próximamente)

### 🚨 Centro de Alertas Inteligente
- **🤖 Alertas automáticas**: Basadas en reglas de negocio
- **🎨 Códigos de color**: Verde/Amarillo/Rojo por criticidad
- ** Comparaciones**: Vs. período anterior
- ** Recomendaciones**: Sugerencias de mejora

---

## Pestañas Especializadas

### 1. 🔥 Executive Dashboard
- ** Resumen ejecutivo**: Métricas clave
- ** Mapa de calor**: Volumen por día/hora
- ** Tendencias**: Con pronóstico automático
- ** Tabla ejecutiva**: Estado de todos los KPIs

### 2. Análisis Temporal
- **📅 Volumen diario**: Tendencias de tickets
- **⏰ Distribución horaria**: Patrones por hora
- **📆 Análisis semanal**: Patrones estacionales
- **🔄 Comparaciones**: Períodos históricos

### 3. Performance Asesores
- ** TOP 10**: Ranking por FCR Rate
- ** Scatter plot**: FCR vs Satisfacción
- ** Ranking completo**: Métricas detalladas
- ** Análisis individual**: Performance por asesor

### 4. 🗂 Análisis de Causas
- **🏷 Categorización**: Automática por tipo
- ** Gráfico waterfall**: Impacto por categoría
- ** Evolución temporal**: Tendencias por causa
- **🔍 Análisis profundo**: Detalles por problema

### 5. 📱 Análisis NPS
- ** Distribución**: Scores NPS detallados
- **📦 Por producto**: NPS segmentado
- **👥 Categorización**: Promotores/Neutrales/Detractores
- ** Evolución**: Tendencias temporales

---

## KPIs y Métricas

### Métricas Principales
| KPI | Objetivo | Descripción |
|-----|----------|-------------|
| **FCR Rate** | >50% | Resolución en primera llamada |
| **MTTR** | <4h | Tiempo medio de resolución |
| **Abandono Rate** | <10% | Tasa de abandono de llamadas |
| **AHT** | <20min | Tiempo medio de atención |
| **NPS Score** | >8.0 | Net Promoter Score |

### 🚨 Sistema de Alertas
- 🟢 **Verde**: Métricas dentro del objetivo
- 🟡 **Amarillo**: Métricas en rango aceptable 
- 🔴 **Rojo**: Métricas críticas que requieren acción

### Análisis Avanzados
- **Patrones temporales**: Día, hora, semana, mes
- **Categorización inteligente**: Tipos de problemas
- **Rankings de performance**: Asesores y equipos
- **Análisis de satisfacción**: NPS segmentado

---

## 📁 Estructura del Proyecto

```
proyecto_kpi_dashboard/
├── dashboard_enterprise.py # DASHBOARD ENTERPRISE ⭐
├── dashboard_streamlit.py # Dashboard básico
├── run_system.py # Sistema CLI
├── create_sample_data.py # Generador de datos
├── requirements_enterprise.txt # Dependencias mínimas
├── requirements.txt # Todas las dependencias
│
├── config/ # Configuraciones
│ ├── config.yaml # Config principal
│ └── config_sample_data.yaml # Config datos ejemplo
│
├── data/samples/ # Datos de ejemplo
│ ├── sample_tickets.csv # Tickets soporte
│ ├── sample_avaya.csv # Llamadas telefónicas
│ ├── sample_nps.csv # Encuestas NPS
│ └── sample_asesores.csv # Info asesores
│
└── src/ # Código fuente
 ├── analysis/ # Análisis especializados
 ├── data/ # Procesamiento datos
 ├── models/ # Modelos de datos
 └── utils/ # Utilidades
```

---

## Opciones de Ejecución

### Dashboard Enterprise (RECOMENDADO)
```bash
python -m streamlit run dashboard_enterprise.py
```
- **URL**: http://localhost:8502
- 🎨 **Diseño**: Nivel Power BI/Looker Studio
- **Gráficos**: Avanzados e interactivos
- 🚨 **Alertas**: Centro inteligente automático

### Dashboard Básico
```bash
python -m streamlit run dashboard_streamlit.py
```
- **URL**: http://localhost:8501
- 🎨 **Diseño**: Funcional y limpio
- **Gráficos**: Estándar con Plotly

### 💻 Análisis CLI
```bash
python run_system.py
```
- **Modo**: Línea de comandos
- **Salida**: Reportes texto/JSON
- 🤖 **Automatización**: Ideal para scripts

---

## Configuración

### config.yaml
```yaml
# Datos de ejemplo
data_sources:
 tickets_csv: "data/samples/sample_tickets.csv"
 avaya_csv: "data/samples/sample_avaya.csv"
 nps_csv: "data/samples/sample_nps.csv"
 asesores_csv: "data/samples/sample_asesores.csv"

# Umbrales de alertas
thresholds:
 fcr_rate:
 good: 50.0 # Verde: >50%
 warning: 30.0 # Amarillo: 30-50%
 critical: 20.0 # Rojo: <30%
 
 mttr_hours:
 good: 4.0 # Verde: <4h
 warning: 8.0 # Amarillo: 4-8h
 critical: 12.0 # Rojo: >8h
```

---

## 📦 Dependencias

### Enterprise (Mínimas)
```txt
streamlit>=1.49.1
plotly>=6.3.0
pandas>=2.3.2
numpy>=2.3.3
openpyxl>=3.1.0
python-dateutil>=2.8.0
PyYAML>=6.0
```

### Completas (Opcional)
- Conectores de base de datos
- Machine Learning (scikit-learn)
- Testing y documentación
- Herramientas adicionales

---

## 🆘 Solución de Problemas

### ❌ "streamlit command not found"
```bash
# Usar python -m en su lugar
python -m streamlit run dashboard_enterprise.py
```

### ❌ "File not found"
```bash
# Generar datos primero
python create_sample_data.py
```

### ❌ Errores de dependencias
```bash
# Instalar solo esenciales
pip install -r requirements_enterprise.txt
```

### ❌ Puerto ocupado
```bash
# El dashboard se abrirá en puerto disponible
# Verificar consola para URL exacta
```

---

## Enterprise vs Básico

| Característica | Dashboard Básico | Dashboard Enterprise |
|----------------|------------------|----------------------|
| **🎨 Diseño** | Funcional | Profesional Power BI |
| ** Gráficos** | Estándar | Avanzados (Gauge, etc.) |
| **🔄 Interactividad** | Básica | Completa con filtros |
| **🚨 Alertas** | ❌ No | Centro automático |
| ** Análisis** | 3 pestañas | 5 pestañas especializadas |
| ** Exportación** | ❌ No | PDF/Excel |
| ** Personalización** | Limitada | Umbrales configurables |
| ** Nivel** | Básico | Enterprise/Corporativo |

---

## 🔮 Próximas Funcionalidades

### Exportación Avanzada
- Reportes PDF automáticos
- Exportación Excel con formato
- 🔄 Programación de reportes
- 🔄 Envío automático por email

### 🤖 Inteligencia Artificial
- 🔄 Detección de anomalías
- 🔄 Predicciones ML avanzadas
- 🔄 Clustering automático
- 🔄 Recomendaciones IA

### 🔄 Tiempo Real
- 🔄 Actualización automática
- 🔄 Alertas push
- 🔄 Monitoreo continuo
- 🔄 Sincronización en vivo

---

## Soporte Técnico

### 🔍 Diagnóstico Rápido
1. Verificar archivos de datos existen
2. Comprobar configuración config.yaml
3. Revisar logs de error en consola
4. Regenerar datos: `python create_sample_data.py`

### Optimización
- **Rendimiento**: Dashboard optimizado para grandes volúmenes
- **Memoria**: Uso eficiente con `@st.cache_data`
- **Carga**: Datos precargados para respuesta rápida
- **UX**: Interfaz responsive y fluida

---

## Conclusión

**El Dashboard Enterprise ofrece una experiencia de Business Intelligence de nivel profesional, comparable con Power BI o Looker Studio, específicamente diseñado para análisis de KPIs de Customer Service.**

### ✨ Beneficios Clave
- 🎨 **Diseño profesional** que impresiona a stakeholders
- **Análisis avanzados** para toma de decisiones
- 🚨 **Alertas inteligentes** para acción proactiva
- **Personalización** según necesidades del negocio

### Ideal Para
- 👔 **Ejecutivos**: Resumen ejecutivo claro
- **Analistas**: Herramientas avanzadas de análisis
- 👥 **Managers**: Supervisión de equipos
- **Operaciones**: Monitoreo en tiempo real

---

*Desarrollado con ❤ para maximizar la eficiencia del Customer Service*