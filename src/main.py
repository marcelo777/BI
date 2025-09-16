"""
Sistema principal del Dashboard KPI - Punto de entrada unificado

DESCRIPCIÓN GENERAL:
Este es el módulo principal que orquesta todas las funcionalidades del sistema
KPI Dashboard. Proporciona una interfaz de línea de comandos unificada para
ejecutar diferentes modos de operación del sistema.

ARQUITECTURA DEL SISTEMA:
El sistema está diseñado con una arquitectura modular que permite:
1. Extracción independiente de datos de múltiples fuentes
2. Procesamiento distribuido de KPIs y métricas
3. Análisis especializados (causas, asesores)
4. Dashboard interactivo en tiempo real
5. Generación de reportes ejecutivos

MODOS DE EJECUCIÓN DISPONIBLES:

1. DASHBOARD (--mode dashboard):
   - Ejecuta el dashboard web interactivo
   - Puerto configurable (default: 8050)
   - Auto-refresh de datos
   - Visualizaciones en tiempo real
   - Filtros y drill-down interactivos

2. EXTRACT (--mode extract):
   - Solo extrae datos de fuentes configuradas
   - Útil para validar conexiones
   - Opción de exportar datos raw
   - Logs detallados del proceso

3. PROCESS (--mode process):
   - Extrae datos y calcula todos los KPIs
   - Muestra resumen ejecutivo en consola
   - Opción de exportar métricas a Excel
   - Validación de objetivos vs resultados

4. CAUSAS (--mode causas):
   - Análisis específico de simplificación de causas
   - Reduce 90+ causas a categorías manejables
   - Exporta mapeo de transformación
   - Análisis de impacto por categoría

5. ASESORES (--mode asesores):
   - Análisis detallado de rendimiento de asesores
   - Validación de hipótesis del 25% de resolución
   - Identificación de problemas de tipificación vs capacidad
   - Recomendaciones específicas por asesor

6. FULL (--mode full):
   - Ejecuta análisis completo del sistema
   - Todos los módulos de extracción, procesamiento y análisis
   - Reporte consolidado en Excel
   - Resumen ejecutivo completo

PARÁMETROS DISPONIBLES:
- --start-date: Fecha inicio análisis (YYYY-MM-DD)
- --end-date: Fecha fin análisis (YYYY-MM-DD)
- --export: Exportar resultados a Excel
- --help: Mostrar ayuda completa

EJEMPLOS DE USO:

Ejecutar dashboard interactivo:
    python src/main.py --mode dashboard

Análisis completo con exportación:
    python src/main.py --mode full --export

Análisis de periodo específico:
    python src/main.py --mode process --start-date 2025-08-01 --end-date 2025-09-15

Solo análisis de causas:
    python src/main.py --mode causas --export

CUMPLIMIENTO FECHA OBJETIVO:
Este sistema cumple con la fecha objetivo del 16/9/2025 para tener el dashboard
actualizado con todas las mejoras solicitadas:

✅ Separación bandeja VIP/Otros
✅ Visibilidad afectaciones escaladas/no escaladas  
✅ Análisis por productos y segmentos
✅ Puntualidad NOC por operador
✅ Abandono AVAYA por operador
✅ FRT y NRT por operador/segmento
✅ FCR y % reaperturas por operador/segmento
✅ MTTR por producto/segmento/asesor/área
✅ AHT por operador/producto/niveles/segmentos
✅ TOP causas por producto
✅ TOP clientes afectaciones
✅ NPS evolutivo por producto/segmento
✅ Tasa respuesta total por producto/segmento
✅ Simplificación de 90+ causas a categorías manejables
✅ Análisis de asesores y validación hipótesis 25%

LOGGING Y MONITOREO:
- Logs detallados en logs/kpi_dashboard.log
- Rotación automática de archivos de log
- Diferentes niveles de log configurables
- Monitoreo de performance y errores

MANEJO DE ERRORES:
- Validación de parámetros de entrada
- Fallback a datos de ejemplo en caso de error
- Mensajes de error informativos
- Continuación grácil en caso de fallos parciales

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16 (FECHA OBJETIVO CUMPLIDA)
Versión: 1.0
"""

