"""
Modelos de datos para el sistema KPI Dashboard
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class TipoSegmento(Enum):
    """Tipos de segmento de cliente"""
    VIP = "VIP"
    REGULAR = "Regular"
    PREMIUM = "Premium"
    CORPORATE = "Corporate"
    ENTERPRISE = "Enterprise"
    STANDARD = "Standard"
    BASIC = "Basic"


class EstadoTicket(Enum):
    """Estados posibles de un ticket"""
    ABIERTO = "Abierto"
    EN_PROGRESO = "En Progreso"
    ESCALADO = "Escalado"
    RESUELTO = "Resuelto"
    CERRADO = "Cerrado"
    REAPERTURADO = "Reaperturado"


class TipoProducto(Enum):
    """Tipos de productos"""
    INTERNET = "Internet"
    TELEFONIA = "Telefonia"
    TV = "TV"
    PAQUETES = "Paquetes"
    EMPRESARIAL = "Empresarial"


@dataclass
class Ticket:
    """Modelo de datos para tickets"""
    ticket_id: str
    operador: str
    producto: TipoProducto
    segmento: TipoSegmento
    fecha_creacion: datetime
    fecha_resolucion: Optional[datetime]
    estado: EstadoTicket
    causa: str
    area_escalada: Optional[str]
    es_vip: bool
    es_reaperturado: bool
    tiempo_resolucion_minutos: Optional[int]
    cliente_id: str
    descripcion: str
    prioridad: str
    
    @property
    def es_escalado(self) -> bool:
        """Determinar si el ticket fue escalado"""
        return self.area_escalada is not None
    
    @property
    def tiempo_resolucion_horas(self) -> Optional[float]:
        """Tiempo de resolución en horas"""
        if self.tiempo_resolucion_minutos:
            return self.tiempo_resolucion_minutos / 60
        return None
    
    @property
    def esta_resuelto(self) -> bool:
        """Verificar si el ticket está resuelto"""
        return self.estado in [EstadoTicket.RESUELTO, EstadoTicket.CERRADO]


@dataclass
class Asesor:
    """Modelo de datos para asesores"""
    asesor_id: str
    nombre: str
    area: str
    nivel: int
    activo: bool
    fecha_ingreso: datetime
    especialidades: List[str]
    
    def __post_init__(self):
        if not self.especialidades:
            self.especialidades = []


@dataclass
class MetricaAbandonoAVAYA:
    """Métrica de abandono de AVAYA"""
    operador: str
    fecha: datetime
    llamadas_recibidas: int
    llamadas_abandonadas: int
    tasa_abandono: float
    tiempo_promedio_abandono: float
    
    @property
    def porcentaje_abandono(self) -> float:
        """Porcentaje de abandono"""
        return self.tasa_abandono * 100


@dataclass
class MetricaAHT:
    """Métrica de Average Handle Time"""
    operador: str
    producto: TipoProducto
    segmento: TipoSegmento
    fecha: datetime
    tiempo_promedio_manejo: float  # en minutos
    numero_llamadas: int
    tiempo_total_conversacion: float
    tiempo_total_hold: float
    tiempo_total_after_call: float
    
    @property
    def aht_horas(self) -> float:
        """AHT en horas"""
        return self.tiempo_promedio_manejo / 60


@dataclass
class MetricaNPS:
    """Métrica de Net Promoter Score"""
    fecha: datetime
    producto: TipoProducto
    segmento: TipoSegmento
    operador: Optional[str]
    promotores: int
    neutros: int
    detractores: int
    total_respuestas: int
    
    @property
    def nps_score(self) -> float:
        """Calcular NPS score"""
        if self.total_respuestas == 0:
            return 0
        
        porcentaje_promotores = (self.promotores / self.total_respuestas) * 100
        porcentaje_detractores = (self.detractores / self.total_respuestas) * 100
        
        return porcentaje_promotores - porcentaje_detractores
    
    @property
    def tasa_respuesta(self) -> float:
        """Tasa de respuesta de la encuesta"""
        # Esto requeriría el total de encuestas enviadas, 
        # asumimos que se calcula externamente
        return 0.0


@dataclass
class MetricaFCR:
    """Métrica de First Call Resolution"""
    operador: str
    segmento: TipoSegmento
    producto: TipoProducto
    fecha: datetime
    casos_resueltos_primera_llamada: int
    total_casos: int
    casos_reaperturados: int
    
    @property
    def fcr_rate(self) -> float:
        """Tasa de FCR"""
        if self.total_casos == 0:
            return 0
        return (self.casos_resueltos_primera_llamada / self.total_casos) * 100
    
    @property
    def tasa_reapertura(self) -> float:
        """Tasa de reapertura"""
        if self.total_casos == 0:
            return 0
        return (self.casos_reaperturados / self.total_casos) * 100


@dataclass
class MetricaMTTR:
    """Métrica de Mean Time to Resolution"""
    producto: TipoProducto
    segmento: TipoSegmento
    asesor: str
    area_escalada: Optional[str]
    fecha: datetime
    tiempo_promedio_resolucion: float  # en horas
    numero_tickets: int
    tiempo_total_resolucion: float
    
    @property
    def mttr_dias(self) -> float:
        """MTTR en días"""
        return self.tiempo_promedio_resolucion / 24


@dataclass
class MetricaFRT:
    """Métrica de First Response Time"""
    operador: str
    segmento: TipoSegmento
    fecha: datetime
    tiempo_promedio_primera_respuesta: float  # en minutos
    numero_tickets: int
    
    @property
    def frt_horas(self) -> float:
        """FRT en horas"""
        return self.tiempo_promedio_primera_respuesta / 60


@dataclass
class MetricaNRT:
    """Métrica de Next Response Time"""
    operador: str
    segmento: TipoSegmento
    fecha: datetime
    tiempo_promedio_siguiente_respuesta: float  # en minutos
    numero_respuestas: int
    
    @property
    def nrt_horas(self) -> float:
        """NRT en horas"""
        return self.tiempo_promedio_siguiente_respuesta / 60


@dataclass
class CausaSimplificada:
    """Modelo para causas simplificadas"""
    categoria_original: str
    categoria_simplificada: str
    descripcion: str
    frecuencia: int
    impacto: str  # Alto, Medio, Bajo
    
    def __post_init__(self):
        if self.impacto not in ["Alto", "Medio", "Bajo"]:
            self.impacto = "Medio"


@dataclass
class AnalisisAsesor:
    """Análisis de rendimiento de asesor"""
    asesor_id: str
    nombre: str
    periodo_inicio: datetime
    periodo_fin: datetime
    total_casos: int
    casos_resueltos: int
    casos_escalados: int
    tiempo_promedio_resolucion: float
    tasa_resolucion: float
    tasa_escalacion: float
    aht_promedio: float
    fcr_rate: float
    nps_promedio: float
    
    @property
    def necesita_revision(self) -> bool:
        """Determinar si el asesor necesita revisión"""
        # Criterios configurables desde config
        return (
            self.tasa_resolucion < 0.75 or  # Menos del 75% de resolución
            self.tasa_escalacion > 0.25 or  # Más del 25% de escalación
            self.fcr_rate < 0.60  # Menos del 60% de FCR
        )
    
    @property
    def categoria_rendimiento(self) -> str:
        """Categorizar rendimiento del asesor"""
        if self.tasa_resolucion >= 0.85 and self.fcr_rate >= 0.75:
            return "Excelente"
        elif self.tasa_resolucion >= 0.75 and self.fcr_rate >= 0.60:
            return "Bueno"
        elif self.tasa_resolucion >= 0.60:
            return "Regular"
        else:
            return "Necesita Mejora"


@dataclass
class KPIResumen:
    """Resumen de KPIs principales"""
    fecha_actualizacion: datetime
    periodo_inicio: datetime
    periodo_fin: datetime
    
    # Métricas principales
    total_tickets: int
    tickets_vip: int
    tickets_regulares: int
    tasa_escalacion_general: float
    mttr_promedio: float
    aht_promedio: float
    fcr_promedio: float
    nps_promedio: float
    tasa_abandono_avaya: float
    tasa_respuesta_encuestas: float
    
    # Top insights
    top_causas: List[Dict[str, Any]]
    top_clientes_afectados: List[Dict[str, Any]]
    asesores_necesitan_revision: List[str]
    productos_mayor_escalacion: List[str]