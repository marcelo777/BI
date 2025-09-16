#!/usr/bin/env python3
"""
Sistema KPI Dashboard - Versión simplificada con datos de ejemplo

Este script permite ejecutar el sistema completo usando solo bibliotecas
estándar de Python y datos de ejemplo generados previamente.

Funcionalidades disponibles:
- extract: Extracción de datos de ejemplo
- process: Procesamiento básico de KPIs
- causas: Análisis básico de causas
- asesores: Análisis básico de asesores
- summary: Resumen ejecutivo completo

Uso:
    python run_system.py extract
    python run_system.py process
    python run_system.py causas
    python run_system.py asesores
    python run_system.py summary

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Agregar src al path
sys.path.append(str(Path(__file__).parent / 'src'))

try:
    from data.simple_extractor import extract_last_month_data, get_data_summary, validate_data_quality
except ImportError:
    print("❌ Error: No se pudo importar el extractor simplificado")
    print("Asegúrese de que existe: src/data/simple_extractor.py")
    sys.exit(1)


def calculate_basic_kpis(data: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Calcula KPIs básicos desde los datos de ejemplo
    
    Args:
        data: Diccionario con datasets
        
    Returns:
        Dict: KPIs calculados
    """
    print("📊 Calculando KPIs básicos...")
    
    kpis = {
        'timestamp': datetime.now().isoformat(),
        'period_days': 30,
        'tickets': {},
        'avaya': {},
        'nps': {},
        'asesores': {}
    }
    
    # === KPIs DE TICKETS ===
    tickets = data.get('tickets_db', [])
    if tickets:
        # FCR (First Call Resolution)
        fcr_count = sum(1 for t in tickets if t.get('resuelto_primera_instancia'))
        kpis['tickets']['fcr_rate'] = round(fcr_count / len(tickets) * 100, 2)
        
        # MTTR (Mean Time To Resolution)
        mttr_values = [t.get('mttr_horas', 0) for t in tickets if t.get('mttr_horas')]
        kpis['tickets']['mttr_promedio'] = round(sum(mttr_values) / len(mttr_values), 2) if mttr_values else 0
        
        # Escalaciones
        escalaciones = sum(1 for t in tickets if t.get('escalado'))
        kpis['tickets']['tasa_escalacion'] = round(escalaciones / len(tickets) * 100, 2)
        
        # Reaperturas
        reaperturas = sum(1 for t in tickets if t.get('reabierto'))
        kpis['tickets']['tasa_reapertura'] = round(reaperturas / len(tickets) * 100, 2)
        
        # Distribución por segmento
        segmentos = {}
        for ticket in tickets:
            segmento = ticket.get('segmento_cliente', 'Unknown')
            segmentos[segmento] = segmentos.get(segmento, 0) + 1
        
        kpis['tickets']['por_segmento'] = {
            segmento: {
                'cantidad': cantidad,
                'porcentaje': round(cantidad / len(tickets) * 100, 2)
            }
            for segmento, cantidad in segmentos.items()
        }
        
        print(f"   ✅ Tickets analizados: {len(tickets)}")
        print(f"      FCR: {kpis['tickets']['fcr_rate']}%")
        print(f"      MTTR: {kpis['tickets']['mttr_promedio']} horas")
        print(f"      Escalación: {kpis['tickets']['tasa_escalacion']}%")
    
    # === KPIs DE AVAYA ===
    avaya = data.get('avaya_data', [])
    if avaya:
        # AHT (Average Handle Time)
        aht_values = [call.get('aht_minutos', 0) for call in avaya if call.get('aht_minutos')]
        kpis['avaya']['aht_promedio'] = round(sum(aht_values) / len(aht_values), 2) if aht_values else 0
        
        # Abandono
        abandonos = sum(1 for call in avaya if call.get('abandonada'))
        kpis['avaya']['tasa_abandono'] = round(abandonos / len(avaya) * 100, 2)
        
        # Distribución por operador
        operadores = {}
        for call in avaya:
            operador = call.get('operador', 'Unknown')
            operadores[operador] = operadores.get(operador, 0) + 1
        
        kpis['avaya']['por_operador'] = {
            operador: {
                'llamadas': cantidad,
                'porcentaje': round(cantidad / len(avaya) * 100, 2)
            }
            for operador, cantidad in operadores.items()
        }
        
        print(f"   ✅ Llamadas analizadas: {len(avaya)}")
        print(f"      AHT: {kpis['avaya']['aht_promedio']} min")
        print(f"      Abandono: {kpis['avaya']['tasa_abandono']}%")
    
    # === KPIs DE NPS ===
    nps = data.get('nps_data', [])
    if nps:
        # NPS Score promedio
        nps_scores = [resp.get('nps_score', 0) for resp in nps if resp.get('nps_score') is not None]
        kpis['nps']['score_promedio'] = round(sum(nps_scores) / len(nps_scores), 2) if nps_scores else 0
        
        # Distribución por categoría
        categorias = {}
        for resp in nps:
            categoria = resp.get('categoria_nps', 'Unknown')
            categorias[categoria] = categorias.get(categoria, 0) + 1
        
        kpis['nps']['por_categoria'] = {
            categoria: {
                'cantidad': cantidad,
                'porcentaje': round(cantidad / len(nps) * 100, 2)
            }
            for categoria, cantidad in categorias.items()
        }
        
        # NPS real (% Promotores - % Detractores)
        promotores = categorias.get('Promotor', 0)
        detractores = categorias.get('Detractor', 0)
        nps_real = round((promotores - detractores) / len(nps) * 100, 2)
        kpis['nps']['nps_real'] = nps_real
        
        print(f"   ✅ Encuestas analizadas: {len(nps)}")
        print(f"      Score promedio: {kpis['nps']['score_promedio']}")
        print(f"      NPS real: {nps_real}%")
    
    return kpis


