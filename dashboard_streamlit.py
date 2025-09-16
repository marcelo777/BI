"""
Dashboard Interactivo KPI Customer Service
Desarrollado con Streamlit para análisis visual de KPIs

Autor: Sistema KPI Dashboard
Fecha: 16/9/2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard KPI Customer Service",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funciones para cargar datos
@st.cache_data
def load_data():
    """Carga todos los datos de ejemplo"""
    try:
        # Obtener el directorio base del archivo actual
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Rutas de los archivos
        tickets_path = os.path.join(base_dir, "data", "samples", "sample_tickets.csv")
        avaya_path = os.path.join(base_dir, "data", "samples", "sample_avaya.csv")
        nps_path = os.path.join(base_dir, "data", "samples", "sample_nps.csv")
        asesores_path = os.path.join(base_dir, "data", "samples", "sample_asesores.csv")
        
        # Cargar datos
        tickets = pd.read_csv(tickets_path)
        avaya = pd.read_csv(avaya_path)
        nps = pd.read_csv(nps_path)
        asesores = pd.read_csv(asesores_path)
        
        # Convertir fechas
        tickets['fecha_creacion'] = pd.to_datetime(tickets['fecha_creacion'])
        tickets['fecha_resolucion'] = pd.to_datetime(tickets['fecha_resolucion'])
        avaya['fecha'] = pd.to_datetime(avaya['timestamp'])  # timestamp en lugar de fecha
        nps['fecha'] = pd.to_datetime(nps['fecha_respuesta'])  # fecha_respuesta en lugar de fecha
        
        # Renombrar columnas para consistencia
        tickets['segmento'] = tickets['segmento_cliente']
        tickets['causa'] = tickets['causa_original']
        tickets['estado'] = tickets['resuelto_primera_instancia'].map({True: 'Resuelto', False: 'Pendiente'})
        avaya['duracion_minutos'] = avaya['aht_minutos']
        nps['score'] = nps['nps_score']
        nps['producto'] = nps['producto']
        
        return tickets, avaya, nps, asesores
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None

def calculate_kpis(tickets, avaya, nps):
    """Calcula los KPIs principales"""
    try:
        # KPIs de Tickets
        total_tickets = len(tickets)
        tickets_resueltos = len(tickets[tickets['resuelto_primera_instancia'] == True])
        fcr_rate = (tickets_resueltos / total_tickets * 100) if total_tickets > 0 else 0
        
        # MTTR (Mean Time To Resolution) - usar la columna mttr_horas directamente
        mttr = tickets['mttr_horas'].mean() if len(tickets) > 0 else 0
        
        # KPIs de AVAYA
        total_llamadas = len(avaya)
        llamadas_abandonadas = len(avaya[avaya['abandonada'] == True])
        abandono_rate = (llamadas_abandonadas / total_llamadas * 100) if total_llamadas > 0 else 0
        
        # AHT (Average Handle Time)
        aht = avaya['aht_minutos'].mean() if len(avaya) > 0 else 0
        
        # NPS
        nps_promedio = nps['nps_score'].mean() if len(nps) > 0 else 0
        
        return {
            'total_tickets': total_tickets,
            'fcr_rate': fcr_rate,
            'mttr': mttr,
            'abandono_rate': abandono_rate,
            'aht': aht,
            'nps_promedio': nps_promedio,
            'total_llamadas': total_llamadas,
            'total_encuestas': len(nps)
        }
    except Exception as e:
        st.error(f"Error calculando KPIs: {e}")
        return {}

def create_kpi_cards(kpis):
    """Crea tarjetas de KPIs principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Tickets",
            value=f"{kpis.get('total_tickets', 0):,}",
            delta=None
        )
        st.metric(
            label="FCR Rate",
            value=f"{kpis.get('fcr_rate', 0):.1f}%",
            delta="vs objetivo 25%"
        )
    
    with col2:
        st.metric(
            label="MTTR",
            value=f"{kpis.get('mttr', 0):.1f}h",
            delta="vs objetivo 4h"
        )
        st.metric(
            label="Total Llamadas",
            value=f"{kpis.get('total_llamadas', 0):,}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Abandono Rate",
            value=f"{kpis.get('abandono_rate', 0):.1f}%",
            delta="vs objetivo <10%"
        )
        st.metric(
            label="AHT",
            value=f"{kpis.get('aht', 0):.1f}min",
            delta="vs objetivo 20min"
        )
    
    with col4:
        st.metric(
            label="NPS Promedio",
            value=f"{kpis.get('nps_promedio', 0):.1f}",
            delta="vs objetivo 8.0"
        )
        st.metric(
            label="Encuestas NPS",
            value=f"{kpis.get('total_encuestas', 0):,}",
            delta=None
        )

