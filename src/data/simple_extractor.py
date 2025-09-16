"""
Extractor de datos simplificado para el Sistema KPI Dashboard

Este módulo proporciona funcionalidad básica de extracción de datos usando
solo bibliotecas estándar de Python, sin dependencias externas.

Funcionalidades:
- Carga datos de ejemplo desde archivos CSV
- Fallback automático cuando no hay conexiones reales
- Conversión básica de tipos de datos
- Manejo de errores robusto

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Carga datos desde archivo CSV y los convierte a lista de diccionarios
    
    Args:
        file_path: Ruta al archivo CSV
        
    Returns:
        List[Dict]: Lista de registros como diccionarios
    """
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convertir strings vacías a None
                converted_row = {}
                for key, value in row.items():
                    if value == '' or value == 'None':
                        converted_row[key] = None
                    elif value in ('True', 'False'):
                        converted_row[key] = value == 'True'
                    else:
                        # Intentar convertir a número
                        try:
                            if '.' in value:
                                converted_row[key] = float(value)
                            else:
                                converted_row[key] = int(value)
                        except (ValueError, TypeError):
                            converted_row[key] = value
                
                data.append(converted_row)
        
        return data
    
    except Exception as e:
        print(f"Error cargando {file_path}: {e}")
        return []


def extract_last_month_data() -> Dict[str, List[Dict]]:
    """
    FUNCIÓN PRINCIPAL DE EXTRACCIÓN
    
    Extrae datos de ejemplo de archivos CSV generados previamente.
    Esta función reemplaza las conexiones reales con datos simulados.
    
    Returns:
        Dict: Diccionario con todos los datasets
    """
    print("=== EXTRAYENDO DATOS DE EJEMPLO ===")
    
    # Ubicación de archivos de ejemplo
    samples_dir = Path(__file__).parent.parent.parent / 'data' / 'samples'
    
    if not samples_dir.exists():
        print(f"❌ Directorio de datos de ejemplo no encontrado: {samples_dir}")
        print("Ejecute primero: python create_sample_data.py")
        return {}
    
    # Extraer cada tipo de dato
    data = {}
    
    # 1. TICKETS
    tickets_file = samples_dir / 'sample_tickets.csv'
    if tickets_file.exists():
        tickets_data = load_csv_data(str(tickets_file))
        data['tickets_db'] = tickets_data
        print(f"✅ Tickets cargados: {len(tickets_data)} registros")
    else:
        print("❌ Archivo de tickets no encontrado")
        data['tickets_db'] = []
    
    # 2. AVAYA
    avaya_file = samples_dir / 'sample_avaya.csv'
    if avaya_file.exists():
        avaya_data = load_csv_data(str(avaya_file))
        data['avaya_data'] = avaya_data
        print(f"✅ Datos AVAYA cargados: {len(avaya_data)} registros")
    else:
        print("❌ Archivo AVAYA no encontrado")
        data['avaya_data'] = []
    
    # 3. NPS
    nps_file = samples_dir / 'sample_nps.csv'
    if nps_file.exists():
        nps_data = load_csv_data(str(nps_file))
        data['nps_data'] = nps_data
        print(f"✅ Datos NPS cargados: {len(nps_data)} registros")
    else:
        print("❌ Archivo NPS no encontrado")
        data['nps_data'] = []
    
    # 4. ASESORES
    asesores_file = samples_dir / 'sample_asesores.csv'
    if asesores_file.exists():
        asesores_data = load_csv_data(str(asesores_file))
        data['asesores'] = asesores_data
        print(f"✅ Asesores cargados: {len(asesores_data)} registros")
    else:
        print("❌ Archivo de asesores no encontrado")
        data['asesores'] = []
    
    # ESTADÍSTICAS FINALES
    total_records = sum(len(dataset) for dataset in data.values())
    print(f"=== EXTRACCIÓN COMPLETADA ===")
    print(f"Total de registros cargados: {total_records:,}")
    
    return data


