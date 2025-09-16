"""
Utilidades de configuración y logging para el proyecto KPI Dashboard

Este módulo maneja toda la configuración del sistema, incluyendo:
- Carga de archivos de configuración YAML
- Configuración del sistema de logging
- Manejo de paths del proyecto
- Variables de configuración por defecto

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16
"""

import yaml
import os
from pathlib import Path
from loguru import logger
import sys


class Config:
    """
    Clase principal para manejo de configuración del proyecto
    
    Esta clase se encarga de:
    1. Cargar configuraciones desde archivos YAML
    2. Proporcionar valores por defecto si no existe configuración
    3. Configurar el sistema de logging con archivos rotativos
    4. Proporcionar métodos para acceder a configuraciones anidadas
    
    Ejemplo de uso:
        config = Config()
        db_host = config.get('database.host')
        db_url = config.get_database_url()
    """
    
    def __init__(self, config_path=None):
        """
        Inicializar la configuración
        
        Args:
            config_path (str, optional): Ruta al archivo de configuración.
                                       Si no se proporciona, usa config/config.yaml
        """
        # Determinar ruta del archivo de configuración
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        
        self.config_path = config_path
        # Cargar configuración desde archivo o usar valores por defecto
        self.config = self._load_config()
        # Configurar sistema de logging basado en la configuración cargada
        self._setup_logging()
    
    def _load_config(self):
        """
        Cargar configuración desde archivo YAML
        
        Returns:
            dict: Diccionario con toda la configuración del sistema
            
        Maneja errores de archivo no encontrado y devuelve configuración por defecto
        """
        try:
            # Intentar abrir y cargar el archivo YAML de configuración
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Si no existe el archivo, mostrar advertencia y usar configuración por defecto
            logger.warning(f"Archivo de configuración no encontrado: {self.config_path}")
            logger.info("Usando configuración por defecto. Ejecuta setup.py para crear configuración inicial.")
            return self._default_config()
    
    def _default_config(self):
        """
        Configuración por defecto del sistema
        
        Returns:
            dict: Configuración mínima para que el sistema funcione
            
        Esta configuración se usa cuando no existe archivo config.yaml
        Permite que el sistema funcione con datos de ejemplo
        """
        return {
            # Configuración mínima de base de datos para desarrollo
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'kpi_database'
            },
            # Configuración básica del dashboard
            'dashboard': {
                'port': 8050,  # Puerto por defecto para Dash
                'debug': True  # Modo debug activado para desarrollo
            },
            # Configuración para análisis de causas
            'causas': {
                'max_categories': 15,        # Máximo de categorías simplificadas
                'similarity_threshold': 0.75  # Umbral de similitud para agrupación
            },
            # Configuración para análisis de asesores
            'asesores': {
                'target_resolution_rate': 0.75,  # Meta de 75% de resolución
                'escalation_threshold': 0.25,    # Máximo 25% de escalación
                'performance_window_days': 30    # Ventana de 30 días para análisis
            }
        }
    
    def _setup_logging(self):
        """
        Configurar sistema de logging avanzado
        
        Configura dos handlers:
        1. Console: Para ver logs en tiempo real durante desarrollo
        2. File: Para persistir logs con rotación automática
        
        Características:
        - Rotación automática por tamaño
        - Retención de archivos históricos
        - Formato colorizado para consola
        - Formato estructurado para archivos
        """
        # Obtener configuración de logging o usar valores por defecto
        log_config = self.config.get('logging', {})
        
        # Determinar ruta del archivo de log
        log_file = log_config.get('file', 'logs/kpi_dashboard.log')
        log_dir = Path(log_file).parent
        # Crear directorio de logs si no existe
        log_dir.mkdir(exist_ok=True)
        
        # Configurar logger (remover configuración por defecto de loguru)
        logger.remove()  # Limpiar handlers existentes
        
        # Handler para consola - logs colorados y legibles durante desarrollo
        logger.add(
            sys.stderr,
            level=log_config.get('level', 'INFO'),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        
        # Handler para archivo - logs estructurados para análisis posterior
        logger.add(
            log_file,
            level=log_config.get('level', 'INFO'),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation=f"{log_config.get('max_size_mb', 100)} MB",  # Rotar cuando alcance 100MB
            retention=log_config.get('backup_count', 5)           # Mantener 5 archivos históricos
        )
    
    def get(self, key_path, default=None):
        """
        Obtener valor de configuración usando notación de puntos
        
        Args:
            key_path (str): Ruta de la configuración usando puntos. Ej: 'database.host'
            default: Valor por defecto si no se encuentra la configuración
            
        Returns:
            Valor de la configuración o default si no existe
            
        Ejemplo:
            host = config.get('database.host')
            port = config.get('database.port', 5432)
        """
        # Dividir la ruta por puntos para navegar en el diccionario anidado
        keys = key_path.split('.')
        value = self.config
        
        # Navegar por cada nivel del diccionario
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                # Si no se encuentra la clave, devolver valor por defecto
                return default
        
        return value
    
    def get_database_url(self):
        """
        Construir URL de conexión a base de datos
        
        Returns:
            str: URL de conexión formateada según el driver configurado
            
        Soporta múltiples tipos de base de datos:
        - PostgreSQL: postgresql://user:pass@host:port/db
        - SQLite: sqlite:///database.db
        
        Raises:
            ValueError: Si el driver no está soportado
        """
        # Obtener configuración de base de datos
        db_config = self.config.get('database', {})
        driver = db_config.get('driver', 'postgresql')
        username = db_config.get('username', 'admin')
        password = db_config.get('password', 'password')
        host = db_config.get('host', 'localhost')
        port = db_config.get('port', 5432)
        name = db_config.get('name', 'kpi_database')
        
        # Construir URL según el tipo de driver
        if driver == 'postgresql':
            return f"postgresql://{username}:{password}@{host}:{port}/{name}"
        elif driver == 'sqlite':
            # Para SQLite, solo necesitamos el nombre del archivo
            return f"sqlite:///{name}.db"
        else:
            raise ValueError(f"Driver de base de datos no soportado: {driver}")


def setup_project_paths():
    """
    Configurar y crear paths necesarios del proyecto
    
    Returns:
        dict: Diccionario con todos los paths importantes del proyecto
        
    Crea automáticamente los directorios que no existen:
    - project_root: Directorio raíz del proyecto
    - src: Código fuente
    - data: Datos de entrada
    - output: Archivos generados y reportes
    - config: Archivos de configuración
    - logs: Archivos de logging
    """
    # Determinar directorio raíz del proyecto (3 niveles arriba desde este archivo)
    project_root = Path(__file__).parent.parent.parent
    
    # Definir todos los paths importantes del proyecto
    paths = {
        'project_root': project_root,
        'src': project_root / 'src',
        'data': project_root / 'data',
        'output': project_root / 'output',
        'config': project_root / 'config',
        'logs': project_root / 'logs'
    }
    
    # Crear directorios que no existan para evitar errores posteriores
    for path_name, path in paths.items():
        path.mkdir(exist_ok=True)
        # Solo loggear si realmente se creó el directorio
        if not path.exists():
            logger.debug(f"Directorio creado: {path_name} -> {path}")
    
    return paths


# =============================================================================
# INSTANCIAS GLOBALES - Configuración singleton para uso en toda la aplicación
# =============================================================================

# Instancia global de configuración - se carga una sola vez al importar el módulo
config = Config()

# Paths del proyecto - disponibles globalmente para todos los módulos
paths = setup_project_paths()