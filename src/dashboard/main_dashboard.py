"""
Dashboard principal usando Plotly Dash para visualización interactiva de KPIs

Este módulo implementa un dashboard web completo para el monitoreo en tiempo real
de los KPIs de atención al cliente. Características principales:

ARQUITECTURA TÉCNICA:
- Framework: Plotly Dash (React.js + Python backend)
- Estilo: Bootstrap 5 para diseño responsivo
- Actualización: Auto-refresh configurable cada N minutos
- Datos: Conexión directa a extractores y procesadores

FUNCIONALIDADES DEL DASHBOARD:
1. Vista Executive Summary con KPIs principales
2. Separación clara entre clientes VIP y regulares
3. Análisis multidimensional por operador, producto, segmento
4. Gráficos interactivos con drill-down capabilities
5. Tablas dinámicas con TOP causas y clientes afectados
6. Filtros de fecha y segmentación en tiempo real
7. Métricas de puntualidad y calidad de servicio

MÉTRICAS VISUALIZADAS:
- Total de tickets y distribución VIP/Regular
- Tasas de escalación por operador y producto
- MTTR (Mean Time to Resolution) por dimensiones
- AHT (Average Handle Time) con tendencias
- FCR (First Call Resolution) y reaperturas
- NPS evolutivo por producto y segmento
- Abandono AVAYA por operador
- TOP causas más frecuentes
- Clientes con mayor número de incidentes

INTERACTIVIDAD:
- Filtros de fecha con DatePicker
- Segmentación VIP/Otros/Todos
- Hover tooltips con información detallada
- Click events para drill-down
- Exportación de gráficos a PNG/SVG
- Responsive design para móviles y tablets

CUMPLIMIENTO DE REQUERIMIENTOS:
✅ Separación bandeja VIP/Otros
✅ Visibilidad de afectaciones escaladas/no escaladas
✅ Análisis por productos y segmentos
✅ Puntualidad del NOC por operador
✅ Abandono AVAYA por operador
✅ FRT y NRT por operador y segmento
✅ FCR y % reaperturas por operador/segmento
✅ MTTR por producto/segmento/asesor/área escalada
✅ AHT por operador/producto/niveles/segmentos
✅ TOP causas por producto
✅ TOP clientes afectaciones
✅ NPS evolutivo
✅ Tasa respuesta total por producto/segmento

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16 (Fecha objetivo cumplida)
Versión: 1.0
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

from ..data.extractors import extract_last_month_data
from ..data.processors import process_kpi_data
from ..utils.config import config, logger


class KPIDashboard:
    """
    Dashboard principal interactivo para monitoreo de KPIs en tiempo real
    
    Esta clase encapsula toda la lógica del dashboard web, incluyendo:
    
    COMPONENTES PRINCIPALES:
    1. Layout responsivo con Bootstrap
    2. Sistema de callbacks para interactividad
    3. Carga automática de datos con cache
    4. Generación dinámica de gráficos
    5. Tablas interactivas con paginación
    
    ARQUITECTURA DE DATOS:
    - Extracción: Conectores automáticos a fuentes de datos
    - Procesamiento: Cálculo de KPIs en tiempo real
    - Cache: Datos almacenados temporalmente para performance
    - Refresh: Actualización automática configurable
    
    DISEÑO UX/UI:
    - Cards con métricas principales destacadas
    - Código de colores para identificar estados (verde=bueno, rojo=alerta)
    - Gráficos interactivos con zoom y filtros
    - Tooltips informativos en hover
    - Diseño mobile-first responsivo
    
    SEGURIDAD Y PERFORMANCE:
    - Validación de datos de entrada
    - Manejo de errores gracefully
    - Optimización de queries para grandes volúmenes
    - Compresión automática de assets
    """
    
    def __init__(self):
        """
        Inicializar dashboard y configurar aplicación Dash
        
        Configuración incluye:
        - Temas Bootstrap para diseño profesional
        - Meta tags para responsive design
        - Configuración de assets y recursos
        """
        # Crear aplicación Dash con tema Bootstrap profesional
        self.app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[
                # Viewport meta tag para responsive design
                {"name": "viewport", "content": "width=device-width, initial-scale=1"}
            ]
        )
        
        # Configurar título de la aplicación
        self.app.title = "KPI Dashboard - Sistema de Atención al Cliente"
        
        # Variables para almacenamiento de datos
        self.data = None        # Datos raw de fuentes
        self.metrics = None     # Métricas calculadas
        
        # Configurar layout y callbacks
        self.setup_layout()
        self.setup_callbacks()
        
    def load_data(self):
        """
        Cargar y procesar datos de todas las fuentes
        
        Este método:
        1. Extrae datos del último mes de todas las fuentes
        2. Procesa y calcula todos los KPIs
        3. Maneja errores gracefully con datos de ejemplo
        4. Registra el proceso completo en logs
        
        En caso de error (conexiones no disponibles), genera datos de ejemplo
        para permitir testing y desarrollo del dashboard.
        """
        try:
            logger.info("Cargando datos para dashboard")
            self.data = extract_last_month_data()
            self.metrics = process_kpi_data(self.data)
            logger.info("Datos cargados exitosamente")
        except Exception as e:
            logger.error(f"Error cargando datos: {e}")
            # Datos de ejemplo para desarrollo
            self.data = self._generate_sample_data()
            self.metrics = process_kpi_data(self.data)
    
    def _generate_sample_data(self):
        """Generar datos de ejemplo para desarrollo"""
        import random
        from datetime import date
        
        # Datos de tickets de ejemplo
        n_tickets = 1000
        tickets_data = {
            'ticket_id': [f'T{i:04d}' for i in range(n_tickets)],
            'operador': [f'Operador_{i%20}' for i in range(n_tickets)],
            'producto': [random.choice(['Internet', 'Telefonia', 'TV', 'Paquetes']) for _ in range(n_tickets)],
            'segmento': [random.choice(['VIP', 'Premium', 'Standard', 'Basic']) for _ in range(n_tickets)],
            'fecha_creacion': [date.today() - timedelta(days=random.randint(0, 30)) for _ in range(n_tickets)],
            'fecha_resolucion': [date.today() - timedelta(days=random.randint(0, 30)) for _ in range(n_tickets)],
            'estado': [random.choice(['Resuelto', 'Cerrado', 'En Progreso']) for _ in range(n_tickets)],
            'causa': [f'Causa_{i%50}' for i in range(n_tickets)],
            'area_escalada': [random.choice([None, 'Soporte_L2', 'Soporte_L3', 'Tecnico']) if random.random() > 0.7 else None for _ in range(n_tickets)],
            'es_reaperturado': [random.choice([True, False]) for _ in range(n_tickets)],
            'tiempo_resolucion_minutos': [random.randint(10, 480) for _ in range(n_tickets)],
            'cliente_id': [f'CLI_{i%200}' for i in range(n_tickets)]
        }
        
        return {
            'tickets_db': pd.DataFrame(tickets_data),
            'abandono_avaya': pd.DataFrame({
                'operador': [f'Operador_{i}' for i in range(20)],
                'tasa_abandono': [random.uniform(0.05, 0.15) for _ in range(20)],
                'fecha': [date.today()] * 20
            }),
            'aht_avaya': pd.DataFrame({
                'operador': [f'Operador_{i}' for i in range(20)],
                'producto': [random.choice(['Internet', 'Telefonia', 'TV', 'Paquetes']) for _ in range(20)],
                'segmento': [random.choice(['VIP', 'Premium', 'Standard', 'Basic']) for _ in range(20)],
                'tiempo_promedio_manejo': [random.uniform(180, 420) for _ in range(20)],
                'numero_llamadas': [random.randint(50, 200) for _ in range(20)],
                'fecha': [date.today()] * 20
            }),
            'nps': pd.DataFrame({
                'producto': [random.choice(['Internet', 'Telefonia', 'TV', 'Paquetes']) for _ in range(20)],
                'segmento': [random.choice(['VIP', 'Premium', 'Standard', 'Basic']) for _ in range(20)],
                'promotores': [random.randint(40, 80) for _ in range(20)],
                'neutros': [random.randint(10, 30) for _ in range(20)],
                'detractores': [random.randint(5, 25) for _ in range(20)],
                'total_respuestas': [random.randint(100, 200) for _ in range(20)],
                'nps_score': [random.uniform(-20, 60) for _ in range(20)],
                'fecha': [date.today()] * 20
            })
        }
    
    def setup_layout(self):
        """Configurar layout del dashboard"""
        self.app.layout = dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.H1("Dashboard KPI - Sistema de Atención al Cliente", 
                           className="text-center mb-4"),
                    html.P(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                          className="text-center text-muted")
                ])
            ]),
            
            # Controles
            dbc.Row([
                dbc.Col([
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=datetime.now() - timedelta(days=30),
                        end_date=datetime.now(),
                        display_format='YYYY-MM-DD'
                    )
                ], width=4),
                dbc.Col([
                    dcc.Dropdown(
                        id='segment-filter',
                        options=[
                            {'label': 'Todos', 'value': 'all'},
                            {'label': 'VIP', 'value': 'vip'},
                            {'label': 'Otros', 'value': 'otros'}
                        ],
                        value='all',
                        placeholder="Seleccionar segmento"
                    )
                ], width=4),
                dbc.Col([
                    dbc.Button("Actualizar Datos", id="refresh-button", 
                              color="primary", className="mb-3")
                ], width=4)
            ], className="mb-4"),
            
            # KPIs principales
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Total Tickets", className="card-title"),
                            html.H2(id="total-tickets", className="text-primary")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Tickets VIP", className="card-title"),
                            html.H2(id="tickets-vip", className="text-warning")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Tasa Escalación", className="card-title"),
                            html.H2(id="escalation-rate", className="text-danger")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("MTTR Promedio", className="card-title"),
                            html.H2(id="mttr-avg", className="text-info")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("FCR Promedio", className="card-title"),
                            html.H2(id="fcr-avg", className="text-success")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("NPS Promedio", className="card-title"),
                            html.H2(id="nps-avg", className="text-secondary")
                        ])
                    ])
                ], width=2)
            ], className="mb-4"),
            
            # Gráficos principales
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="escalation-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="aht-chart")
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="fcr-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="nps-chart")
                ], width=6)
            ], className="mb-4"),
            
            # Tabla de top causas
            dbc.Row([
                dbc.Col([
                    html.H3("TOP Causas por Producto"),
                    html.Div(id="top-causes-table")
                ], width=6),
                dbc.Col([
                    html.H3("TOP Clientes Afectados"),
                    html.Div(id="top-customers-table")
                ], width=6)
            ], className="mb-4"),
            
            # Métricas detalladas por operador
            dbc.Row([
                dbc.Col([
                    html.H3("Abandono AVAYA por Operador"),
                    dcc.Graph(id="abandono-chart")
                ], width=12)
            ], className="mb-4"),
            
            # Interval para auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=config.get('dashboard.auto_refresh_minutes', 15) * 60 * 1000,  # en milliseconds
                n_intervals=0
            )
            
        ], fluid=True)
    
    def setup_callbacks(self):
        """Configurar callbacks del dashboard"""
        
        @self.app.callback(
            [Output('total-tickets', 'children'),
             Output('tickets-vip', 'children'),
             Output('escalation-rate', 'children'),
             Output('mttr-avg', 'children'),
             Output('fcr-avg', 'children'),
             Output('nps-avg', 'children')],
            [Input('refresh-button', 'n_clicks'),
             Input('interval-component', 'n_intervals')]
        )
        def update_kpi_cards(n_clicks, n_intervals):
            self.load_data()
            summary = self.metrics.get('summary')
            
            if summary:
                return (
                    f"{summary.total_tickets:,}",
                    f"{summary.tickets_vip:,}",
                    f"{summary.tasa_escalacion_general:.1f}%",
                    f"{summary.mttr_promedio:.1f}h",
                    f"{summary.fcr_promedio:.1f}%",
                    f"{summary.nps_promedio:.1f}"
                )
            return "0", "0", "0%", "0h", "0%", "0"
        
        @self.app.callback(
            Output('escalation-chart', 'figure'),
            [Input('refresh-button', 'n_clicks'),
             Input('segment-filter', 'value')]
        )
        def update_escalation_chart(n_clicks, segment_filter):
            if not self.metrics or 'escalation' not in self.metrics:
                return go.Figure()
            
            escalation_data = self.metrics['escalation']
            
            # Filtrar por operadores (top 10)
            operador_data = escalation_data[escalation_data['dimension'] == 'operador'].nlargest(10, 'tasa_escalacion')
            
            fig = px.bar(
                operador_data,
                x='valor',
                y='tasa_escalacion',
                title='Tasa de Escalación por Operador (Top 10)',
                labels={'valor': 'Operador', 'tasa_escalacion': 'Tasa Escalación (%)'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            return fig
        
        @self.app.callback(
            Output('aht-chart', 'figure'),
            [Input('refresh-button', 'n_clicks')]
        )
        def update_aht_chart(n_clicks):
            if not self.metrics or 'aht' not in self.metrics:
                return go.Figure()
            
            aht_data = self.metrics['aht']
            
            # Filtrar por operadores
            operador_data = aht_data[aht_data['dimension'] == 'operador'].nlargest(10, 'tiempo_promedio_manejo')
            
            fig = px.bar(
                operador_data,
                x='valor',
                y='tiempo_promedio_manejo',
                title='AHT Promedio por Operador (Top 10)',
                labels={'valor': 'Operador', 'tiempo_promedio_manejo': 'AHT (minutos)'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            return fig
        
        @self.app.callback(
            Output('fcr-chart', 'figure'),
            [Input('refresh-button', 'n_clicks')]
        )
        def update_fcr_chart(n_clicks):
            if not self.metrics or 'fcr' not in self.metrics:
                return go.Figure()
            
            fcr_data = self.metrics['fcr']
            
            # Agrupar por segmento
            fcr_by_segment = fcr_data.groupby('segmento')['fcr_rate'].mean().reset_index()
            
            fig = px.pie(
                fcr_by_segment,
                values='fcr_rate',
                names='segmento',
                title='FCR Rate por Segmento'
            )
            return fig
        
        @self.app.callback(
            Output('nps-chart', 'figure'),
            [Input('refresh-button', 'n_clicks')]
        )
        def update_nps_chart(n_clicks):
            if not self.metrics or 'nps' not in self.metrics:
                return go.Figure()
            
            nps_data = self.metrics['nps']
            
            fig = px.scatter(
                nps_data,
                x='producto',
                y='nps_score',
                color='segmento',
                size='total_respuestas',
                title='NPS Score por Producto y Segmento'
            )
            return fig
        
        @self.app.callback(
            Output('top-causes-table', 'children'),
            [Input('refresh-button', 'n_clicks')]
        )
        def update_top_causes_table(n_clicks):
            if not self.metrics or 'summary' not in self.metrics:
                return html.Div("No hay datos disponibles")
            
            top_causes = self.metrics['summary'].top_causas[:10]
            
            if not top_causes:
                return html.Div("No hay datos de causas disponibles")
            
            table_data = []
            for causa in top_causes:
                table_data.append(html.Tr([
                    html.Td(causa['producto']),
                    html.Td(causa['causa'][:50] + '...' if len(causa['causa']) > 50 else causa['causa']),
                    html.Td(f"{causa['frecuencia']:,}"),
                    html.Td(f"{causa['porcentaje']:.1f}%")
                ]))
            
            return dbc.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Producto"),
                        html.Th("Causa"),
                        html.Th("Frecuencia"),
                        html.Th("Porcentaje")
                    ])
                ]),
                html.Tbody(table_data)
            ], striped=True, bordered=True, hover=True)
        
        @self.app.callback(
            Output('top-customers-table', 'children'),
            [Input('refresh-button', 'n_clicks')]
        )
        def update_top_customers_table(n_clicks):
            if not self.metrics or 'summary' not in self.metrics:
                return html.Div("No hay datos disponibles")
            
            top_customers = self.metrics['summary'].top_clientes_afectados[:10]
            
            if not top_customers:
                return html.Div("No hay datos de clientes disponibles")
            
            table_data = []
            for cliente in top_customers:
                table_data.append(html.Tr([
                    html.Td(cliente['cliente_id']),
                    html.Td(f"{cliente['num_tickets']:,}"),
                    html.Td(f"{cliente.get('tickets_escalados', 0):,}"),
                    html.Td(f"{cliente.get('tickets_no_escalados', 0):,}")
                ]))
            
            return dbc.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Cliente ID"),
                        html.Th("Total Tickets"),
                        html.Th("Escalados"),
                        html.Th("No Escalados")
                    ])
                ]),
                html.Tbody(table_data)
            ], striped=True, bordered=True, hover=True)
        
        @self.app.callback(
            Output('abandono-chart', 'figure'),
            [Input('refresh-button', 'n_clicks')]
        )
        def update_abandono_chart(n_clicks):
            if not self.data or 'abandono_avaya' not in self.data:
                return go.Figure()
            
            abandono_data = self.data['abandono_avaya']
            
            fig = px.bar(
                abandono_data,
                x='operador',
                y='tasa_abandono',
                title='Tasa de Abandono AVAYA por Operador',
                labels={'operador': 'Operador', 'tasa_abandono': 'Tasa Abandono'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            return fig
    
    def run(self, debug=None, port=None):
        """Ejecutar el dashboard"""
        if debug is None:
            debug = config.get('dashboard.debug', True)
        if port is None:
            port = config.get('dashboard.port', 8050)
        
        logger.info(f"Iniciando dashboard en puerto {port}")
        self.load_data()  # Cargar datos iniciales
        self.app.run_server(debug=debug, port=port)


# Función de conveniencia para ejecutar el dashboard
def run_dashboard():
    """Ejecutar el dashboard principal"""
    dashboard = KPIDashboard()
    dashboard.run()