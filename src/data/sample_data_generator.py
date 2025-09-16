"""
Generador de datos de ejemplo para el Sistema KPI Dashboard

PROPÓSITO:
Este módulo genera datos simulados realistas para todas las fuentes de datos
del sistema KPI Dashboard, permitiendo ejecutar y probar todas las funcionalidades
sin necesidad de conexiones reales a bases de datos o APIs externas.

CARACTERÍSTICAS DE LOS DATOS SIMULADOS:
- Volúmenes realistas basados en operaciones reales de customer service
- Distribuciones estadísticas coherentes con patrones reales
- Correlaciones lógicas entre diferentes métricas
- Datos históricos de los últimos 90 días
- Simulación de patrones estacionales y tendencias

FUENTES DE DATOS SIMULADAS:
1. Base de datos principal (tickets, asesores, productos)
2. Sistema AVAYA (llamadas, colas, abandono)
3. Encuestas NPS por producto y segmento
4. Datos de escalación y resolución

CASOS DE USO:
- Desarrollo y testing del sistema
- Demos y presentaciones
- Validación de KPIs y métricas
- Training de nuevos usuarios

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import uuid

# Configurar semilla para reproducibilidad
np.random.seed(42)
random.seed(42)


class SampleDataGenerator:
    """
    Generador principal de datos de ejemplo
    
    Esta clase centraliza la generación de todos los datasets simulados
    necesarios para el funcionamiento completo del sistema KPI Dashboard.
    """
    
    def __init__(self, start_date: datetime = None, end_date: datetime = None):
        """
        Inicializa el generador con parámetros de configuración
        
        Args:
            start_date: Fecha inicio de los datos (default: 90 días atrás)
            end_date: Fecha fin de los datos (default: hoy)
        """
        self.end_date = end_date or datetime.now().replace(hour=23, minute=59, second=59)
        self.start_date = start_date or (self.end_date - timedelta(days=90))
        
        # Configuración de volúmenes diarios (basado en operaciones reales)
        self.daily_tickets_range = (150, 300)  # 150-300 tickets por día
        self.daily_calls_range = (500, 800)    # 500-800 llamadas por día
        self.daily_nps_range = (20, 50)        # 20-50 encuestas NPS por día
        
        # Configuración de catálogos maestros
        self.productos = [
            'Internet Hogar', 'TV Cable', 'Telefonía Fija', 'Móvil Postpago',
            'Móvil Prepago', 'Internet Móvil', 'Empresarial', 'Cloud Services'
        ]
        
        self.segmentos = ['VIP', 'Premium', 'Regular', 'Básico']
        
        self.areas_noc = ['NOC_Central', 'NOC_Norte', 'NOC_Sur', 'NOC_Este', 'NOC_Oeste']
        
        self.operadores = [
            'Operador_A', 'Operador_B', 'Operador_C', 'Operador_D', 'Operador_E'
        ]
        
        # Generar asesores con perfiles realistas
        self.asesores = self._generate_asesores_catalog()
        
        # Configurar causas originales (90+ como en requerimientos)
        self.causas_originales = self._generate_causas_catalog()
    
    def _generate_asesores_catalog(self) -> List[Dict]:
        """
        Genera catálogo de asesores con perfiles realistas
        
        Simula 50 asesores con diferentes niveles de experiencia,
        especialidades y patrones de rendimiento típicos.
        
        Returns:
            List[Dict]: Lista de asesores con sus características
        """
        asesores = []
        
        # Niveles de experiencia y sus características típicas
        niveles_experiencia = [
            {'nivel': 'Junior', 'cantidad': 20, 'fcr_base': 0.15, 'aht_base': 25},
            {'nivel': 'Semi-Senior', 'cantidad': 20, 'fcr_base': 0.25, 'aht_base': 20},
            {'nivel': 'Senior', 'cantidad': 10, 'fcr_base': 0.35, 'aht_base': 18}
        ]
        
        asesor_id = 1
        for nivel_info in niveles_experiencia:
            for i in range(nivel_info['cantidad']):
                # Simular variabilidad individual dentro del nivel
                fcr_variation = np.random.normal(0, 0.05)  # ±5% variación
                aht_variation = np.random.normal(0, 3)     # ±3 min variación
                
                asesor = {
                    'asesor_id': f'ASE_{asesor_id:03d}',
                    'nombre': f'Asesor_{asesor_id:03d}',
                    'nivel_experiencia': nivel_info['nivel'],
                    'fcr_esperado': max(0.05, nivel_info['fcr_base'] + fcr_variation),
                    'aht_esperado': max(10, nivel_info['aht_base'] + aht_variation),
                    'area': random.choice(['Técnico', 'Comercial', 'Retención', 'Soporte']),
                    'turno': random.choice(['Mañana', 'Tarde', 'Noche']),
                    'fecha_ingreso': self.start_date - timedelta(days=random.randint(30, 1095))
                }
                
                asesores.append(asesor)
                asesor_id += 1
        
        return asesores
    
    def _generate_causas_catalog(self) -> List[str]:
        """
        Genera catálogo de 90+ causas originales para simular la complejidad real
        
        Estas causas representan la situación actual donde hay demasiadas
        categorías específicas que necesitan ser simplificadas.
        
        Returns:
            List[str]: Lista de 95 causas diferentes
        """
        causas_base = [
            # Técnicas (35 causas)
            'Sin señal TV canal específico', 'Lentitud navegación específica',
            'Corte intermitente fibra', 'Ruido línea telefónica matutino',
            'Falla WiFi 5GHz específica', 'Error configuración router modelo X',
            'Interferencia microondas', 'Sobrecalentamiento ONT verano',
            'Falla cable coaxial humedad', 'Error DNS específico',
            'Congestión nodo hora pico', 'Falla amplificador sector norte',
            'Problema sincronización ADSL', 'Error DHCP renovación',
            'Interferencia bluetooth', 'Falla splitter antiguo',
            'Problema NAT específico', 'Error VoIP codecs',
            'Falla switch cascada', 'Problema QoS streaming',
            'Error firewall bloqueo', 'Problema IPv6 transición',
            'Falla modem DOCSIS 3.0', 'Error certificados SSL',
            'Problema VPN corporativa', 'Falla UPS respaldo',
            'Error configuración VLAN', 'Problema mesh network',
            'Falla fibra empalme', 'Error autenticación 802.1X',
            'Problema CDN contenido', 'Falla ethernet gigabit',
            'Error protocolo PPPoE', 'Problema load balancing',
            'Falla backup automático',
            
            # Comerciales (25 causas)
            'Consulta plan específico región A', 'Duda promoción temporal',
            'Cambio plan mayor capacidad', 'Downgrade plan básico',
            'Consulta roaming país específico', 'Duda facturación detallada',
            'Reclamo cargo no reconocido', 'Consulta descuento veteranos',
            'Cambio ciclo facturación', 'Duda impuestos regionales',
            'Consulta plan empresarial', 'Cambio titular cuenta',
            'Duda garantía extendida', 'Consulta financiamiento',
            'Reclamo doble cobro', 'Consulta portabilidad',
            'Duda plan familiar', 'Cambio método pago',
            'Consulta beneficios fidelidad', 'Reclamo promoción no aplicada',
            'Duda términos contrato', 'Consulta suspensión temporal',
            'Cambio dirección facturación', 'Duda plan prepago corporativo',
            'Consulta migración tecnología',
            
            # Administrativas (35 causas)
            'Actualización datos personales específicos', 'Cambio email contacto',
            'Solicitud certificado ingresos', 'Consulta historial pagos',
            'Cambio fecha vencimiento', 'Solicitud factura duplicada',
            'Consulta saldo a favor', 'Cambio forma entrega factura',
            'Solicitud constancia servicio', 'Consulta política privacidad',
            'Cambio PIN seguridad', 'Solicitud bloqueo línea',
            'Consulta cobertura zona específica', 'Cambio idioma preferencia',
            'Solicitud instalación técnica', 'Consulta horarios atención',
            'Cambio autorizado cuenta', 'Solicitud visita técnica',
            'Consulta términos legales', 'Cambio notificaciones SMS',
            'Solicitud desbloqueo equipo', 'Consulta proceso reclamos',
            'Cambio sucursal atención', 'Solicitud manual usuario',
            'Consulta canales digitales', 'Cambio configuración alertas',
            'Solicitud backup configuración', 'Consulta app móvil',
            'Cambio preferencias marketing', 'Solicitud exportar datos',
            'Consulta programa lealtad', 'Cambio zona horaria',
            'Solicitud eliminar cuenta', 'Consulta accesibilidad',
            'Cambio configuración parentales'
        ]
        
        return causas_base
    
    def generate_tickets_data(self) -> pd.DataFrame:
        """
        Genera dataset de tickets con distribuciones realistas
        
        Simula el comportamiento real de tickets de customer service incluyendo:
        - Patrones estacionales (más tickets en fin de semana)
        - Distribución por productos y segmentos
        - Escalaciones basadas en complejidad
        - Tiempos de resolución variables
        - Reaperturas con probabilidades realistas
        
        Returns:
            pd.DataFrame: Dataset de tickets simulados
        """
        tickets = []
        current_date = self.start_date
        ticket_id = 1
        
        while current_date <= self.end_date:
            # Calcular volumen diario con variabilidad estacional
            base_volume = random.randint(*self.daily_tickets_range)
            
            # Aumentar tickets en fin de semana (más uso residencial)
            if current_date.weekday() >= 5:  # Sábado o Domingo
                base_volume = int(base_volume * 1.3)
            
            # Generar tickets para el día
            for _ in range(base_volume):
                # Seleccionar características con distribuciones realistas
                producto = np.random.choice(self.productos, p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.08, 0.05, 0.02])
                segmento = np.random.choice(self.segmentos, p=[0.10, 0.20, 0.50, 0.20])
                asesor = random.choice(self.asesores)
                causa_original = random.choice(self.causas_originales)
                
                # Generar timestamp realista (horario laboral principalmente)
                if current_date.weekday() < 5:  # Días laborales
                    hour = max(8, min(22, int(np.random.normal(14, 4))))
                else:  # Fines de semana
                    hour = max(9, min(21, int(np.random.normal(15, 3))))
                
                timestamp_creacion = current_date.replace(
                    hour=hour,
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                )
                
                # Determinar escalación basada en producto y complejidad
                escalado = self._determine_escalation(producto, causa_original, segmento)
                
                # Calcular tiempo de resolución basado en múltiples factores
                mttr_hours = self._calculate_realistic_mttr(
                    producto, segmento, escalado, asesor['nivel_experiencia'], causa_original
                )
                
                timestamp_resolucion = timestamp_creacion + timedelta(hours=mttr_hours)
                
                # Determinar si fue resuelto en primera instancia (FCR)
                fcr = self._determine_fcr(asesor, producto, causa_original)
                
                # Simular reapertura (5-15% de probabilidad)
                reabierto = random.random() < 0.08 if fcr else random.random() < 0.20
                
                ticket = {
                    'ticket_id': f'TKT_{ticket_id:06d}',
                    'fecha_creacion': timestamp_creacion,
                    'fecha_resolucion': timestamp_resolucion,
                    'producto': producto,
                    'segmento_cliente': segmento,
                    'asesor_id': asesor['asesor_id'],
                    'asesor_nombre': asesor['nombre'],
                    'asesor_nivel': asesor['nivel_experiencia'],
                    'causa_original': causa_original,
                    'area_responsable': asesor['area'],
                    'escalado': escalado,
                    'escalado_a': random.choice(self.areas_noc) if escalado else None,
                    'resuelto_primera_instancia': fcr,
                    'reabierto': reabierto,
                    'mttr_horas': mttr_hours,
                    'satisfaccion_cliente': self._generate_satisfaction_score(fcr, mttr_hours, escalado),
                    'cliente_id': f'CLI_{random.randint(1, 50000):05d}',
                    'canal_entrada': np.random.choice(['Web', 'Telefono', 'App', 'Presencial'], p=[0.40, 0.35, 0.20, 0.05]),
                    'prioridad': self._determine_priority(segmento, producto),
                    'complejidad': self._determine_complexity(causa_original),
                }
                
                tickets.append(ticket)
                ticket_id += 1
            
            current_date += timedelta(days=1)
        
        return pd.DataFrame(tickets)
    
    def _determine_escalation(self, producto: str, causa: str, segmento: str) -> bool:
        """
        Determina si un ticket debe ser escalado basado en reglas de negocio
        
        Args:
            producto: Tipo de producto
            causa: Causa del ticket
            segmento: Segmento del cliente
            
        Returns:
            bool: True si debe ser escalado
        """
        # Productos técnicos complejos tienen mayor probabilidad de escalación
        escalation_probability = 0.15  # Base 15%
        
        if 'Empresarial' in producto or 'Cloud' in producto:
            escalation_probability += 0.10
        
        if segmento == 'VIP':
            escalation_probability += 0.05
        
        # Causas técnicas complejas
        if any(keyword in causa.lower() for keyword in ['fibra', 'configuración', 'error', 'falla']):
            escalation_probability += 0.08
        
        return random.random() < escalation_probability
    
    def _calculate_realistic_mttr(self, producto: str, segmento: str, escalado: bool, 
                                 asesor_nivel: str, causa: str) -> float:
        """
        Calcula MTTR realista basado en múltiples factores
        
        Args:
            producto: Tipo de producto
            segmento: Segmento del cliente
            escalado: Si fue escalado
            asesor_nivel: Nivel de experiencia del asesor
            causa: Causa del ticket
            
        Returns:
            float: MTTR en horas
        """
        # MTTR base por tipo de causa
        if 'consulta' in causa.lower():
            base_mttr = 0.5  # 30 minutos
        elif any(keyword in causa.lower() for keyword in ['cambio', 'actualización']):
            base_mttr = 1.0  # 1 hora
        elif any(keyword in causa.lower() for keyword in ['falla', 'error', 'problema']):
            base_mttr = 4.0  # 4 horas
        else:
            base_mttr = 2.0  # 2 horas por defecto
        
        # Ajustes por nivel de asesor
        if asesor_nivel == 'Junior':
            base_mttr *= 1.5
        elif asesor_nivel == 'Senior':
            base_mttr *= 0.7
        
        # Ajustes por escalación
        if escalado:
            base_mttr += random.uniform(8, 24)  # 8-24 horas adicionales
        
        # Ajustes por segmento (VIP tiene prioridad)
        if segmento == 'VIP':
            base_mttr *= 0.6
        elif segmento == 'Premium':
            base_mttr *= 0.8
        
        # Añadir variabilidad realista
        mttr = max(0.1, base_mttr * random.uniform(0.5, 2.0))
        
        return round(mttr, 2)
    
    def _determine_fcr(self, asesor: Dict, producto: str, causa: str) -> bool:
        """
        Determina si un ticket fue resuelto en primera instancia (FCR)
        
        Args:
            asesor: Información del asesor
            producto: Tipo de producto
            causa: Causa del ticket
            
        Returns:
            bool: True si fue FCR
        """
        fcr_probability = asesor['fcr_esperado']
        
        # Ajustar por complejidad de la causa
        if 'consulta' in causa.lower():
            fcr_probability += 0.30
        elif any(keyword in causa.lower() for keyword in ['falla', 'error']):
            fcr_probability -= 0.15
        
        # Ajustar por producto
        if 'Empresarial' in producto:
            fcr_probability -= 0.10
        
        return random.random() < min(0.95, max(0.05, fcr_probability))
    
    def _generate_satisfaction_score(self, fcr: bool, mttr: float, escalado: bool) -> int:
        """
        Genera score de satisfacción basado en factores de calidad
        
        Args:
            fcr: Si fue resuelto en primera instancia
            mttr: Tiempo de resolución en horas
            escalado: Si fue escalado
            
        Returns:
            int: Score de satisfacción (1-10)
        """
        base_score = 7.0
        
        if fcr:
            base_score += 1.5
        
        if mttr <= 1:
            base_score += 1.0
        elif mttr >= 24:
            base_score -= 2.0
        
        if escalado:
            base_score -= 0.5
        
        # Añadir variabilidad
        score = base_score + random.uniform(-1, 1)
        
        return max(1, min(10, int(round(score))))
    
    def _determine_priority(self, segmento: str, producto: str) -> str:
        """Determina prioridad del ticket"""
        if segmento == 'VIP':
            return 'Alta'
        elif 'Empresarial' in producto:
            return 'Alta'
        elif segmento == 'Premium':
            return 'Media'
        else:
            return random.choice(['Baja', 'Media'])
    
    def _determine_complexity(self, causa: str) -> str:
        """Determina complejidad basada en la causa"""
        if 'consulta' in causa.lower():
            return 'Baja'
        elif any(keyword in causa.lower() for keyword in ['falla', 'error', 'problema']):
            return 'Alta'
        else:
            return 'Media'


def generate_sample_avaya_data(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Genera datos simulados de AVAYA (sistema de llamadas)
    
    Simula métricas realistas de call center incluyendo:
    - Llamadas entrantes por operador y cola
    - Tasas de abandono variables por horario
    - AHT (Average Handle Time) realista
    - Distribución por productos y tipos de llamada
    
    Args:
        start_date: Fecha inicio
        end_date: Fecha fin
        
    Returns:
        pd.DataFrame: Dataset de llamadas AVAYA
    """
    calls = []
    call_id = 1
    current_date = start_date
    
    operadores = ['Operador_A', 'Operador_B', 'Operador_C', 'Operador_D', 'Operador_E']
    colas = ['Cola_Tecnica', 'Cola_Comercial', 'Cola_Retencion', 'Cola_Soporte']
    
    while current_date <= end_date:
        # Volumen diario de llamadas
        daily_calls = random.randint(500, 800)
        
        # Más llamadas en días laborales
        if current_date.weekday() >= 5:
            daily_calls = int(daily_calls * 0.7)
        
        for _ in range(daily_calls):
            # Hora realista (concentración en horarios de oficina)
            if current_date.weekday() < 5:
                hour = max(8, min(20, int(np.random.normal(13, 3))))
            else:
                hour = max(10, min(18, int(np.random.normal(14, 2))))
            
            timestamp = current_date.replace(
                hour=hour,
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            operador = random.choice(operadores)
            cola = random.choice(colas)
            
            # AHT realista basado en tipo de cola
            if cola == 'Cola_Tecnica':
                aht_minutes = max(5, np.random.normal(22, 8))
            elif cola == 'Cola_Comercial':
                aht_minutes = max(3, np.random.normal(15, 5))
            elif cola == 'Cola_Retencion':
                aht_minutes = max(8, np.random.normal(35, 12))
            else:
                aht_minutes = max(4, np.random.normal(18, 6))
            
            # Determinar abandono (mayor en horas pico)
            abandono_prob = 0.08  # Base 8%
            if 12 <= hour <= 14 or 17 <= hour <= 19:  # Horas pico
                abandono_prob += 0.05
            
            abandonada = random.random() < abandono_prob
            
            # Tiempo en cola (mayor si hay abandono)
            if abandonada:
                tiempo_cola = max(30, np.random.normal(180, 60))  # 3 min promedio
                aht_minutes = 0
            else:
                tiempo_cola = max(5, np.random.normal(45, 20))   # 45 seg promedio
            
            call = {
                'call_id': f'CALL_{call_id:08d}',
                'timestamp': timestamp,
                'operador': operador,
                'cola': cola,
                'tiempo_cola_segundos': int(tiempo_cola),
                'aht_minutos': round(aht_minutes, 2),
                'abandonada': abandonada,
                'transferida': random.random() < 0.12,  # 12% transferencias
                'producto_consultado': random.choice([
                    'Internet Hogar', 'TV Cable', 'Telefonía Fija', 'Móvil Postpago',
                    'Móvil Prepago', 'Internet Móvil', 'Empresarial', 'General'
                ]),
                'tipo_llamada': random.choice(['Consulta', 'Reclamo', 'Soporte_Tecnico', 'Comercial']),
                'satisfaccion_llamada': random.randint(1, 10) if not abandonada else None,
                'cliente_id': f'CLI_{random.randint(1, 50000):05d}',
                'numero_origen': f'+56{random.randint(900000000, 999999999)}',
                'duracion_total_segundos': int(tiempo_cola + (aht_minutes * 60)) if not abandonada else int(tiempo_cola)
            }
            
            calls.append(call)
            call_id += 1
        
        current_date += timedelta(days=1)
    
    return pd.DataFrame(calls)


def generate_sample_nps_data(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Genera datos simulados de encuestas NPS
    
    Simula respuestas realistas de NPS incluyendo:
    - Distribución por productos y segmentos
    - Variabilidad temporal
    - Correlación con eventos de servicio
    - Comentarios categorializados
    
    Args:
        start_date: Fecha inicio
        end_date: Fecha fin
        
    Returns:
        pd.DataFrame: Dataset de encuestas NPS
    """
    nps_responses = []
    response_id = 1
    current_date = start_date
    
    productos = [
        'Internet Hogar', 'TV Cable', 'Telefonía Fija', 'Móvil Postpago',
        'Móvil Prepago', 'Internet Móvil', 'Empresarial', 'Cloud Services'
    ]
    segmentos = ['VIP', 'Premium', 'Regular', 'Básico']
    
    # Comentarios típicos por rango de NPS
    comentarios_detractores = [
        'Servicio muy lento, muchas fallas',
        'Atención al cliente deficiente',
        'Problemas técnicos constantes',
        'Precio muy alto para el servicio',
        'Tiempo de espera excesivo'
    ]
    
    comentarios_neutrales = [
        'Servicio regular, podría mejorar',
        'Funciona pero tiene algunos problemas',
        'Precio aceptable, servicio promedio',
        'Atención correcta pero no excepcional',
        'Cumple expectativas básicas'
    ]
    
    comentarios_promotores = [
        'Excelente servicio, muy satisfecho',
        'Atención rápida y efectiva',
        'Buena relación calidad-precio',
        'Personal muy profesional',
        'Recomiendo totalmente el servicio'
    ]
    
    while current_date <= end_date:
        # Volumen diario de encuestas NPS
        daily_surveys = random.randint(20, 50)
        
        for _ in range(daily_surveys):
            producto = random.choice(productos)
            segmento = np.random.choice(segmentos, p=[0.10, 0.20, 0.50, 0.20])
            
            # NPS score basado en segmento y producto
            if segmento == 'VIP':
                nps_base = 8.5
            elif segmento == 'Premium':
                nps_base = 7.5
            elif segmento == 'Regular':
                nps_base = 6.5
            else:
                nps_base = 5.5
            
            # Ajuste por producto
            if producto in ['Empresarial', 'Cloud Services']:
                nps_base += 0.5
            elif producto in ['Móvil Prepago']:
                nps_base -= 0.5
            
            # Generar score con variabilidad
            nps_score = max(0, min(10, int(round(nps_base + np.random.normal(0, 1.5)))))
            
            # Categorizar respuesta
            if nps_score <= 6:
                categoria = 'Detractor'
                comentario = random.choice(comentarios_detractores)
            elif nps_score <= 8:
                categoria = 'Neutral'
                comentario = random.choice(comentarios_neutrales)
            else:
                categoria = 'Promotor'
                comentario = random.choice(comentarios_promotores)
            
            # Timestamp
            timestamp = current_date.replace(
                hour=random.randint(8, 22),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            nps_response = {
                'respuesta_id': f'NPS_{response_id:06d}',
                'fecha_respuesta': timestamp,
                'cliente_id': f'CLI_{random.randint(1, 50000):05d}',
                'producto': producto,
                'segmento_cliente': segmento,
                'nps_score': nps_score,
                'categoria_nps': categoria,
                'comentario': comentario,
                'canal_encuesta': random.choice(['Email', 'SMS', 'App', 'Web']),
                'tiempo_respuesta_dias': random.randint(0, 7),
                'contacto_previo': random.random() < 0.60,  # 60% tuvo contacto previo
                'resolucion_satisfactoria': random.random() < 0.75 if nps_score >= 7 else random.random() < 0.30,
                'recomendaria_servicio': nps_score >= 7,
                'region': random.choice(['Norte', 'Centro', 'Sur', 'Este', 'Oeste']),
                'edad_cliente': random.randint(18, 75),
                'antiguedad_meses': random.randint(1, 120)
            }
            
            nps_responses.append(nps_response)
            response_id += 1
        
        current_date += timedelta(days=1)
    
    return pd.DataFrame(nps_responses)


def export_sample_data_to_files(base_path: str = None):
    """
    Exporta todos los datos de ejemplo a archivos CSV y Excel
    
    Genera archivos organizados que pueden ser utilizados por el sistema
    para testing y demos sin conexiones reales.
    
    Args:
        base_path: Ruta base donde exportar (default: proyecto/data/samples)
    """
    if base_path is None:
        from pathlib import Path
        base_path = Path(__file__).parent.parent.parent / 'data' / 'samples'
    
    # Crear directorio si no existe
    Path(base_path).mkdir(parents=True, exist_ok=True)
    
    # Generar datos para los últimos 90 días
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print("Generando datos de ejemplo...")
    print(f"Período: {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}")
    
    # Generar datasets
    generator = SampleDataGenerator(start_date, end_date)
    
    print("1. Generando datos de tickets...")
    tickets_df = generator.generate_tickets_data()
    
    print("2. Generando datos de AVAYA...")
    avaya_df = generate_sample_avaya_data(start_date, end_date)
    
    print("3. Generando datos de NPS...")
    nps_df = generate_sample_nps_data(start_date, end_date)
    
    # Exportar a CSV
    print("4. Exportando a archivos...")
    tickets_df.to_csv(Path(base_path) / 'sample_tickets.csv', index=False)
    avaya_df.to_csv(Path(base_path) / 'sample_avaya.csv', index=False)
    nps_df.to_csv(Path(base_path) / 'sample_nps.csv', index=False)
    
    # Exportar catálogos
    asesores_df = pd.DataFrame(generator.asesores)
    asesores_df.to_csv(Path(base_path) / 'sample_asesores.csv', index=False)
    
    # Exportar a Excel consolidado
    with pd.ExcelWriter(Path(base_path) / 'sample_data_complete.xlsx') as writer:
        tickets_df.to_excel(writer, sheet_name='Tickets', index=False)
        avaya_df.to_excel(writer, sheet_name='AVAYA', index=False)
        nps_df.to_excel(writer, sheet_name='NPS', index=False)
        asesores_df.to_excel(writer, sheet_name='Asesores', index=False)
    
    # Estadísticas generadas
    print(f"\n=== DATOS GENERADOS ===")
    print(f"Tickets: {len(tickets_df):,} registros")
    print(f"Llamadas AVAYA: {len(avaya_df):,} registros")
    print(f"Respuestas NPS: {len(nps_df):,} registros")
    print(f"Asesores: {len(asesores_df)} registros")
    print(f"\nArchivos exportados en: {base_path}")
    print("- sample_tickets.csv")
    print("- sample_avaya.csv") 
    print("- sample_nps.csv")
    print("- sample_asesores.csv")
    print("- sample_data_complete.xlsx (consolidado)")


if __name__ == "__main__":
    """
    Ejecutar generación de datos de ejemplo
    """
    print("=== GENERADOR DE DATOS DE EJEMPLO ===")
    print("Sistema KPI Dashboard - Datos simulados")
    print("=" * 50)
    
    export_sample_data_to_files()
    
    print("\n✅ Generación completada exitosamente!")
    print("Los datos están listos para usar con el sistema KPI Dashboard.")