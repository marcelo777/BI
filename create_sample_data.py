#!/usr/bin/env python3
"""
Generador de datos de ejemplo básico (sin dependencias externas)

Este script crea datos de ejemplo en formato CSV usando solo bibliotecas estándar de Python.
Permite que el sistema funcione completamente sin instalar dependencias.

Autor: Sistema KPI Dashboard  
Fecha: 2025-09-16
"""

import csv
import random
import json
from datetime import datetime, timedelta
from pathlib import Path


def create_sample_data():
    """Genera todos los datos de ejemplo necesarios"""
    
    # Crear directorio
    samples_dir = Path(__file__).parent / 'data' / 'samples'
    samples_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== GENERADOR DE DATOS DE EJEMPLO ===")
    print("Sistema KPI Dashboard")
    print("=" * 50)
    
    # 1. TICKETS
    print("1. Generando tickets...")
    tickets_file = samples_dir / 'sample_tickets.csv'
    
    with open(tickets_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Headers
        writer.writerow([
            'ticket_id', 'fecha_creacion', 'fecha_resolucion', 'producto', 
            'segmento_cliente', 'asesor_id', 'asesor_nombre', 'asesor_nivel',
            'causa_original', 'area_responsable', 'escalado', 'escalado_a',
            'resuelto_primera_instancia', 'reabierto', 'mttr_horas', 
            'satisfaccion_cliente', 'cliente_id', 'canal_entrada', 'prioridad', 'complejidad'
        ])
        
        productos = ['Internet Hogar', 'TV Cable', 'Telefonía Fija', 'Móvil Postpago', 'Móvil Prepago', 'Internet Móvil', 'Empresarial']
        segmentos = ['VIP', 'Premium', 'Regular', 'Básico']
        causas = [
            'Sin señal TV canal específico', 'Lentitud navegación específica', 'Corte intermitente fibra',
            'Consulta plan específico región', 'Cambio plan mayor capacidad', 'Duda promoción temporal',
            'Actualización datos personales', 'Cambio email contacto', 'Solicitud certificado ingresos',
            'Falla WiFi 5GHz específica', 'Error configuración router', 'Problema VoIP corporativa'
        ]
        areas_noc = ['NOC_Central', 'NOC_Norte', 'NOC_Sur', 'NOC_Este', 'NOC_Oeste']
        
        # Generar 1000 tickets
        for i in range(1000):
            fecha_base = datetime.now() - timedelta(days=random.randint(1, 90))
            mttr_hours = round(random.uniform(0.5, 48.0), 2)
            fecha_resolucion = fecha_base + timedelta(hours=mttr_hours)
            escalado = random.choice([True, False])
            
            writer.writerow([
                f'TKT_{i+1:06d}',
                fecha_base.strftime('%Y-%m-%d %H:%M:%S'),
                fecha_resolucion.strftime('%Y-%m-%d %H:%M:%S'),
                random.choice(productos),
                random.choice(segmentos),
                f'ASE_{random.randint(1, 50):03d}',
                f'Asesor_{random.randint(1, 50):03d}',
                random.choice(['Junior', 'Semi-Senior', 'Senior']),
                random.choice(causas),
                random.choice(['Técnico', 'Comercial', 'Retención', 'Soporte']),
                escalado,
                random.choice(areas_noc) if escalado else '',
                random.choice([True, False]),
                random.choice([True, False]),
                mttr_hours,
                random.randint(1, 10),
                f'CLI_{random.randint(1, 50000):05d}',
                random.choice(['Web', 'Telefono', 'App', 'Presencial']),
                random.choice(['Alta', 'Media', 'Baja']),
                random.choice(['Alta', 'Media', 'Baja'])
            ])
    
    print(f"   ✅ 1,000 tickets generados en {tickets_file}")
    
    # 2. AVAYA
    print("2. Generando datos AVAYA...")
    avaya_file = samples_dir / 'sample_avaya.csv'
    
    with open(avaya_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow([
            'call_id', 'timestamp', 'operador', 'cola', 'tiempo_cola_segundos',
            'aht_minutos', 'abandonada', 'transferida', 'producto_consultado',
            'tipo_llamada', 'satisfaccion_llamada', 'cliente_id', 'numero_origen', 'duracion_total_segundos'
        ])
        
        operadores = ['Operador_A', 'Operador_B', 'Operador_C', 'Operador_D', 'Operador_E']
        colas = ['Cola_Tecnica', 'Cola_Comercial', 'Cola_Retencion', 'Cola_Soporte']
        
        # Generar 2000 llamadas
        for i in range(2000):
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 2160))  # 90 días
            abandonada = random.choice([True, False])
            aht = 0 if abandonada else round(random.uniform(5, 35), 2)
            tiempo_cola = random.randint(10, 300)
            
            writer.writerow([
                f'CALL_{i+1:08d}',
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                random.choice(operadores),
                random.choice(colas),
                tiempo_cola,
                aht,
                abandonada,
                random.choice([True, False]),
                random.choice(productos),
                random.choice(['Consulta', 'Reclamo', 'Soporte_Tecnico', 'Comercial']),
                random.randint(1, 10) if not abandonada else '',
                f'CLI_{random.randint(1, 50000):05d}',
                f'+56{random.randint(900000000, 999999999)}',
                int(tiempo_cola + (aht * 60)) if not abandonada else tiempo_cola
            ])
    
    print(f"   ✅ 2,000 llamadas AVAYA generadas en {avaya_file}")
    
    # 3. NPS
    print("3. Generando datos NPS...")
    nps_file = samples_dir / 'sample_nps.csv'
    
    with open(nps_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow([
            'respuesta_id', 'fecha_respuesta', 'cliente_id', 'producto', 'segmento_cliente',
            'nps_score', 'categoria_nps', 'comentario', 'canal_encuesta', 'tiempo_respuesta_dias',
            'contacto_previo', 'resolucion_satisfactoria', 'recomendaria_servicio', 'region',
            'edad_cliente', 'antiguedad_meses'
        ])
        
        comentarios_detractores = [
            'Servicio muy lento, muchas fallas',
            'Atención al cliente deficiente',
            'Problemas técnicos constantes',
            'Precio muy alto para el servicio'
        ]
        
        comentarios_neutrales = [
            'Servicio regular, podría mejorar',
            'Funciona pero tiene algunos problemas',
            'Precio aceptable, servicio promedio'
        ]
        
        comentarios_promotores = [
            'Excelente servicio, muy satisfecho',
            'Atención rápida y efectiva',
            'Buena relación calidad-precio',
            'Personal muy profesional'
        ]
        
        # Generar 500 encuestas NPS
        for i in range(500):
            fecha = datetime.now() - timedelta(days=random.randint(1, 90))
            nps_score = random.randint(0, 10)
            
            if nps_score <= 6:
                categoria = 'Detractor'
                comentario = random.choice(comentarios_detractores)
            elif nps_score <= 8:
                categoria = 'Neutral'
                comentario = random.choice(comentarios_neutrales)
            else:
                categoria = 'Promotor'
                comentario = random.choice(comentarios_promotores)
            
            writer.writerow([
                f'NPS_{i+1:06d}',
                fecha.strftime('%Y-%m-%d %H:%M:%S'),
                f'CLI_{random.randint(1, 50000):05d}',
                random.choice(productos),
                random.choice(segmentos),
                nps_score,
                categoria,
                comentario,
                random.choice(['Email', 'SMS', 'App', 'Web']),
                random.randint(0, 7),
                random.choice([True, False]),
                random.choice([True, False]),
                nps_score >= 7,
                random.choice(['Norte', 'Centro', 'Sur', 'Este', 'Oeste']),
                random.randint(18, 75),
                random.randint(1, 120)
            ])
    
    print(f"   ✅ 500 encuestas NPS generadas en {nps_file}")
    
    # 4. ASESORES
    print("4. Generando catálogo de asesores...")
    asesores_file = samples_dir / 'sample_asesores.csv'
    
    with open(asesores_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow([
            'asesor_id', 'nombre', 'nivel_experiencia', 'fcr_esperado', 'aht_esperado',
            'area', 'turno', 'fecha_ingreso'
        ])
        
        # Generar 50 asesores
        for i in range(50):
            nivel = random.choice(['Junior', 'Semi-Senior', 'Senior'])
            
            # FCR y AHT esperado basado en nivel
            if nivel == 'Junior':
                fcr_esperado = round(random.uniform(0.10, 0.20), 3)
                aht_esperado = round(random.uniform(20, 30), 1)
            elif nivel == 'Semi-Senior':
                fcr_esperado = round(random.uniform(0.20, 0.30), 3)
                aht_esperado = round(random.uniform(15, 25), 1)
            else:  # Senior
                fcr_esperado = round(random.uniform(0.30, 0.40), 3)
                aht_esperado = round(random.uniform(12, 20), 1)
            
            fecha_ingreso = datetime.now() - timedelta(days=random.randint(30, 1095))
            
            writer.writerow([
                f'ASE_{i+1:03d}',
                f'Asesor_{i+1:03d}',
                nivel,
                fcr_esperado,
                aht_esperado,
                random.choice(['Técnico', 'Comercial', 'Retención', 'Soporte']),
                random.choice(['Mañana', 'Tarde', 'Noche']),
                fecha_ingreso.strftime('%Y-%m-%d')
            ])
    
    print(f"   ✅ 50 asesores generados en {asesores_file}")
    
    # 5. CREAR ARCHIVO DE CONFIGURACIÓN PARA DATOS DE EJEMPLO
    print("5. Creando configuración para datos de ejemplo...")
    
    config_sample = {
        'database': {
            'use_sample_data': True,
            'sample_data_path': 'data/samples'
        },
        'avaya': {
            'use_sample_data': True,
            'sample_data_path': 'data/samples'
        },
        'nps': {
            'use_sample_data': True,
            'sample_data_path': 'data/samples'
        },
        'dashboard': {
            'auto_refresh_minutes': 5,
            'debug': True,
            'port': 8050
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/kpi_dashboard.log'
        }
    }
    
    config_file = Path(__file__).parent / 'config' / 'config_sample_data.yaml'
    config_file.parent.mkdir(exist_ok=True)
    
    # Escribir como YAML básico
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write("# Configuración para usar datos de ejemplo\n")
        f.write("# Generado automáticamente\n\n")
        
        def write_yaml_section(obj, indent=0):
            for key, value in obj.items():
                if isinstance(value, dict):
                    f.write('  ' * indent + f"{key}:\n")
                    write_yaml_section(value, indent + 1)
                else:
                    f.write('  ' * indent + f"{key}: {value}\n")
        
        write_yaml_section(config_sample)
    
    print(f"   ✅ Configuración creada en {config_file}")
    
    # 6. CREAR ARCHIVO README PARA LOS DATOS
    print("6. Creando documentación de datos...")
    
    readme_content = """# Datos de Ejemplo - Sistema KPI Dashboard

## Descripción
Este directorio contiene datos simulados para ejecutar el Sistema KPI Dashboard sin conexiones reales a bases de datos o APIs externas.

## Archivos Generados

### sample_tickets.csv (1,000 registros)
- Tickets de customer service simulados
- Incluye: FCR, MTTR, escalaciones, segmentación
- Período: últimos 90 días

### sample_avaya.csv (2,000 registros)  
- Llamadas del sistema AVAYA simuladas
- Incluye: AHT, abandono, colas, operadores
- Período: últimos 90 días

### sample_nps.csv (500 registros)
- Encuestas NPS simuladas por producto
- Incluye: scores, categorización, comentarios
- Período: últimos 90 días

### sample_asesores.csv (50 registros)
- Catálogo de asesores con perfiles realistas
- Incluye: niveles, FCR esperado, AHT esperado

## Uso
Los datos se cargan automáticamente cuando el sistema no puede conectar a fuentes reales.

## Ejecutar con Datos de Ejemplo
```bash
python src/main.py --mode dashboard
python src/main.py --mode process --export
python src/main.py --mode full
```

## Estadísticas
- Total registros: 3,550
- Período simulado: 90 días
- Volumen diario promedio: ~40 registros
- Cobertura: Todos los KPIs requeridos

Generado: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
"""
    
    readme_file = samples_dir / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✅ Documentación creada en {readme_file}")
    
    # RESUMEN FINAL
    print(f"\n✅ GENERACIÓN COMPLETADA EXITOSAMENTE!")
    print(f"📁 Ubicación: {samples_dir}")
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Tickets: 1,000 registros")
    print(f"   • Llamadas AVAYA: 2,000 registros")  
    print(f"   • Encuestas NPS: 500 registros")
    print(f"   • Asesores: 50 registros")
    print(f"   • Total: 3,550 registros")
    
    print(f"\n📁 ARCHIVOS GENERADOS:")
    print(f"   • sample_tickets.csv")
    print(f"   • sample_avaya.csv")
    print(f"   • sample_nps.csv")
    print(f"   • sample_asesores.csv")
    print(f"   • README.md")
    print(f"   • config_sample_data.yaml")
    
    print(f"\n🚀 EL SISTEMA ESTÁ LISTO PARA USAR!")
    print(f"   Ejecute: python src/main.py --mode dashboard")
    print(f"   O también: python src/main.py --mode process --export")
    
    return True


if __name__ == "__main__":
    try:
        create_sample_data()
        print(f"\n🎉 ¡Datos de ejemplo creados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error generando datos: {e}")
        exit(1)