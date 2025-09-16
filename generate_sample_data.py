#!/usr/bin/env python3
"""
Script para generar datos de ejemplo para el Sistema KPI Dashboard

PROPÓSITO:
Este script ejecuta la generación de todos los datos de ejemplo necesarios
para que el sistema funcione completamente sin conexiones reales.

CASOS DE USO:
- Desarrollo y testing del sistema
- Demos y presentaciones
- Training de nuevos usuarios
- Validación de funcionalidades

EJECUCIÓN:
python generate_sample_data.py

Autor: Sistema KPI Dashboard
Fecha: 2025-09-16
"""

import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.append(str(Path(__file__).parent / 'src'))

try:
    from data.sample_data_generator import export_sample_data_to_files
    print("Módulo generador importado exitosamente")
except ImportError as e:
    print(f"Error importando módulo: {e}")
    print("Creando generador básico...")
    
    import pandas as pd
    import numpy as np
    import random
    from datetime import datetime, timedelta
    
    def create_basic_sample_data():
        """Genera datos básicos de ejemplo"""
        
        # Crear directorio samples
        samples_dir = Path(__file__).parent / 'data' / 'samples'
        samples_dir.mkdir(parents=True, exist_ok=True)
        
        print("Generando datos básicos de ejemplo...")
        
        # 1. TICKETS
        print("1. Generando tickets...")
        tickets = []
        for i in range(500):
            fecha_base = datetime.now() - timedelta(days=random.randint(1, 90))
            
            ticket = {
                'ticket_id': f'TKT_{i+1:06d}',
                'fecha_creacion': fecha_base,
                'fecha_resolucion': fecha_base + timedelta(hours=random.randint(1, 48)),
                'producto': random.choice(['Internet Hogar', 'TV Cable', 'Telefonía Fija', 'Móvil Postpago', 'Móvil Prepago']),
                'segmento_cliente': random.choice(['VIP', 'Premium', 'Regular', 'Básico']),
                'asesor_id': f'ASE_{random.randint(1, 50):03d}',
                'asesor_nombre': f'Asesor_{random.randint(1, 50):03d}',
                'asesor_nivel': random.choice(['Junior', 'Semi-Senior', 'Senior']),
                'causa_original': random.choice([
                    'Sin señal TV', 'Lentitud navegación', 'Corte intermitente', 'Consulta plan', 
                    'Cambio plan', 'Reclamo facturación', 'Soporte técnico', 'Actualización datos'
                ]),
                'escalado': random.choice([True, False]),
                'resuelto_primera_instancia': random.choice([True, False]),
                'reabierto': random.choice([True, False]),
                'mttr_horas': round(random.uniform(0.5, 24.0), 2),
                'satisfaccion_cliente': random.randint(1, 10),
                'cliente_id': f'CLI_{random.randint(1, 10000):05d}',
                'canal_entrada': random.choice(['Web', 'Telefono', 'App', 'Presencial']),
                'prioridad': random.choice(['Alta', 'Media', 'Baja']),
                'complejidad': random.choice(['Alta', 'Media', 'Baja'])
            }
            tickets.append(ticket)
        
        tickets_df = pd.DataFrame(tickets)
        tickets_df.to_csv(samples_dir / 'sample_tickets.csv', index=False)
        print(f"   ✅ {len(tickets_df)} tickets generados")
        
        # 2. AVAYA
        print("2. Generando datos AVAYA...")
        calls = []
        for i in range(1000):
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 2160))  # 90 días
            
            call = {
                'call_id': f'CALL_{i+1:08d}',
                'timestamp': timestamp,
                'operador': random.choice(['Operador_A', 'Operador_B', 'Operador_C', 'Operador_D']),
                'cola': random.choice(['Cola_Tecnica', 'Cola_Comercial', 'Cola_Retencion', 'Cola_Soporte']),
                'tiempo_cola_segundos': random.randint(10, 300),
                'aht_minutos': round(random.uniform(5, 35), 2),
                'abandonada': random.choice([True, False]),
                'transferida': random.choice([True, False]),
                'producto_consultado': random.choice(['Internet Hogar', 'TV Cable', 'Móvil Postpago', 'General']),
                'tipo_llamada': random.choice(['Consulta', 'Reclamo', 'Soporte_Tecnico', 'Comercial']),
                'satisfaccion_llamada': random.randint(1, 10),
                'cliente_id': f'CLI_{random.randint(1, 10000):05d}',
                'duracion_total_segundos': random.randint(60, 2100)
            }
            calls.append(call)
        
        avaya_df = pd.DataFrame(calls)
        avaya_df.to_csv(samples_dir / 'sample_avaya.csv', index=False)
        print(f"   ✅ {len(avaya_df)} llamadas generadas")
        
        # 3. NPS
        print("3. Generando datos NPS...")
        nps_responses = []
        for i in range(200):
            fecha = datetime.now() - timedelta(days=random.randint(1, 90))
            nps_score = random.randint(0, 10)
            
            if nps_score <= 6:
                categoria = 'Detractor'
                comentario = 'Servicio deficiente, muchos problemas'
            elif nps_score <= 8:
                categoria = 'Neutral'
                comentario = 'Servicio regular, puede mejorar'
            else:
                categoria = 'Promotor'
                comentario = 'Excelente servicio, muy satisfecho'
            
            nps = {
                'respuesta_id': f'NPS_{i+1:06d}',
                'fecha_respuesta': fecha,
                'cliente_id': f'CLI_{random.randint(1, 10000):05d}',
                'producto': random.choice(['Internet Hogar', 'TV Cable', 'Móvil Postpago', 'Telefonía Fija']),
                'segmento_cliente': random.choice(['VIP', 'Premium', 'Regular', 'Básico']),
                'nps_score': nps_score,
                'categoria_nps': categoria,
                'comentario': comentario,
                'canal_encuesta': random.choice(['Email', 'SMS', 'App', 'Web']),
                'recomendaria_servicio': nps_score >= 7
            }
            nps_responses.append(nps)
        
        nps_df = pd.DataFrame(nps_responses)
        nps_df.to_csv(samples_dir / 'sample_nps.csv', index=False)
        print(f"   ✅ {len(nps_df)} encuestas NPS generadas")
        
        # 4. ASESORES
        print("4. Generando catálogo de asesores...")
        asesores = []
        for i in range(50):
            nivel = random.choice(['Junior', 'Semi-Senior', 'Senior'])
            
            # FCR esperado basado en nivel
            if nivel == 'Junior':
                fcr_esperado = random.uniform(0.10, 0.20)
                aht_esperado = random.uniform(20, 30)
            elif nivel == 'Semi-Senior':
                fcr_esperado = random.uniform(0.20, 0.30)
                aht_esperado = random.uniform(15, 25)
            else:  # Senior
                fcr_esperado = random.uniform(0.30, 0.40)
                aht_esperado = random.uniform(12, 20)
            
            asesor = {
                'asesor_id': f'ASE_{i+1:03d}',
                'nombre': f'Asesor_{i+1:03d}',
                'nivel_experiencia': nivel,
                'fcr_esperado': round(fcr_esperado, 3),
                'aht_esperado': round(aht_esperado, 1),
                'area': random.choice(['Técnico', 'Comercial', 'Retención', 'Soporte']),
                'turno': random.choice(['Mañana', 'Tarde', 'Noche']),
                'fecha_ingreso': datetime.now() - timedelta(days=random.randint(30, 1095))
            }
            asesores.append(asesor)
        
        asesores_df = pd.DataFrame(asesores)
        asesores_df.to_csv(samples_dir / 'sample_asesores.csv', index=False)
        print(f"   ✅ {len(asesores_df)} asesores generados")
        
        # 5. EXCEL CONSOLIDADO
        print("5. Creando archivo Excel consolidado...")
        with pd.ExcelWriter(samples_dir / 'sample_data_complete.xlsx') as writer:
            tickets_df.to_excel(writer, sheet_name='Tickets', index=False)
            avaya_df.to_excel(writer, sheet_name='AVAYA', index=False)
            nps_df.to_excel(writer, sheet_name='NPS', index=False)
            asesores_df.to_excel(writer, sheet_name='Asesores', index=False)
        
        print("   ✅ Archivo Excel consolidado creado")
        
        return {
            'tickets': len(tickets_df),
            'avaya': len(avaya_df),
            'nps': len(nps_df),
            'asesores': len(asesores_df),
            'path': samples_dir
        }
    
    def main():
        """Función principal"""
        print("=== GENERADOR DE DATOS DE EJEMPLO ===")
        print("Sistema KPI Dashboard")
        print("=" * 50)
        
        try:
            stats = create_basic_sample_data()
            
            print(f"\n✅ GENERACIÓN COMPLETADA EXITOSAMENTE!")
            print(f"📁 Ubicación: {stats['path']}")
            print(f"\n📊 ESTADÍSTICAS:")
            print(f"   • Tickets: {stats['tickets']:,} registros")
            print(f"   • Llamadas AVAYA: {stats['avaya']:,} registros")
            print(f"   • Encuestas NPS: {stats['nps']:,} registros")
            print(f"   • Asesores: {stats['asesores']:,} registros")
            
            print(f"\n📁 ARCHIVOS GENERADOS:")
            print(f"   • sample_tickets.csv")
            print(f"   • sample_avaya.csv")
            print(f"   • sample_nps.csv")
            print(f"   • sample_asesores.csv")
            print(f"   • sample_data_complete.xlsx (consolidado)")
            
            print(f"\n🚀 EL SISTEMA ESTÁ LISTO PARA USAR!")
            print(f"   Ejecute: python src/main.py --mode dashboard")
            
        except Exception as e:
            print(f"❌ Error generando datos: {e}")
            return 1
        
        return 0

if __name__ == "__main__":
    try:
        # Intentar usar el generador avanzado
        export_sample_data_to_files()
    except:
        # Fallback a generador básico
        exit(main())