def create_tickets_charts(tickets):
    """Crea gráficos de análisis de tickets"""
    
    # Gráfico de tickets por producto
    tickets_producto = tickets['producto'].value_counts()
    fig_producto = px.bar(
        x=tickets_producto.index,
        y=tickets_producto.values,
        title="Distribución de Tickets por Producto",
        labels={'x': 'Producto', 'y': 'Cantidad de Tickets'},
        color=tickets_producto.values,
        color_continuous_scale='viridis'
    )
    fig_producto.update_layout(showlegend=False)
    
    # Gráfico de tickets por segmento
    tickets_segmento = tickets['segmento_cliente'].value_counts()
    fig_segmento = px.pie(
        values=tickets_segmento.values,
        names=tickets_segmento.index,
        title="Distribución de Tickets por Segmento"
    )
    
    # Gráfico de evolución temporal
    tickets['fecha'] = tickets['fecha_creacion'].dt.date
    tickets_tiempo = tickets.groupby('fecha').size().reset_index(name='cantidad')
    fig_tiempo = px.line(
        tickets_tiempo,
        x='fecha',
        y='cantidad',
        title="Evolución Temporal de Tickets",
        markers=True
    )
    
    return fig_producto, fig_segmento, fig_tiempo

def create_causas_analysis(tickets):
    """Análisis de causas simplificadas"""
    
    # Mapeo de causas a categorías simplificadas
    causa_mapping = {
        'Corte intermitente fibra': 'Técnica',
        'Solicitud certificado ingresos': 'Administrativa',
        'Duda promoción temporal': 'Comercial',
        'Lentitud navegación específica': 'Técnica',
        'Falta señal TV específica': 'Técnica',
        'Reactivación línea suspendida': 'Administrativa',
        'Consulta saldo actual': 'Administrativa',
        'Error facturación duplicada': 'Comercial',
        'Solicitud cambio plan': 'Comercial',
        'Configuración email móvil': 'Técnica',
        'Bloqueo internacional sin causa': 'Técnica',
        'Revisión consumos excesivos': 'Comercial'
    }
    
    # Aplicar mapeo
    tickets['categoria_causa'] = tickets['causa_original'].map(causa_mapping).fillna('Otras')
    
    # Análisis de causas
    causas_count = tickets['categoria_causa'].value_counts()
    
    # Gráfico de barras horizontales
    fig_causas = px.bar(
        x=causas_count.values,
        y=causas_count.index,
        orientation='h',
        title="TOP Causas Simplificadas",
        labels={'x': 'Cantidad de Tickets', 'y': 'Categoría'},
        color=causas_count.values,
        color_continuous_scale='plasma'
    )
    fig_causas.update_layout(yaxis={'categoryorder':'total ascending'})
    
    return fig_causas, causas_count

def create_asesores_analysis(tickets, asesores):
    """Análisis de rendimiento de asesores"""
    
    # Merge con datos de asesores - usar asesor_nombre directamente de tickets
    tickets_asesores = tickets.copy()
    
    # Análisis por asesor
    asesor_stats = tickets_asesores.groupby('asesor_nombre').agg({
        'ticket_id': 'count',  # total tickets
        'resuelto_primera_instancia': 'sum'  # tickets resueltos
    }).reset_index()
    
    asesor_stats.columns = ['asesor', 'total_tickets', 'tickets_resueltos']
    asesor_stats['fcr_rate'] = (asesor_stats['tickets_resueltos'] / asesor_stats['total_tickets'] * 100)
    asesor_stats = asesor_stats.sort_values('fcr_rate', ascending=False)
    
    # Gráfico de rendimiento de asesores (top 10)
    top_asesores = asesor_stats.head(10)
    fig_asesores = px.bar(
        top_asesores,
        x='asesor',
        y='fcr_rate',
        title="TOP 10 Asesores por FCR Rate",
        labels={'fcr_rate': 'FCR Rate (%)', 'asesor': 'Asesor'},
        color='fcr_rate',
        color_continuous_scale='greens'
    )
    fig_asesores.update_layout(xaxis={'tickangle': 45})
    
    return fig_asesores, asesor_stats

def create_nps_analysis(nps):
    """Análisis de NPS"""
    
    # NPS por producto
    nps_producto = nps.groupby('producto')['nps_score'].mean().reset_index()
    nps_producto.columns = ['producto', 'score']
    fig_nps_producto = px.bar(
        nps_producto,
        x='producto',
        y='score',
        title="NPS Promedio por Producto",
        labels={'score': 'NPS Score', 'producto': 'Producto'},
        color='score',
        color_continuous_scale='RdYlGn'
    )
    
    # Distribución de scores NPS
    fig_nps_dist = px.histogram(
        nps,
        x='nps_score',
        nbins=10,
        title="Distribución de Scores NPS",
        labels={'nps_score': 'NPS Score', 'count': 'Frecuencia'}
    )
    
    # NPS evolutivo
    nps['fecha'] = pd.to_datetime(nps['fecha_respuesta']).dt.date
    nps_tiempo = nps.groupby('fecha')['nps_score'].mean().reset_index()
    nps_tiempo.columns = ['fecha', 'score']
    fig_nps_tiempo = px.line(
        nps_tiempo,
        x='fecha',
        y='score',
        title="Evolución Temporal NPS",
        markers=True
    )
    
    return fig_nps_producto, fig_nps_dist, fig_nps_tiempo

