from flask import Blueprint, jsonify
from database import get_db
from datetime import datetime, timedelta

bp = Blueprint('alerts', __name__, url_prefix='/api/alertas')

def rows_to_dicts(cursor, rows):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, r)) for r in rows]

@bp.route('', methods=['GET'])
def get_alertas():
    conn = get_db()
    c = conn.cursor()
    alertas = []

    c.execute("""
        SELECT p.*, c.nombre as categoria
        FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo=1 AND p.stock_actual <= p.stock_minimo
        ORDER BY (CAST(p.stock_actual AS FLOAT) / NULLIF(p.stock_minimo,0)) ASC
    """)
    criticos = rows_to_dicts(c, c.fetchall())
    for p in criticos:
        alertas.append({
            'tipo': 'critico',
            'titulo': 'Stock Critico',
            'mensaje': f'{p["nombre"]} tiene solo {p["stock_actual"]} unidades (minimo: {p["stock_minimo"]}). Requiere reabastecimiento inmediato.',
            'producto_id': p['id'],
            'producto': p['nombre'],
            'accion': f'Pedir al menos {p["stock_maximo"] - p["stock_actual"]} unidades a {p["proveedor"] or "proveedor"}',
            'categoria': p['categoria'],
            'prioridad': 1
        })

    c.execute("""
        SELECT p.*, c.nombre as categoria
        FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo=1 AND p.stock_actual > p.stock_minimo AND p.stock_actual <= p.stock_minimo*2
        ORDER BY p.stock_actual ASC
    """)
    bajos = rows_to_dicts(c, c.fetchall())
    for p in bajos:
        alertas.append({
            'tipo': 'advertencia',
            'titulo': 'Stock Bajo',
            'mensaje': f'{p["nombre"]} tiene {p["stock_actual"]} unidades. Por debajo del nivel recomendado.',
            'producto_id': p['id'],
            'producto': p['nombre'],
            'accion': f'Programar pedido de {p["stock_maximo"] - p["stock_actual"]} unidades',
            'categoria': p['categoria'],
            'prioridad': 2
        })

    c.execute("SELECT * FROM productos WHERE activo=1 AND stock_actual > 0")
    cols = [desc[0] for desc in c.description]
    productos = [dict(zip(cols, r)) for r in c.fetchall()]
    for p in productos:
        c.execute("""
            SELECT COALESCE(SUM(dv.cantidad),0) as qty
            FROM detalle_ventas dv JOIN ventas v ON dv.venta_id=v.id
            WHERE dv.producto_id=%s AND v.fecha >= NOW() - INTERVAL '14 days'
        """, (p['id'],))
        ventas = c.fetchone()[0]
        venta_diaria = ventas / 14
        if venta_diaria > 0:
            dias = p['stock_actual'] / venta_diaria
            if dias <= 7 and p['stock_actual'] > p['stock_minimo']:
                fecha_est = (datetime.now() + timedelta(days=dias)).strftime('%d/%m/%Y')
                alertas.append({
                    'tipo': 'prediccion',
                    'titulo': 'Agotamiento Proximo',
                    'mensaje': f'{p["nombre"]} se agotara aproximadamente el {fecha_est} ({round(dias,1)} dias) al ritmo actual de ventas.',
                    'producto_id': p['id'],
                    'producto': p['nombre'],
                    'accion': f'Hacer pedido en los proximos 3 dias. Cantidad sugerida: {int(p["stock_maximo"] - p["stock_actual"])} unidades',
                    'categoria': '',
                    'prioridad': 2
                })

    c.execute("""
        SELECT p.*, c.nombre as categoria,
               ROUND(CAST((p.precio_venta - p.precio_compra)*100.0/NULLIF(p.precio_venta,0) AS numeric),1) as margen
        FROM productos p LEFT JOIN categorias c ON p.categoria_id=c.id
        WHERE p.activo=1 AND p.stock_actual <= p.stock_minimo*1.5
        AND (p.precio_venta - p.precio_compra)*100.0/NULLIF(p.precio_venta,0) >= 30
        ORDER BY margen DESC LIMIT 5
    """)
    oportunidades = rows_to_dicts(c, c.fetchall())
    for p in oportunidades:
        if not any(a['producto_id'] == p['id'] and a['tipo'] == 'critico' for a in alertas):
            alertas.append({
                'tipo': 'oportunidad',
                'titulo': 'Oportunidad de Ganancia',
                'mensaje': f'{p["nombre"]} tiene margen de {p["margen"]}% y stock limitado ({p["stock_actual"]} uds). Reabastecer maximiza ganancias.',
                'producto_id': p['id'],
                'producto': p['nombre'],
                'accion': f'Invertir en stock. Ganancia por unidad: ${round(p["precio_venta"]-p["precio_compra"],0):,.0f}',
                'categoria': p['categoria'],
                'prioridad': 3
            })

    alertas.sort(key=lambda x: x['prioridad'])
    c.close(); conn.close()
    return jsonify({
        'alertas': alertas,
        'resumen': {
            'total': len(alertas),
            'criticos': sum(1 for a in alertas if a['tipo'] == 'critico'),
            'advertencias': sum(1 for a in alertas if a['tipo'] == 'advertencia'),
            'predicciones': sum(1 for a in alertas if a['tipo'] == 'prediccion'),
            'oportunidades': sum(1 for a in alertas if a['tipo'] == 'oportunidad'),
        }
    })