def analyze_causes(data: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Análisis básico de causas
    
    Args:
        data: Diccionario con datasets
        
    Returns:
        Dict: Análisis de causas
    """
    print("🔍 Analizando causas...")
    
    tickets = data.get('tickets_db', [])
    if not tickets:
        return {}
    
    # Contar causas originales
    causas_count = {}
    for ticket in tickets:
        causa = ticket.get('causa_original', 'Unknown')
        causas_count[causa] = causas_count.get(causa, 0) + 1
    
    # Ordenar por frecuencia
    causas_ordenadas = sorted(causas_count.items(), key=lambda x: x[1], reverse=True)
    
    # TOP 10 causas
    top_causas = causas_ordenadas[:10]
    
    # Simplificación básica por palabras clave
    categorias_simplificadas = {
        'Técnicas': ['señal', 'lentitud', 'corte', 'falla', 'error', 'wifi', 'router'],
        'Comerciales': ['consulta', 'plan', 'cambio', 'promoción', 'duda', 'facturación'],
        'Administrativas': ['actualización', 'datos', 'email', 'certificado', 'solicitud']
    }
    
    simplificadas = {'Técnicas': 0, 'Comerciales': 0, 'Administrativas': 0, 'Otras': 0}
    
    for causa, count in causas_count.items():
        categorizada = False
        causa_lower = causa.lower()
        
        for categoria, palabras_clave in categorias_simplificadas.items():
            if any(palabra in causa_lower for palabra in palabras_clave):
                simplificadas[categoria] += count
                categorizada = True
                break
        
        if not categorizada:
            simplificadas['Otras'] += count
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'causas_originales': len(causas_count),
        'top_10_causas': [
            {'causa': causa, 'cantidad': count, 'porcentaje': round(count/len(tickets)*100, 2)}
            for causa, count in top_causas
        ],
        'categorias_simplificadas': {
            categoria: {
                'cantidad': cantidad,
                'porcentaje': round(cantidad/len(tickets)*100, 2)
            }
            for categoria, cantidad in simplificadas.items()
        },
        'reduccion_categorias': f"{len(causas_count)} → 4 categorías ({round((1-4/len(causas_count))*100, 1)}% reducción)"
    }
    
    print(f"   ✅ Causas originales: {len(causas_count)}")
    print(f"   ✅ Categorías simplificadas: 4")
    print(f"   ✅ Reducción: {round((1-4/len(causas_count))*100, 1)}%")
    
    return analysis


def analyze_advisors(data: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Análisis básico de asesores
    
    Args:
        data: Diccionario con datasets
        
    Returns:
        Dict: Análisis de asesores
    """
    print("👥 Analizando rendimiento de asesores...")
    
    tickets = data.get('tickets_db', [])
    asesores = data.get('asesores', [])
    
    if not tickets:
        return {}
    
    # Análisis de rendimiento por asesor
    asesor_stats = {}
    
    for ticket in tickets:
        asesor_id = ticket.get('asesor_id')
        if not asesor_id:
            continue
        
        if asesor_id not in asesor_stats:
            asesor_stats[asesor_id] = {
                'total_tickets': 0,
                'fcr_count': 0,
                'mttr_total': 0,
                'escalaciones': 0
            }
        
        stats = asesor_stats[asesor_id]
        stats['total_tickets'] += 1
        
        if ticket.get('resuelto_primera_instancia'):
            stats['fcr_count'] += 1
        
        if ticket.get('mttr_horas'):
            stats['mttr_total'] += ticket['mttr_horas']
        
        if ticket.get('escalado'):
            stats['escalaciones'] += 1
    
    # Calcular métricas finales
    asesor_analysis = []
    fcr_rates = []
    
    for asesor_id, stats in asesor_stats.items():
        if stats['total_tickets'] > 0:
            fcr_rate = stats['fcr_count'] / stats['total_tickets']
            mttr_promedio = stats['mttr_total'] / stats['total_tickets']
            tasa_escalacion = stats['escalaciones'] / stats['total_tickets']
            
            asesor_analysis.append({
                'asesor_id': asesor_id,
                'total_tickets': stats['total_tickets'],
                'fcr_rate': round(fcr_rate, 3),
                'mttr_promedio': round(mttr_promedio, 2),
                'tasa_escalacion': round(tasa_escalacion, 3)
            })
            
            fcr_rates.append(fcr_rate)
    
    # Validar hipótesis del 25%
    fcr_promedio = sum(fcr_rates) / len(fcr_rates) if fcr_rates else 0
    hipotesis_25_confirmada = fcr_promedio >= 0.25
    
    # Categorización de rendimiento
    alto_rendimiento = sum(1 for rate in fcr_rates if rate >= 0.30)
    rendimiento_medio = sum(1 for rate in fcr_rates if 0.20 <= rate < 0.30)
    bajo_rendimiento = sum(1 for rate in fcr_rates if rate < 0.20)
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'total_asesores': len(asesor_analysis),
        'fcr_promedio': round(fcr_promedio, 3),
        'hipotesis_25_pct': {
            'confirmada': hipotesis_25_confirmada,
            'diferencia': round((fcr_promedio - 0.25) * 100, 2)
        },
        'distribucion_rendimiento': {
            'alto_rendimiento': f"{alto_rendimiento} asesores (≥30% FCR)",
            'rendimiento_medio': f"{rendimiento_medio} asesores (20-29% FCR)",
            'bajo_rendimiento': f"{bajo_rendimiento} asesores (<20% FCR)"
        },
        'top_5_asesores': sorted(asesor_analysis, key=lambda x: x['fcr_rate'], reverse=True)[:5],
        'asesores_necesitan_atencion': [a for a in asesor_analysis if a['fcr_rate'] < 0.15]
    }
    
    print(f"   ✅ Asesores analizados: {len(asesor_analysis)}")
    print(f"   ✅ FCR promedio: {round(fcr_promedio*100, 1)}%")
    print(f"   ✅ Hipótesis 25% confirmada: {'Sí' if hipotesis_25_confirmada else 'No'}")
    
    return analysis