def get_data_summary(data: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Genera resumen estadístico de los datos cargados
    
    Args:
        data: Diccionario con datasets
        
    Returns:
        Dict: Resumen estadístico
    """
    summary = {
        'total_records': sum(len(dataset) for dataset in data.values()),
        'datasets': {},
        'date_range': {},
        'extraction_time': datetime.now().isoformat()
    }
    
    for name, dataset in data.items():
        if dataset:
            summary['datasets'][name] = {
                'count': len(dataset),
                'columns': list(dataset[0].keys()) if dataset else []
            }
            
            # Detectar rango de fechas
            date_fields = [col for col in dataset[0].keys() if 'fecha' in col.lower() or 'timestamp' in col.lower()]
            if date_fields:
                dates = []
                for record in dataset:
                    for field in date_fields:
                        if record.get(field):
                            try:
                                # Intentar parsear fecha
                                date_str = str(record[field])
                                if ' ' in date_str:
                                    parsed_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                                else:
                                    parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                                dates.append(parsed_date)
                            except:
                                pass
                
                if dates:
                    summary['date_range'][name] = {
                        'start': min(dates).isoformat(),
                        'end': max(dates).isoformat(),
                        'days': (max(dates) - min(dates)).days
                    }
    
    return summary


def validate_data_quality(data: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Valida la calidad y completitud de los datos
    
    Args:
        data: Diccionario con datasets
        
    Returns:
        Dict: Reporte de calidad de datos
    """
    quality_report = {
        'validation_time': datetime.now().isoformat(),
        'overall_status': 'PASS',
        'issues': [],
        'dataset_quality': {}
    }
    
    # Validaciones por dataset
    required_fields = {
        'tickets_db': ['ticket_id', 'fecha_creacion', 'producto', 'asesor_id'],
        'avaya_data': ['call_id', 'timestamp', 'operador', 'aht_minutos'],
        'nps_data': ['respuesta_id', 'fecha_respuesta', 'nps_score', 'producto'],
        'asesores': ['asesor_id', 'nombre', 'nivel_experiencia']
    }
    
    for dataset_name, dataset in data.items():
        if not dataset:
            quality_report['issues'].append(f"Dataset {dataset_name} está vacío")
            quality_report['overall_status'] = 'WARNING'
            continue
        
        dataset_quality = {
            'record_count': len(dataset),
            'required_fields_present': True,
            'data_types_valid': True,
            'missing_values': 0
        }
        
        # Verificar campos requeridos
        if dataset_name in required_fields:
            required = required_fields[dataset_name]
            first_record = dataset[0]
            
            for field in required:
                if field not in first_record:
                    dataset_quality['required_fields_present'] = False
                    quality_report['issues'].append(f"Campo requerido {field} faltante en {dataset_name}")
                    quality_report['overall_status'] = 'FAIL'
        
        # Contar valores nulos/vacíos
        for record in dataset:
            for key, value in record.items():
                if value is None or value == '':
                    dataset_quality['missing_values'] += 1
        
        quality_report['dataset_quality'][dataset_name] = dataset_quality
    
    return quality_report


def export_data_summary(data: Dict[str, List[Dict]], output_path: str = None):
    """
    Exporta resumen de datos a archivo JSON
    
    Args:
        data: Diccionario con datasets
        output_path: Ruta de salida (opcional)
    """
    if output_path is None:
        output_path = Path(__file__).parent.parent.parent / 'data' / 'data_summary.json'
    
    summary = get_data_summary(data)
    quality = validate_data_quality(data)
    
    export_data = {
        'summary': summary,
        'quality_report': quality,
        'export_timestamp': datetime.now().isoformat()
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Resumen de datos exportado a: {output_path}")
        
    except Exception as e:
        print(f"❌ Error exportando resumen: {e}")


if __name__ == "__main__":
    """
    Ejecutar extracción de datos de ejemplo y generar resumen
    """
    print("=== EXTRACTOR DE DATOS SIMPLIFICADO ===")
    print("Sistema KPI Dashboard")
    print("=" * 50)
    
    # Extraer datos
    data = extract_last_month_data()
    
    if data:
        # Generar y mostrar resumen
        summary = get_data_summary(data)
        quality = validate_data_quality(data)
        
        print(f"\n📊 RESUMEN DE DATOS:")
        print(f"   Total de registros: {summary['total_records']:,}")
        print(f"   Datasets cargados: {len(summary['datasets'])}")
        
        for name, info in summary['datasets'].items():
            print(f"   • {name}: {info['count']:,} registros")
        
        print(f"\n✅ CALIDAD DE DATOS: {quality['overall_status']}")
        if quality['issues']:
            print("   Problemas encontrados:")
            for issue in quality['issues']:
                print(f"   ⚠️  {issue}")
        
        # Exportar resumen
        export_data_summary(data)
        
        print(f"\n🚀 DATOS LISTOS PARA USAR!")
        print(f"   Los datos pueden ser procesados por el sistema KPI Dashboard")
    
    else:
        print(f"\n❌ No se pudieron cargar datos de ejemplo")
        print(f"   Ejecute primero: python create_sample_data.py")