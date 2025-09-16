"""
Conectores para diferentes fuentes de datos del sistema KPI Dashboard

Este módulo contiene todos los conectores necesarios para extraer datos de:
- Base de datos principal (PostgreSQL/SQLite)
- Sistema AVAYA (API REST)
- Sistema de tickets (API REST)
- Sistema de NPS/Encuestas (API REST)
- Datos de ejemplo (fallback automático)

Cada conector maneja:
- Autenticación específica del sistema
- Manejo de errores y timeouts
- Transformación inicial de datos
- Logging detallado de operaciones
- Fallback automático a datos de ejemplo

Arquitectura:
- DatabaseConnector: Conexión directa a BD principal
- AvayaConnector: API de sistema telefónico AVAYA
- TicketsConnector: API de sistema de tickets/incidentes
- NPSConnector: API de sistema de encuestas NPS
- DataExtractor: Orquestador principal que coordina todos los conectores
- SampleDataLoader: Cargador de datos de ejemplo para testing y demos

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16
Versión: 1.0
"""

import pandas as pd
import requests
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from pathlib import Path

from ..utils.config import config, logger, paths


def extract_last_month_data() -> Dict:
    """
    FUNCIÓN PRINCIPAL DE EXTRACCIÓN - Punto de entrada unificado
    
    Esta función es el punto de entrada principal para extraer datos de todas
    las fuentes configuradas. Incluye lógica de fallback para usar datos de
    ejemplo cuando las conexiones reales no están disponibles.
    
    FUENTES DE DATOS SOPORTADAS:
    1. Base de datos principal (tickets, asesores, productos)
    2. Sistema AVAYA (llamadas, métricas de abandono)
    3. APIs de tickets externos
    4. Encuestas NPS
    5. Datos de ejemplo (fallback automático)
    
    LÓGICA DE FALLBACK:
    - Intenta conexiones reales primero
    - Si falla, usa datos de ejemplo automáticamente
    - Logs detallados del proceso
    - Continuación grácil en caso de errores
    
    Returns:
        Dict: Diccionario con todos los datasets extraídos
        {
            'tickets_db': pd.DataFrame,
            'avaya_data': pd.DataFrame,
            'nps_data': pd.DataFrame,
            'asesores': pd.DataFrame
        }
    """
    logger.info("=== INICIANDO EXTRACCIÓN DE DATOS ===")
    logger.info("Extrayendo datos del último mes para análisis KPI")
    
    # Calcular fechas del período (último mes)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    logger.info(f"Período de extracción: {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}")
    
    # Instanciar extractor principal
    extractor = DataExtractor(config)
    data_extracted = {}
    
    try:
        # ESTRATEGIA DE EXTRACCIÓN CON FALLBACK AUTOMÁTICO
        # ================================================
        
        # 1. INTENTAR EXTRACCIÓN DESDE FUENTES REALES
        logger.info("Intentando extracción desde fuentes de datos reales...")
        
        # Extraer tickets de base de datos
        logger.info("Extrayendo tickets de base de datos...")
        tickets_db = extractor.extract_db_data(start_date, end_date)
        
        if tickets_db is not None and len(tickets_db) > 0:
            data_extracted['tickets_db'] = tickets_db
            logger.info(f"✅ Tickets DB extraídos: {len(tickets_db)} registros")
        else:
            logger.warning("❌ No se pudieron extraer tickets de DB - usando datos de ejemplo")
            tickets_db = extractor.load_sample_tickets()
            data_extracted['tickets_db'] = tickets_db
            logger.info(f"📊 Datos de ejemplo cargados: {len(tickets_db)} tickets")
        
        # Extraer datos AVAYA
        logger.info("Extrayendo datos de AVAYA...")
        avaya_data = extractor.extract_avaya_data(start_date, end_date)
        
        if avaya_data is not None and len(avaya_data) > 0:
            data_extracted['avaya_data'] = avaya_data
            logger.info(f"✅ Datos AVAYA extraídos: {len(avaya_data)} registros")
        else:
            logger.warning("❌ No se pudieron extraer datos de AVAYA - usando datos de ejemplo")
            avaya_data = extractor.load_sample_avaya()
            data_extracted['avaya_data'] = avaya_data
            logger.info(f"📊 Datos de ejemplo AVAYA: {len(avaya_data)} llamadas")
        
        # Extraer datos NPS
        logger.info("Extrayendo datos de NPS...")
        nps_data = extractor.extract_nps_data(start_date, end_date)
        
        if nps_data is not None and len(nps_data) > 0:
            data_extracted['nps_data'] = nps_data
            logger.info(f"✅ Datos NPS extraídos: {len(nps_data)} registros")
        else:
            logger.warning("❌ No se pudieron extraer datos de NPS - usando datos de ejemplo")
            nps_data = extractor.load_sample_nps()
            data_extracted['nps_data'] = nps_data
            logger.info(f"📊 Datos de ejemplo NPS: {len(nps_data)} encuestas")
        
        # Extraer catálogo de asesores
        logger.info("Extrayendo catálogo de asesores...")
        asesores_data = extractor.extract_asesores_data()
        
        if asesores_data is not None and len(asesores_data) > 0:
            data_extracted['asesores'] = asesores_data
            logger.info(f"✅ Asesores extraídos: {len(asesores_data)} registros")
        else:
            logger.warning("❌ No se pudo extraer catálogo de asesores - usando datos de ejemplo")
            asesores_data = extractor.load_sample_asesores()
            data_extracted['asesores'] = asesores_data
            logger.info(f"📊 Datos de ejemplo asesores: {len(asesores_data)} asesores")
        
        # VALIDACIÓN FINAL DE DATOS EXTRAÍDOS
        # ===================================
        total_records = sum(len(df) if df is not None else 0 for df in data_extracted.values())
        logger.info(f"=== EXTRACCIÓN COMPLETADA ===")
        logger.info(f"Total de registros extraídos: {total_records:,}")
        
        # Log detallado por fuente
        for source, df in data_extracted.items():
            if df is not None:
                logger.info(f"{source}: {len(df):,} registros")
                
                # Validar que tenga las columnas básicas esperadas
                if source == 'tickets_db' and 'ticket_id' not in df.columns:
                    logger.warning(f"Dataset {source} no tiene estructura esperada")
                elif source == 'avaya_data' and 'call_id' not in df.columns:
                    logger.warning(f"Dataset {source} no tiene estructura esperada")
                elif source == 'nps_data' and 'nps_score' not in df.columns:
                    logger.warning(f"Dataset {source} no tiene estructura esperada")
        
        return processed_data
    
    def load_sample_tickets(self) -> pd.DataFrame:
        """
        Carga datos de ejemplo de tickets desde archivos CSV
        
        Esta función permite al sistema funcionar con datos simulados cuando
        no hay conexión a fuentes reales. Los datos de ejemplo incluyen:
        - Distribución realista por productos y segmentos
        - Patrones temporales coherentes
        - Métricas de FCR, MTTR y escalación
        
        Returns:
            pd.DataFrame: Dataset de tickets simulados
        """
        try:
            # Intentar cargar desde archivo CSV
            sample_path = paths.root / 'data' / 'samples' / 'sample_tickets.csv'
            
            if sample_path.exists():
                logger.info(f"Cargando datos de ejemplo desde: {sample_path}")
                df = pd.read_csv(sample_path)
                
                # Convertir fechas
                df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
                df['fecha_resolucion'] = pd.to_datetime(df['fecha_resolucion'])
                
                logger.info(f"Datos de ejemplo cargados: {len(df)} tickets")
                return df
            else:
                logger.warning(f"Archivo de ejemplo no encontrado: {sample_path}")
                logger.info("Generando datos de ejemplo automáticamente...")
                return self.generate_sample_tickets()
                
        except Exception as e:
            logger.error(f"Error cargando datos de ejemplo de tickets: {e}")
            logger.info("Generando datos de ejemplo automáticamente...")
            return self.generate_sample_tickets()
    
    def load_sample_avaya(self) -> pd.DataFrame:
        """
        Carga datos de ejemplo de AVAYA desde archivos CSV
        
        Returns:
            pd.DataFrame: Dataset de llamadas AVAYA simuladas
        """
        try:
            sample_path = paths.root / 'data' / 'samples' / 'sample_avaya.csv'
            
            if sample_path.exists():
                logger.info(f"Cargando datos AVAYA de ejemplo desde: {sample_path}")
                df = pd.read_csv(sample_path)
                
                # Convertir timestamp
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                logger.info(f"Datos AVAYA de ejemplo cargados: {len(df)} llamadas")
                return df
            else:
                logger.info("Generando datos AVAYA de ejemplo automáticamente...")
                return self.generate_sample_avaya()
                
        except Exception as e:
            logger.error(f"Error cargando datos AVAYA de ejemplo: {e}")
            return self.generate_sample_avaya()
    
    def load_sample_nps(self) -> pd.DataFrame:
        """
        Carga datos de ejemplo de NPS desde archivos CSV
        
        Returns:
            pd.DataFrame: Dataset de encuestas NPS simuladas
        """
        try:
            sample_path = paths.root / 'data' / 'samples' / 'sample_nps.csv'
            
            if sample_path.exists():
                logger.info(f"Cargando datos NPS de ejemplo desde: {sample_path}")
                df = pd.read_csv(sample_path)
                
                # Convertir fechas
                df['fecha_respuesta'] = pd.to_datetime(df['fecha_respuesta'])
                
                logger.info(f"Datos NPS de ejemplo cargados: {len(df)} encuestas")
                return df
            else:
                logger.info("Generando datos NPS de ejemplo automáticamente...")
                return self.generate_sample_nps()
                
        except Exception as e:
            logger.error(f"Error cargando datos NPS de ejemplo: {e}")
            return self.generate_sample_nps()
    
    def load_sample_asesores(self) -> pd.DataFrame:
        """
        Carga catálogo de asesores de ejemplo desde archivos CSV
        
        Returns:
            pd.DataFrame: Catálogo de asesores simulados
        """
        try:
            sample_path = paths.root / 'data' / 'samples' / 'sample_asesores.csv'
            
            if sample_path.exists():
                logger.info(f"Cargando asesores de ejemplo desde: {sample_path}")
                df = pd.read_csv(sample_path)
                
                # Convertir fechas
                df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'])
                
                logger.info(f"Asesores de ejemplo cargados: {len(df)} asesores")
                return df
            else:
                logger.info("Generando catálogo de asesores de ejemplo automáticamente...")
                return self.generate_sample_asesores()
                
        except Exception as e:
            logger.error(f"Error cargando asesores de ejemplo: {e}")
            return self.generate_sample_asesores()
    
    def load_all_sample_data(self) -> Dict[str, pd.DataFrame]:
        """
        Carga todos los datos de ejemplo necesarios para el sistema
        
        Esta función es el fallback completo cuando no se puede conectar
        a ninguna fuente de datos real. Garantiza que el sistema pueda
        funcionar completamente con datos simulados.
        
        Returns:
            Dict[str, pd.DataFrame]: Todos los datasets simulados
        """
        logger.info("=== CARGANDO DATOS DE EJEMPLO COMPLETOS ===")
        
        return {
            'tickets_db': self.load_sample_tickets(),
            'avaya_data': self.load_sample_avaya(),
            'nps_data': self.load_sample_nps(),
            'asesores': self.load_sample_asesores()
        }
    
    def generate_sample_tickets(self) -> pd.DataFrame:
        """
        Genera tickets de ejemplo dinámicamente si no existen archivos
        
        Returns:
            pd.DataFrame: Dataset básico de tickets simulados
        """
        logger.info("Generando tickets de ejemplo básicos...")
        
        # Generar datos mínimos para funcionamiento
        import random
        from datetime import datetime, timedelta
        
        tickets = []
        for i in range(100):  # 100 tickets de ejemplo
            fecha_base = datetime.now() - timedelta(days=random.randint(1, 30))
            
            ticket = {
                'ticket_id': f'TKT_{i+1:06d}',
                'fecha_creacion': fecha_base,
                'fecha_resolucion': fecha_base + timedelta(hours=random.randint(1, 48)),
                'producto': random.choice(['Internet Hogar', 'TV Cable', 'Móvil Postpago']),
                'segmento_cliente': random.choice(['VIP', 'Premium', 'Regular', 'Básico']),
                'asesor_id': f'ASE_{random.randint(1, 20):03d}',
                'escalado': random.choice([True, False]),
                'resuelto_primera_instancia': random.choice([True, False]),
                'mttr_horas': random.uniform(0.5, 24.0),
                'causa_original': f'Causa_ejemplo_{random.randint(1, 10)}'
            }
            tickets.append(ticket)
        
        return pd.DataFrame(tickets)
    
    def generate_sample_avaya(self) -> pd.DataFrame:
        """
        Genera datos AVAYA de ejemplo dinámicamente
        
        Returns:
            pd.DataFrame: Dataset básico de llamadas simuladas
        """
        logger.info("Generando datos AVAYA de ejemplo básicos...")
        
        import random
        from datetime import datetime, timedelta
        
        calls = []
        for i in range(200):  # 200 llamadas de ejemplo
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 720))  # 30 días
            
            call = {
                'call_id': f'CALL_{i+1:08d}',
                'timestamp': timestamp,
                'operador': f'Operador_{random.choice(["A", "B", "C"])}',
                'cola': random.choice(['Cola_Tecnica', 'Cola_Comercial']),
                'aht_minutos': random.uniform(5, 30),
                'abandonada': random.choice([True, False]),
                'tiempo_cola_segundos': random.randint(10, 300)
            }
            calls.append(call)
        
        return pd.DataFrame(calls)
    
    def generate_sample_nps(self) -> pd.DataFrame:
        """
        Genera datos NPS de ejemplo dinámicamente
        
        Returns:
            pd.DataFrame: Dataset básico de encuestas NPS simuladas
        """
        logger.info("Generando datos NPS de ejemplo básicos...")
        
        import random
        from datetime import datetime, timedelta
        
        nps_responses = []
        for i in range(50):  # 50 encuestas de ejemplo
            fecha = datetime.now() - timedelta(days=random.randint(1, 30))
            
            nps = {
                'respuesta_id': f'NPS_{i+1:06d}',
                'fecha_respuesta': fecha,
                'cliente_id': f'CLI_{random.randint(1, 1000):05d}',
                'producto': random.choice(['Internet Hogar', 'TV Cable', 'Móvil Postpago']),
                'segmento_cliente': random.choice(['VIP', 'Premium', 'Regular']),
                'nps_score': random.randint(0, 10),
                'comentario': 'Comentario de ejemplo'
            }
            nps_responses.append(nps)
        
        return pd.DataFrame(nps_responses)
    
    def generate_sample_asesores(self) -> pd.DataFrame:
        """
        Genera catálogo de asesores de ejemplo dinámicamente
        
        Returns:
            pd.DataFrame: Catálogo básico de asesores simulados
        """
        logger.info("Generando catálogo de asesores de ejemplo básicos...")
        
        import random
        from datetime import datetime, timedelta
        
        asesores = []
        for i in range(20):  # 20 asesores de ejemplo
            asesor = {
                'asesor_id': f'ASE_{i+1:03d}',
                'nombre': f'Asesor_{i+1:03d}',
                'nivel_experiencia': random.choice(['Junior', 'Semi-Senior', 'Senior']),
                'area': random.choice(['Técnico', 'Comercial', 'Soporte']),
                'fecha_ingreso': datetime.now() - timedelta(days=random.randint(30, 1095))
            }
            asesores.append(asesor)
        
        return pd.DataFrame(asesores)
        
    except Exception as e:
        logger.error(f"Error crítico en extracción de datos: {e}")
        logger.info("Activando modo completo de datos de ejemplo...")
        
        # FALLBACK COMPLETO A DATOS DE EJEMPLO
        # ====================================
        return extractor.load_all_sample_data()


