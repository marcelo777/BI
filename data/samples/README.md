# Datos de Ejemplo - Sistema KPI Dashboard

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

Generado: 2025-09-16 12:12:36