# Función principal
def main():
    """Función principal del dashboard"""
    
    # Título principal
    st.title("Dashboard KPI Customer Service")
    st.markdown("**Análisis Integral de KPIs - Datos de Ejemplo**")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        tickets, avaya, nps, asesores = load_data()
    
    if tickets is None:
        st.error("No se pudieron cargar los datos. Asegúrate de que los archivos existan.")
        return
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    
    # Filtro de fechas
    fecha_min = tickets['fecha_creacion'].min().date()
    fecha_max = tickets['fecha_creacion'].max().date()
    
    fecha_inicio = st.sidebar.date_input(
        "Fecha inicio",
        value=fecha_min,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    fecha_fin = st.sidebar.date_input(
        "Fecha fin",
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    # Filtro por producto
    productos = ['Todos'] + list(tickets['producto'].unique())
    producto_seleccionado = st.sidebar.selectbox("Producto", productos)
    
    # Filtro por segmento
    segmentos = ['Todos'] + list(tickets['segmento_cliente'].unique())
    segmento_seleccionado = st.sidebar.selectbox("Segmento", segmentos)
    
    # Aplicar filtros
    tickets_filtrados = tickets[
        (tickets['fecha_creacion'].dt.date >= fecha_inicio) &
        (tickets['fecha_creacion'].dt.date <= fecha_fin)
    ]
    
    if producto_seleccionado != 'Todos':
        tickets_filtrados = tickets_filtrados[tickets_filtrados['producto'] == producto_seleccionado]
    
    if segmento_seleccionado != 'Todos':
        tickets_filtrados = tickets_filtrados[tickets_filtrados['segmento_cliente'] == segmento_seleccionado]
    
    # Calcular KPIs
    kpis = calculate_kpis(tickets_filtrados, avaya, nps)
    
    # Mostrar KPIs principales
    st.header("KPIs Principales")
    create_kpi_cards(kpis)
    
    st.markdown("---")
    
    # Tabs para diferentes análisis
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Análisis Tickets",
        "Análisis Causas",
        "Análisis Asesores",
        "Análisis NPS",
        "Datos Detallados"
    ])
    
    with tab1:
        st.header("Análisis de Tickets")
        
        # Crear gráficos de tickets
        fig_producto, fig_segmento, fig_tiempo = create_tickets_charts(tickets_filtrados)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_producto, use_container_width=True)
        with col2:
            st.plotly_chart(fig_segmento, use_container_width=True)
        
        st.plotly_chart(fig_tiempo, use_container_width=True)
    
    with tab2:
        st.header("Análisis de Causas")
        
        fig_causas, causas_count = create_causas_analysis(tickets_filtrados)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(fig_causas, use_container_width=True)
        
        with col2:
            st.subheader("Resumen de Causas")
            st.dataframe(
                causas_count.reset_index().rename(columns={'index': 'Categoría', 'categoria_causa': 'Tickets'}),
                use_container_width=True
            )
    
    with tab3:
        st.header("Análisis de Asesores")
        
        fig_asesores, asesor_stats = create_asesores_analysis(tickets_filtrados, asesores)
        
        st.plotly_chart(fig_asesores, use_container_width=True)
        
        # Estadísticas de asesores
        st.subheader("Estadísticas Detalladas de Asesores")
        st.dataframe(asesor_stats, use_container_width=True)
    
    with tab4:
        st.header("Análisis NPS")
        
        fig_nps_producto, fig_nps_dist, fig_nps_tiempo = create_nps_analysis(nps)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_nps_producto, use_container_width=True)
        with col2:
            st.plotly_chart(fig_nps_dist, use_container_width=True)
        
        st.plotly_chart(fig_nps_tiempo, use_container_width=True)
    
    with tab5:
        st.header("Datos Detallados")
        
        # Mostrar datos raw
        data_option = st.selectbox(
            "Seleccionar conjunto de datos:",
            ["Tickets", "AVAYA", "NPS", "Asesores"]
        )
        
        if data_option == "Tickets":
            st.dataframe(tickets_filtrados, use_container_width=True)
        elif data_option == "AVAYA":
            st.dataframe(avaya, use_container_width=True)
        elif data_option == "NPS":
            st.dataframe(nps, use_container_width=True)
        elif data_option == "Asesores":
            st.dataframe(asesores, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Dashboard KPI Customer Service** | "
        "Desarrollado con Streamlit | "
        f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

if __name__ == "__main__":
    main()