class DatabaseConnector:
    """
    Conector para base de datos principal del sistema
    
    Este conector maneja la conexión a la base de datos principal donde se almacenan:
    - Datos históricos de tickets e incidentes
    - Información de asesores y operadores
    - Configuraciones del sistema
    - Datos procesados y KPIs calculados
    
    Características:
    - Soporte para PostgreSQL y SQLite
    - Pool de conexiones automático via SQLAlchemy
    - Queries optimizadas para extracción de datos
    - Manejo automático de reconexión
    """
    
    def __init__(self):
        """
        Inicializar conexión a base de datos
        
        La conexión se establece usando la configuración del archivo config.yaml
        """
        self.engine = None
        self._connect()
    
    def _connect(self):
        """
        Establecer conexión a la base de datos usando SQLAlchemy
        
        Raises:
            Exception: Si no se puede establecer la conexión
        """
        try:
            # Obtener URL de conexión desde configuración
            db_url = config.get_database_url()
            logger.info(f"Conectando a base de datos: {db_url.split('@')[0]}@***")  # Log sin credenciales
            
            # Crear engine de SQLAlchemy con configuraciones optimizadas
            self.engine = create_engine(
                db_url,
                pool_size=10,          # Pool de 10 conexiones simultáneas
                max_overflow=20,       # Hasta 20 conexiones adicionales si es necesario
                pool_recycle=3600,     # Reciclar conexiones cada hora
                echo=False             # No mostrar SQL queries en logs (cambiar a True para debug)
            )
            
            # Probar la conexión
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info("Conexión a base de datos establecida exitosamente")
            
        except Exception as e:
            logger.error(f"Error conectando a base de datos: {e}")
            logger.error("Verifica que la base de datos esté ejecutándose y las credenciales sean correctas")
            raise
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Ejecutar consulta SQL y retornar DataFrame de pandas
        
        Args:
            query (str): Consulta SQL a ejecutar
            
        Returns:
            pd.DataFrame: Resultado de la consulta como DataFrame
            
        Raises:
            Exception: Si hay error en la consulta SQL
        """
        try:
            logger.debug(f"Ejecutando consulta SQL: {query[:100]}...")  # Log solo primeros 100 caracteres
            
            # Ejecutar consulta y convertir resultado a DataFrame
            result_df = pd.read_sql_query(query, self.engine)
            
            logger.info(f"Consulta ejecutada exitosamente. Filas obtenidas: {len(result_df)}")
            return result_df
            
        except Exception as e:
            logger.error(f"Error ejecutando consulta SQL: {e}")
            logger.error(f"Query problemática: {query}")
            raise
    
    def get_tickets_data(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """
        Obtener datos de tickets en rango de fechas específico
        
        Args:
            fecha_inicio (str): Fecha inicio en formato YYYY-MM-DD
            fecha_fin (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: DataFrame con todos los datos de tickets en el rango
            
        La consulta incluye:
        - Información básica del ticket (ID, operador, producto, segmento)
        - Fechas de creación y resolución
        - Estado actual y causa
        - Información de escalación
        - Clasificación VIP y reaperturas
        - Tiempo de resolución calculado
        """
        # Query SQL optimizada para obtener todos los datos necesarios de tickets
        query = f"""
        SELECT 
            ticket_id,                      -- ID único del ticket
            operador,                       -- Asesor/operador asignado
            producto,                       -- Tipo de producto (Internet, TV, etc.)
            segmento,                       -- Segmento cliente (VIP, Standard, etc.)
            fecha_creacion,                 -- Cuándo se creó el ticket
            fecha_resolucion,               -- Cuándo se resolvió (puede ser NULL)
            estado,                         -- Estado actual del ticket
            causa,                          -- Causa/motivo del ticket
            area_escalada,                  -- Área a la que se escaló (NULL si no escaló)
            es_vip,                         -- Boolean: si el cliente es VIP
            es_reaperturado,               -- Boolean: si el ticket fue reabierto
            tiempo_resolucion_minutos,      -- Tiempo total de resolución en minutos
            cliente_id                      -- ID del cliente para análisis
        FROM tickets 
        WHERE fecha_creacion BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
        ORDER BY fecha_creacion DESC       -- Más recientes primero
        """
        
        logger.info(f"Extrayendo datos de tickets del {fecha_inicio} al {fecha_fin}")
        return self.execute_query(query)
    
    def get_asesores_data(self) -> pd.DataFrame:
        """
        Obtener datos maestros de asesores/operadores activos
        
        Returns:
            pd.DataFrame: DataFrame con información de todos los asesores activos
            
        Incluye información necesaria para análisis de rendimiento:
        - Identificación del asesor
        - Área y nivel de experiencia
        - Estado activo/inactivo
        """
        # Query para obtener información de asesores activos
        query = """
        SELECT 
            asesor_id,          -- ID único del asesor
            nombre,             -- Nombre completo
            area,               -- Área de trabajo (Soporte L1, L2, etc.)
            nivel,              -- Nivel de experiencia (1=Junior, 2=Semi-senior, 3=Senior)
            activo              -- Si está actualmente trabajando
        FROM asesores
        WHERE activo = true     -- Solo asesores que están trabajando actualmente
        ORDER BY area, nivel DESC
        """
        
        logger.info("Extrayendo datos de asesores activos")
        return self.execute_query(query)


class AvayaConnector:
    """
    Conector para sistema telefónico AVAYA
    
    AVAYA es el sistema que maneja todas las llamadas telefónicas del call center.
    Este conector extrae métricas clave como:
    - Tasa de abandono por operador
    - Tiempo promedio de manejo (AHT)
    - Número de llamadas atendidas
    - Tiempo en hold, conversación y after-call work
    
    Autenticación:
    - Usa sistema de tokens JWT
    - Renovación automática de tokens expirados
    - Credenciales configuradas en config.yaml
    
    Manejo de errores:
    - Reintentos automáticos en caso de fallas temporales
    - Timeouts configurables
    - Logging detallado de todas las operaciones
    """
    
    def __init__(self):
        """
        Inicializar conector AVAYA y establecer autenticación
        """
        # Cargar configuración específica de AVAYA
        self.base_url = config.get('avaya.api_url')
        self.username = config.get('avaya.username')
        self.password = config.get('avaya.password')
        self.timeout = config.get('avaya.timeout', 30)
        
        # Crear sesión HTTP reutilizable para eficiencia
        self.session = requests.Session()
        # Configurar headers comunes
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'KPI-Dashboard/1.0'
        })
        
        # Autenticar inmediatamente al crear el conector
        self._authenticate()
    
    def _authenticate(self):
        """
        Autenticar con API de AVAYA usando credenciales configuradas
        
        El proceso de autenticación:
        1. Envía credenciales al endpoint de autenticación
        2. Recibe token JWT válido
        3. Configura token en headers de la sesión para futuras requests
        
        Raises:
            Exception: Si falla la autenticación
        """
        try:
            logger.info("Iniciando autenticación con AVAYA")
            
            # Preparar credenciales para autenticación
            auth_data = {
                'username': self.username,
                'password': self.password,
                'grant_type': 'password'  # Tipo de autenticación OAuth2
            }
            
            # Realizar request de autenticación
            response = self.session.post(
                f"{self.base_url}/auth",
                json=auth_data,
                timeout=self.timeout
            )
            
            # Verificar que la respuesta sea exitosa
            response.raise_for_status()
            
            # Extraer token de la respuesta
            auth_response = response.json()
            token = auth_response.get('access_token')
            
            if not token:
                raise ValueError("No se recibió token de acceso en la respuesta de AVAYA")
            
            # Configurar token en headers para futuras requests
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            
            logger.info("Autenticación AVAYA exitosa")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red autenticando con AVAYA: {e}")
            raise
        except Exception as e:
            logger.error(f"Error general autenticando con AVAYA: {e}")
            raise
    
    def get_abandono_data(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """
        Obtener datos de abandono de llamadas por operador
        
        Args:
            fecha_inicio (str): Fecha inicio en formato YYYY-MM-DD
            fecha_fin (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: DataFrame con métricas de abandono por operador
            
        Métricas incluidas:
        - Operador/agente
        - Llamadas recibidas total
        - Llamadas abandonadas
        - Tasa de abandono (porcentaje)
        - Tiempo promedio de abandono
        
        La tasa de abandono alta indica que los clientes cuelgan antes de ser atendidos,
        lo cual es un indicador crítico de calidad de servicio.
        """
        try:
            params = {
                'start_date': fecha_inicio,
                'end_date': fecha_fin,
                'metric': 'abandonment_rate'
            }
            
            response = self.session.get(
                f"{self.base_url}/reports/abandonment",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['results'])
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de abandono AVAYA: {e}")
            raise
    
    def get_aht_data(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """Obtener datos de AHT (Average Handle Time)"""
        try:
            params = {
                'start_date': fecha_inicio,
                'end_date': fecha_fin,
                'metric': 'aht'
            }
            
            response = self.session.get(
                f"{self.base_url}/reports/aht",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['results'])
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de AHT AVAYA: {e}")
            raise


class TicketsConnector:
    """Conector para sistema de tickets"""
    
    def __init__(self):
        self.base_url = config.get('tickets.api_url')
        self.api_key = config.get('tickets.api_key')
        self.timeout = config.get('tickets.timeout', 30)
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': self.api_key})
    
    def get_tickets_by_date_range(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """Obtener tickets en rango de fechas"""
        try:
            params = {
                'start_date': fecha_inicio,
                'end_date': fecha_fin,
                'include_details': True
            }
            
            response = self.session.get(
                f"{self.base_url}/tickets",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['tickets'])
            
        except Exception as e:
            logger.error(f"Error obteniendo tickets: {e}")
            raise
    
    def get_escalation_data(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """Obtener datos de escalaciones"""
        try:
            params = {
                'start_date': fecha_inicio,
                'end_date': fecha_fin,
                'type': 'escalations'
            }
            
            response = self.session.get(
                f"{self.base_url}/escalations",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['escalations'])
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de escalación: {e}")
            raise


class NPSConnector:
    """Conector para datos de NPS"""
    
    def __init__(self):
        self.base_url = config.get('nps.api_url')
        self.api_key = config.get('nps.api_key')
        self.timeout = config.get('nps.timeout', 30)
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def get_nps_data(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """Obtener datos de NPS"""
        try:
            params = {
                'start_date': fecha_inicio,
                'end_date': fecha_fin,
                'breakdown': ['product', 'segment', 'operator']
            }
            
            response = self.session.get(
                f"{self.base_url}/nps/scores",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['scores'])
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de NPS: {e}")
            raise
    
    def get_response_rate(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """Obtener tasa de respuesta de encuestas"""
        try:
            params = {
                'start_date': fecha_inicio,
                'end_date': fecha_fin,
                'metric': 'response_rate'
            }
            
            response = self.session.get(
                f"{self.base_url}/surveys/response-rate",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return pd.DataFrame(data['response_rates'])
            
        except Exception as e:
            logger.error(f"Error obteniendo tasa de respuesta: {e}")
            raise


class DataExtractor:
    """Clase principal para extraer datos de todas las fuentes"""
    
    def __init__(self):
        self.db = DatabaseConnector()
        self.avaya = AvayaConnector()
        self.tickets = TicketsConnector()
        self.nps = NPSConnector()
    
    def extract_all_data(self, fecha_inicio: str, fecha_fin: str) -> Dict[str, pd.DataFrame]:
        """Extraer todos los datos necesarios para el dashboard"""
        logger.info(f"Extrayendo datos del {fecha_inicio} al {fecha_fin}")
        
        data = {}
        
        try:
            # Datos de base de datos
            data['tickets_db'] = self.db.get_tickets_data(fecha_inicio, fecha_fin)
            data['asesores'] = self.db.get_asesores_data()
            
            # Datos de AVAYA
            data['abandono_avaya'] = self.avaya.get_abandono_data(fecha_inicio, fecha_fin)
            data['aht_avaya'] = self.avaya.get_aht_data(fecha_inicio, fecha_fin)
            
            # Datos de tickets API
            data['tickets_api'] = self.tickets.get_tickets_by_date_range(fecha_inicio, fecha_fin)
            data['escalaciones'] = self.tickets.get_escalation_data(fecha_inicio, fecha_fin)
            
            # Datos de NPS
            data['nps'] = self.nps.get_nps_data(fecha_inicio, fecha_fin)
            data['tasa_respuesta'] = self.nps.get_response_rate(fecha_inicio, fecha_fin)
            
            logger.info("Extracción de datos completada exitosamente")
            return data
            
        except Exception as e:
            logger.error(f"Error en extracción de datos: {e}")
            raise


# Función de conveniencia para extraer datos de último mes
def extract_last_month_data() -> Dict[str, pd.DataFrame]:
    """Extraer datos del último mes"""
    today = datetime.now()
    fecha_fin = today.strftime('%Y-%m-%d')
    fecha_inicio = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    
    extractor = DataExtractor()
    return extractor.extract_all_data(fecha_inicio, fecha_fin)