def generate_executive_summary(data: Dict[str, List[Dict]], kpis: Dict[str, Any], 
                              causes_analysis: Dict[str, Any], advisors_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera resumen ejecutivo completo
    
    Returns:
        Dict: Resumen ejecutivo
    """
    summary = {
        'timestamp': datetime.now().isoformat(),
        'period': 'Últimos 30 días (datos simulados)',
        'data_overview': get_data_summary(data),
        'key_metrics': {
            'fcr_rate': kpis.get('tickets', {}).get('fcr_rate', 0),
            'mttr_hours': kpis.get('tickets', {}).get('mttr_promedio', 0),
            'aht_minutes': kpis.get('avaya', {}).get('aht_promedio', 0),
            'abandonment_rate': kpis.get('avaya', {}).get('tasa_abandono', 0),
            'nps_score': kpis.get('nps', {}).get('nps_real', 0),
            'escalation_rate': kpis.get('tickets', {}).get('tasa_escalacion', 0)
        },
        'achievements': [],
        'concerns': [],
        'recommendations': []
    }
    
    # Evaluar métricas vs objetivos
    fcr_target = 25.0  # 25%
    mttr_target = 4.0  # 4 horas
    aht_target = 20.0  # 20 minutos
    abandonment_target = 10.0  # 10%
    
    metrics = summary['key_metrics']
    
    # Logros
    if metrics['fcr_rate'] >= fcr_target:
        summary['achievements'].append(f"FCR por encima del objetivo: {metrics['fcr_rate']}% vs {fcr_target}%")
    
    if metrics['mttr_hours'] <= mttr_target:
        summary['achievements'].append(f"MTTR dentro del objetivo: {metrics['mttr_hours']}h vs {mttr_target}h")
    
    if metrics['abandonment_rate'] <= abandonment_target:
        summary['achievements'].append(f"Tasa de abandono controlada: {metrics['abandonment_rate']}% vs {abandonment_target}%")
    
    # Preocupaciones
    if metrics['fcr_rate'] < fcr_target:
        summary['concerns'].append(f"FCR por debajo del objetivo: {metrics['fcr_rate']}% vs {fcr_target}%")
    
    if metrics['mttr_hours'] > mttr_target:
        summary['concerns'].append(f"MTTR por encima del objetivo: {metrics['mttr_hours']}h vs {mttr_target}h")
    
    if metrics['abandonment_rate'] > abandonment_target:
        summary['concerns'].append(f"Alta tasa de abandono: {metrics['abandonment_rate']}% vs {abandonment_target}%")
    
    # Recomendaciones
    if causes_analysis:
        summary['recommendations'].append("Implementar simplificación de causas para mejorar eficiencia")
    
    if advisors_analysis and not advisors_analysis.get('hipotesis_25_pct', {}).get('confirmada'):
        summary['recommendations'].append("Reforzar capacitación de asesores para mejorar FCR")
    
    summary['recommendations'].extend([
        "Continuar monitoreo de KPIs críticos",
        "Implementar dashboard automático para seguimiento",
        "Realizar análisis mensual de tendencias"
    ])
    
    return summary


def main():
    """Función principal del sistema simplificado"""
    
    if len(sys.argv) < 2:
        print("Uso: python run_system.py [extract|process|causas|asesores|summary]")
        return 1
    
    mode = sys.argv[1].lower()
    
    print("=== SISTEMA KPI DASHBOARD (VERSIÓN SIMPLIFICADA) ===")
    print("Usando datos de ejemplo simulados")
    print("=" * 60)
    
    # Verificar que existen los datos de ejemplo
    samples_dir = Path(__file__).parent / 'data' / 'samples'
    if not samples_dir.exists():
        print("❌ Datos de ejemplo no encontrados")
        print("Ejecute primero: python create_sample_data.py")
        return 1
    
    if mode == 'extract':
        # Solo extracción
        data = extract_last_month_data()
        if data:
            summary = get_data_summary(data)
            quality = validate_data_quality(data)
            print(f"\n✅ Extracción completada - {summary['total_records']:,} registros")
            print(f"   Calidad: {quality['overall_status']}")
    
    elif mode == 'process':
        # Extracción + procesamiento de KPIs
        data = extract_last_month_data()
        if data:
            kpis = calculate_basic_kpis(data)
            
            print(f"\n📊 === RESUMEN DE KPIs ===")
            if 'tickets' in kpis:
                t = kpis['tickets']
                print(f"🎫 TICKETS:")
                print(f"   FCR: {t.get('fcr_rate', 0)}%")
                print(f"   MTTR: {t.get('mttr_promedio', 0)} horas")
                print(f"   Escalación: {t.get('tasa_escalacion', 0)}%")
            
            if 'avaya' in kpis:
                a = kpis['avaya']
                print(f"☎️  AVAYA:")
                print(f"   AHT: {a.get('aht_promedio', 0)} min")
                print(f"   Abandono: {a.get('tasa_abandono', 0)}%")
            
            if 'nps' in kpis:
                n = kpis['nps']
                print(f"⭐ NPS:")
                print(f"   Score: {n.get('score_promedio', 0)}")
                print(f"   NPS Real: {n.get('nps_real', 0)}%")
    
    elif mode == 'causas':
        # Análisis de causas
        data = extract_last_month_data()
        if data:
            causes_analysis = analyze_causes(data)
            
            if causes_analysis:
                print(f"\n🔍 === ANÁLISIS DE CAUSAS ===")
                print(f"Causas originales: {causes_analysis['causas_originales']}")
                print(f"Reducción: {causes_analysis['reduccion_categorias']}")
                
                print(f"\nTOP 5 CAUSAS:")
                for causa_info in causes_analysis['top_10_causas'][:5]:
                    print(f"   • {causa_info['causa']}: {causa_info['cantidad']} ({causa_info['porcentaje']}%)")
    
    elif mode == 'asesores':
        # Análisis de asesores
        data = extract_last_month_data()
        if data:
            advisors_analysis = analyze_advisors(data)
            
            if advisors_analysis:
                print(f"\n👥 === ANÁLISIS DE ASESORES ===")
                print(f"Asesores analizados: {advisors_analysis['total_asesores']}")
                print(f"FCR promedio: {round(advisors_analysis['fcr_promedio']*100, 1)}%")
                
                hip = advisors_analysis['hipotesis_25_pct']
                print(f"Hipótesis 25% FCR: {'✅ CONFIRMADA' if hip['confirmada'] else '❌ NO CONFIRMADA'}")
                
                print(f"\nTOP 3 ASESORES:")
                for asesor in advisors_analysis['top_5_asesores'][:3]:
                    print(f"   • {asesor['asesor_id']}: {round(asesor['fcr_rate']*100, 1)}% FCR")
    
    elif mode == 'summary':
        # Resumen ejecutivo completo
        print("Generando resumen ejecutivo completo...")
        
        data = extract_last_month_data()
        if data:
            kpis = calculate_basic_kpis(data)
            causes_analysis = analyze_causes(data)
            advisors_analysis = analyze_advisors(data)
            
            executive_summary = generate_executive_summary(data, kpis, causes_analysis, advisors_analysis)
            
            # Mostrar resumen
            print(f"\n📋 === RESUMEN EJECUTIVO ===")
            print(f"Período: {executive_summary['period']}")
            
            print(f"\n📊 MÉTRICAS CLAVE:")
            metrics = executive_summary['key_metrics']
            print(f"   FCR: {metrics['fcr_rate']}%")
            print(f"   MTTR: {metrics['mttr_hours']} horas")
            print(f"   AHT: {metrics['aht_minutes']} minutos")
            print(f"   Abandono: {metrics['abandonment_rate']}%")
            print(f"   NPS: {metrics['nps_score']}%")
            print(f"   Escalación: {metrics['escalation_rate']}%")
            
            if executive_summary['achievements']:
                print(f"\n✅ LOGROS:")
                for achievement in executive_summary['achievements']:
                    print(f"   • {achievement}")
            
            if executive_summary['concerns']:
                print(f"\n⚠️  PREOCUPACIONES:")
                for concern in executive_summary['concerns']:
                    print(f"   • {concern}")
            
            print(f"\n💡 RECOMENDACIONES:")
            for recommendation in executive_summary['recommendations']:
                print(f"   • {recommendation}")
            
            # Exportar a JSON
            output_file = Path(__file__).parent / 'exports' / f'resumen_ejecutivo_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
            output_file.parent.mkdir(exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(executive_summary, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Resumen exportado: {output_file}")
    
    else:
        print(f"❌ Modo '{mode}' no reconocido")
        print("Modos disponibles: extract, process, causas, asesores, summary")
        return 1
    
    print(f"\n✅ Ejecución completada exitosamente!")
    return 0


if __name__ == "__main__":
    exit(main())