import sys
from pathlib import Path
import argparse
from datetime import datetime, timedelta
import pandas as pd

# Agregar el directorio src al path para imports relativos
sys.path.append(str(Path(__file__).parent))

from dashboard.main_dashboard import run_dashboard
from data.extractors import extract_last_month_data, DataExtractor
from data.processors import process_kpi_data
from analysis.causas_analysis import analyze_causes, export_causes_analysis
from analysis.asesores_analysis import analyze_asesores_performance, validate_25_percent_hypothesis
from utils.config import config, logger, paths


def main():
    """
    Función principal del sistema - Punto de entrada único
    
    Maneja:
    1. Parsing de argumentos de línea de comandos
    2. Validación de parámetros
    3. Ejecución del modo solicitado
    4. Manejo global de errores
    5. Logging de operaciones
    
    Returns:
        int: Código de salida (0=éxito, 1=error)
    """
    # Logging inicial del arranque del sistema
    logger.info("=== INICIO SISTEMA KPI DASHBOARD ===")
    logger.info(f"Modo de ejecución detectado: Línea de comandos")
    logger.info(f"Timestamp de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuración del parser de argumentos con opciones detalladas
    # Proporciona interfaz CLI completa y profesional para todos los modos
    parser = argparse.ArgumentParser(
        description='''
Sistema KPI Dashboard - Análisis completo de customer service
============================================================

Este sistema permite analizar y visualizar KPIs críticos de atención al cliente,
incluyendo métricas de rendimiento, análisis de causas y evaluación de asesores.

MODOS DISPONIBLES:
- dashboard: Dashboard web interactivo
- extract: Solo extracción de datos  
- process: Procesamiento completo de KPIs
- causas: Análisis de simplificación de causas
- asesores: Análisis de rendimiento de asesores
- full: Análisis completo con todos los módulos

EJEMPLOS:
python src/main.py --mode dashboard
python src/main.py --mode full --export
python src/main.py --mode process --start-date 2025-08-01 --end-date 2025-09-15
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Definición de argumentos con validaciones y ayudas detalladas
    parser.add_argument(
        '--mode', 
        choices=['dashboard', 'extract', 'process', 'causas', 'asesores', 'full'], 
        default='dashboard', 
        help='''Modo de ejecución del sistema:
        dashboard: Inicia dashboard web interactivo (puerto 8050)
        extract: Solo extrae datos de fuentes configuradas
        process: Extrae y procesa todos los KPIs
        causas: Análisis de simplificación de causas
        asesores: Análisis de rendimiento de asesores
        full: Análisis completo con reporte consolidado'''
    )
    
    parser.add_argument(
        '--start-date', 
        type=str, 
        help='Fecha inicio del análisis (formato: YYYY-MM-DD). Default: 30 días atrás'
    )
    
    parser.add_argument(
        '--end-date', 
        type=str, 
        help='Fecha fin del análisis (formato: YYYY-MM-DD). Default: hoy'
    )
    
    parser.add_argument(
        '--export', 
        action='store_true', 
        help='Exportar todos los resultados a archivos Excel en carpeta exports/'
    )
    
    # Parsing y validación de argumentos
    args = parser.parse_args()
    
    # Log de configuración detectada
    logger.info(f"=== CONFIGURACIÓN DETECTADA ===")
    logger.info(f"Modo solicitado: {args.mode}")
    logger.info(f"Exportación habilitada: {args.export}")
    logger.info(f"Fecha inicio personalizada: {args.start_date or 'No (30 días atrás)'}")
    logger.info(f"Fecha fin personalizada: {args.end_date or 'No (hoy)'}")
    
    # Configuración y validación de fechas del período de análisis
    # El sistema permite análisis históricos y períodos personalizados
    if args.end_date:
        try:
            end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
            logger.info(f"Fecha fin configurada: {end_date.strftime('%Y-%m-%d')}")
        except ValueError:
            logger.error(f"Formato de fecha fin inválido: {args.end_date}. Use YYYY-MM-DD")
            return 1
    else:
        end_date = datetime.now()
        logger.info(f"Fecha fin automática: {end_date.strftime('%Y-%m-%d')}")
    
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
            logger.info(f"Fecha inicio configurada: {start_date.strftime('%Y-%m-%d')}")
            
            # Validación de coherencia temporal
            if start_date >= end_date:
                logger.error("La fecha de inicio debe ser anterior a la fecha fin")
                return 1
        except ValueError:
            logger.error(f"Formato de fecha inicio inválido: {args.start_date}. Use YYYY-MM-DD")
            return 1
    else:
        start_date = end_date - timedelta(days=30)
        logger.info(f"Fecha inicio automática: {start_date.strftime('%Y-%m-%d')} (30 días atrás)")
    
    # Validación del período de análisis
    period_days = (end_date - start_date).days
    logger.info(f"Período de análisis: {period_days} días")
    
    if period_days > 365:
        logger.warning(f"Período muy largo ({period_days} días). Puede afectar performance.")
    elif period_days < 1:
        logger.error("El período de análisis debe ser de al menos 1 día")
        return 1
    
    # EJECUCIÓN DEL MODO SOLICITADO
    # ==============================
    # Cada modo tiene su lógica específica y manejo de errores independiente
    
    try:
        logger.info(f"=== INICIANDO MODO: {args.mode.upper()} ===")
        
        if args.mode == 'dashboard':
            """
            MODO DASHBOARD: Dashboard web interactivo
            - Inicia servidor web en puerto 8050
            - Auto-refresh cada 5 minutos
            - Visualizaciones interactivas con filtros
            - Drill-down por dimensiones
            """
            logger.info("Iniciando dashboard web interactivo...")
            logger.info("El dashboard estará disponible en: http://localhost:8050")
            logger.info("Para detener el dashboard, presione Ctrl+C")
            
            # Ejecutar dashboard con configuración debug
            run_dashboard(debug=config.get('dashboard', {}).get('debug', False))
            
        elif args.mode == 'extract':
            """
            MODO EXTRACT: Solo extracción de datos
            - Conecta a todas las fuentes configuradas
            - Valida conexiones y disponibilidad
            - Extrae datos raw sin procesamiento
            - Útil para debugging y validación
            """
            logger.info("Iniciando extracción de datos...")
            logger.info(f"Período: {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}")
            
            # Instanciar extractor con configuración
            extractor = DataExtractor(config)
            
            # Extraer datos de todas las fuentes
            logger.info("Extrayendo datos de base de datos...")
            db_data = extractor.extract_db_data(start_date, end_date)
            logger.info(f"Registros DB extraídos: {len(db_data) if db_data is not None else 0}")
            
            logger.info("Extrayendo datos de AVAYA...")
            avaya_data = extractor.extract_avaya_data(start_date, end_date)
            logger.info(f"Registros AVAYA extraídos: {len(avaya_data) if avaya_data is not None else 0}")
            
            logger.info("Extrayendo datos de tickets...")
            tickets_data = extractor.extract_tickets_data(start_date, end_date)
            logger.info(f"Registros tickets extraídos: {len(tickets_data) if tickets_data is not None else 0}")
            
            logger.info("Extrayendo datos de NPS...")
            nps_data = extractor.extract_nps_data(start_date, end_date)
            logger.info(f"Registros NPS extraídos: {len(nps_data) if nps_data is not None else 0}")
            
            # Opcional: Exportar datos raw
            if args.export:
                logger.info("Exportando datos raw a Excel...")
                try:
                    import pandas as pd
                    
                    export_path = paths.exports / f'datos_raw_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.xlsx'
                    with pd.ExcelWriter(export_path) as writer:
                        if db_data is not None:
                            db_data.to_excel(writer, sheet_name='DB_Data', index=False)
                        if avaya_data is not None:
                            avaya_data.to_excel(writer, sheet_name='AVAYA_Data', index=False)
                        if tickets_data is not None:
                            tickets_data.to_excel(writer, sheet_name='Tickets_Data', index=False)
                        if nps_data is not None:
                            nps_data.to_excel(writer, sheet_name='NPS_Data', index=False)
                    
                    logger.info(f"Datos raw exportados a: {export_path}")
                except Exception as e:
                    logger.error(f"Error exportando datos raw: {e}")
            
            logger.info("Extracción completada exitosamente")
            
        elif args.mode == 'process':
            logger.info(f"Extrayendo datos del {start_date.strftime('%Y-%m-%d')} al {end_date.strftime('%Y-%m-%d')}")
            extractor = DataExtractor()
            data = extractor.extract_all_data(
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            
            if args.export:
                # Exportar datos raw
                for name, df in data.items():
                    if not df.empty:
                        export_path = paths['output'] / f"raw_data_{name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
                        df.to_excel(export_path, index=False)
                        logger.info(f"Datos exportados: {export_path}")
            
            logger.info("Extracción completada")
            
        elif args.mode == 'process':
            logger.info("Procesando datos y calculando KPIs")
            data = extract_last_month_data()
            metrics = process_kpi_data(data)
            
            if args.export:
                from data.processors import DataProcessor
                processor = DataProcessor(data)
                export_path = paths['output'] / f"kpi_metrics_{datetime.now().strftime('%Y%m%d')}.xlsx"
                processor.export_to_excel(str(export_path), metrics)
                logger.info(f"Métricas exportadas: {export_path}")
            
            # Mostrar resumen
            summary = metrics.get('summary')
            if summary:
                print(f"\n=== RESUMEN DE KPIs ===")
                print(f"Total Tickets: {summary.total_tickets:,}")
                print(f"Tickets VIP: {summary.tickets_vip:,}")
                print(f"Tasa Escalación: {summary.tasa_escalacion_general:.1f}%")
                print(f"MTTR Promedio: {summary.mttr_promedio:.1f}h")
                print(f"FCR Promedio: {summary.fcr_promedio:.1f}%")
                print(f"NPS Promedio: {summary.nps_promedio:.1f}")
            
            logger.info("Procesamiento completado")
            
        elif args.mode == 'causas':
            logger.info("Analizando y simplificando causas")
            data = extract_last_month_data()
            tickets_df = data.get('tickets_db', data.get('tickets_api', pd.DataFrame()))
            
            if not tickets_df.empty:
                simplified_causes, report = analyze_causes(tickets_df)
                
                print(f"\n=== ANÁLISIS DE CAUSAS ===")
                print(f"Causas originales: {report['resumen']['causas_originales']}")
                print(f"Categorías simplificadas: {report['resumen']['categorias_simplificadas']}")
                print(f"Reducción: {report['resumen']['reduccion_porcentaje']:.1f}%")
                
                if args.export:
                    export_path = paths['output'] / f"analisis_causas_{datetime.now().strftime('%Y%m%d')}.xlsx"
                    export_causes_analysis(simplified_causes, report, str(export_path))
                    logger.info(f"Análisis de causas exportado: {export_path}")
            else:
                logger.warning("No se encontraron datos de tickets para análisis de causas")
            
            logger.info("Análisis de causas completado")
            
        elif args.mode == 'asesores':
            logger.info("Analizando rendimiento de asesores")
            data = extract_last_month_data()
            tickets_df = data.get('tickets_db', data.get('tickets_api', pd.DataFrame()))
            asesores_df = data.get('asesores', pd.DataFrame())
            
            if not tickets_df.empty:
                asesores_analysis, patterns, recommendations = analyze_asesores_performance(
                    tickets_df, asesores_df
                )
                
                # Validar hipótesis del 25%
                validation = validate_25_percent_hypothesis(asesores_analysis)
                
                print(f"\n=== ANÁLISIS DE ASESORES ===")
                print(f"Total asesores analizados: {len(asesores_analysis)}")
                print(f"Tasa resolución promedio: {validation['porcentaje_promedio']}")
                print(f"Asesores que necesitan revisión: {len(patterns['asesores_necesitan_revision'])}")
                print(f"Hipótesis 25% confirmada: {'Sí' if validation['hipotesis_confirmada'] else 'No'}")
                print(f"Conclusión: {validation['conclusion']}")
                print(f"\nDistribución de rendimiento:")
                for categoria, datos in patterns['distribucion_rendimiento'].items():
                    print(f"  {categoria.title()}: {datos}")
                
                print(f"\nRecomendaciones principales:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"  {i}. {rec['recomendacion']}")
                
                logger.info("Análisis de asesores completado")
            else:
                logger.warning("No se encontraron datos de tickets para análisis de asesores")
            
        elif args.mode == 'full':
            logger.info("Ejecutando análisis completo")
            
            # 1. Extraer datos
            logger.info("Paso 1: Extrayendo datos")
            data = extract_last_month_data()
            
            # 2. Procesar KPIs
            logger.info("Paso 2: Procesando KPIs")
            metrics = process_kpi_data(data)
            
            # 3. Análisis de causas
            logger.info("Paso 3: Analizando causas")
            tickets_df = data.get('tickets_db', data.get('tickets_api', pd.DataFrame()))
            if not tickets_df.empty:
                simplified_causes, causas_report = analyze_causes(tickets_df)
            
            # 4. Análisis de asesores
            logger.info("Paso 4: Analizando asesores")
            asesores_df = data.get('asesores', pd.DataFrame())
            if not tickets_df.empty:
                asesores_analysis, patterns, recommendations = analyze_asesores_performance(
                    tickets_df, asesores_df
                )
                validation = validate_25_percent_hypothesis(asesores_analysis)
            
            # 5. Generar reporte consolidado
            if args.export:
                logger.info("Paso 5: Generando reporte consolidado")
                generate_consolidated_report(
                    metrics, simplified_causes, causas_report, 
                    asesores_analysis, patterns, recommendations, validation
                )
            
            # 6. Mostrar resumen ejecutivo
            print_executive_summary(metrics, causas_report, validation)
            
            logger.info("Análisis completo terminado")
            
    except Exception as e:
        logger.error(f"Error en ejecución: {e}", exc_info=True)
        return 1
    
    return 0


def generate_consolidated_report(metrics, simplified_causes, causas_report, 
                               asesores_analysis, patterns, recommendations, validation):
    """Generar reporte consolidado"""
    import pandas as pd
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    consolidated_file = paths['output'] / f"reporte_consolidado_{timestamp}.xlsx"
    
    with pd.ExcelWriter(str(consolidated_file), engine='openpyxl') as writer:
        
        # Hoja 1: Resumen Ejecutivo
        summary = metrics.get('summary')
        if summary:
            executive_data = {
                'KPI': [
                    'Total Tickets', 'Tickets VIP', 'Tickets Regulares',
                    'Tasa Escalación General (%)', 'MTTR Promedio (h)',
                    'AHT Promedio (min)', 'FCR Promedio (%)', 'NPS Promedio',
                    'Causas Originales', 'Categorías Simplificadas',
                    'Tasa Resolución Asesores (%)', 'Asesores Necesitan Revisión'
                ],
                'Valor': [
                    summary.total_tickets, summary.tickets_vip, summary.tickets_regulares,
                    summary.tasa_escalacion_general, summary.mttr_promedio,
                    summary.aht_promedio, summary.fcr_promedio, summary.nps_promedio,
                    causas_report['resumen']['causas_originales'],
                    causas_report['resumen']['categorias_simplificadas'],
                    f"{validation['tasa_resolucion_promedio']:.1%}",
                    len(patterns['asesores_necesitan_revision'])
                ],
                'Meta/Objetivo': [
                    '-', '-', '-', '< 25%', '< 4h', '< 300min', '> 75%', '> 70',
                    '-', '< 15', '> 75%', '< 10'
                ]
            }
            
            pd.DataFrame(executive_data).to_excel(writer, sheet_name='Resumen_Ejecutivo', index=False)
        
        # Hoja 2: Métricas KPI detalladas
        if 'fcr' in metrics and not metrics['fcr'].empty:
            metrics['fcr'].to_excel(writer, sheet_name='FCR_Detallado', index=False)
        
        if 'mttr' in metrics and not metrics['mttr'].empty:
            metrics['mttr'].to_excel(writer, sheet_name='MTTR_Detallado', index=False)
        
        # Hoja 3: Top causas simplificadas
        top_causas_data = []
        for causa_name, causa_obj in simplified_causes.items():
            top_causas_data.append({
                'Categoria': causa_name,
                'Frecuencia': causa_obj.frecuencia,
                'Impacto': causa_obj.impacto,
                'Descripcion': causa_obj.descripcion
            })
        
        if top_causas_data:
            pd.DataFrame(top_causas_data).to_excel(writer, sheet_name='Causas_Simplificadas', index=False)
        
        # Hoja 4: Recomendaciones
        pd.DataFrame(recommendations).to_excel(writer, sheet_name='Recomendaciones', index=False)
    
    logger.info(f"Reporte consolidado generado: {consolidated_file}")


def print_executive_summary(metrics, causas_report, validation):
    """Imprimir resumen ejecutivo en consola"""
    summary = metrics.get('summary')
    
    print(f"\n" + "="*60)
    print(f"           RESUMEN EJECUTIVO KPI DASHBOARD")
    print(f"           Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"="*60)
    
    if summary:
        print(f"\n📊 MÉTRICAS PRINCIPALES:")
        print(f"   • Total Tickets: {summary.total_tickets:,}")
        print(f"   • Tickets VIP: {summary.tickets_vip:,} ({summary.tickets_vip/summary.total_tickets*100:.1f}%)")
        print(f"   • Tasa Escalación: {summary.tasa_escalacion_general:.1f}% {'✅' if summary.tasa_escalacion_general < 25 else '⚠️'}")
        print(f"   • MTTR Promedio: {summary.mttr_promedio:.1f}h {'✅' if summary.mttr_promedio < 4 else '⚠️'}")
        print(f"   • FCR Promedio: {summary.fcr_promedio:.1f}% {'✅' if summary.fcr_promedio > 75 else '⚠️'}")
        print(f"   • NPS Promedio: {summary.nps_promedio:.1f} {'✅' if summary.nps_promedio > 70 else '⚠️'}")
    
    print(f"\n🔍 ANÁLISIS DE CAUSAS:")
    print(f"   • Causas originales: {causas_report['resumen']['causas_originales']}")
    print(f"   • Categorías simplificadas: {causas_report['resumen']['categorias_simplificadas']}")
    print(f"   • Reducción lograda: {causas_report['resumen']['reduccion_porcentaje']:.1f}%")
    
    print(f"\n👥 ANÁLISIS DE ASESORES:")
    print(f"   • Tasa resolución promedio: {validation['porcentaje_promedio']}")
    print(f"   • Hipótesis 25% confirmada: {'Sí ✅' if validation['hipotesis_confirmada'] else 'No ⚠️'}")
    print(f"   • Conclusión: {validation['conclusion']}")
    
    print(f"\n🎯 ACCIONES PRIORITARIAS:")
    print(f"   1. {validation['recomendacion_principal']}")
    if summary and summary.tasa_escalacion_general > 25:
        print(f"   2. Reducir tasa de escalación del {summary.tasa_escalacion_general:.1f}% al 25%")
    if summary and summary.fcr_promedio < 75:
        print(f"   3. Mejorar FCR del {summary.fcr_promedio:.1f}% al 75%+")
    
    print(f"\n📅 OBJETIVO FECHA: 16/9/2025 - Dashboard actualizado")
    print(f"="*60)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)