from flask import Blueprint, request, jsonify
from database import get_db
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

def rows_to_dicts(cursor, rows):
    cols = [desc[0] for desc in cursor.description]
    result = []
    for r in rows:
        d = dict(zip(cols, r))
        # Serialize any datetime/date values
        for k, v in d.items():
            if hasattr(v, 'strftime'):
                d[k] = v.strftime('%Y-%m-%d %H:%M:%S') if hasattr(v, 'hour') else v.strftime('%Y-%m-%d')
        result.append(d)
    return result

def calcular_prediccion(ventas_diarias, stock_actual):
    if not ventas_diarias or stock_actual <= 0:
        return None
    n = len(ventas_diarias)
    weights = list(range(1, n + 1))
    total_weight = sum(weights)
    promedio_ponderado = sum(v * w for v, w in zip(ventas_diarias, weights)) / total_weight
    if promedio_ponderado <= 0:
        return None
    dias_restantes = stock_actual / promedio_ponderado
    fecha_agotamiento = datetime.now() + timedelta(days=dias_restantes)
    return {
        'dias_restantes': round(dias_restantes, 1),
        'fecha_estimada': fecha_agotamiento.strftime('%Y-%m-%d'),
        'venta_diaria_promedio': round(promedio_ponderado, 2),
        'confianza': 'alta' if n >= 14 else 'media' if n >= 7 else 'baja'
    }

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT TO_CHAR(fecha,'YYYY-MM-DD') as dia,
               SUM(total) as total, SUM(ganancia) as ganancia, COUNT(*) as num_ventas
        FROM ventas
        WHERE fecha >= NOW() - INTERVAL '30 days'
        GROUP BY dia ORDER BY dia
    """)
    ventas_30 = rows_to_dicts(c, c.fetchall())

    c.execute("""
        SELECT c.nombre, SUM(dv.subtotal) as total, SUM(dv.ganancia) as ganancia,
               SUM(dv.cantidad) as unidades
        FROM detalle_ventas dv
        JOIN productos p ON dv.producto_id = p.id
        JOIN categorias c ON p.categoria_id = c.id
        JOIN ventas v ON dv.venta_id = v.id
        WHERE v.fecha >= NOW() - INTERVAL '30 days'
        GROUP BY c.nombre ORDER BY total DESC
    """)
    por_categoria = rows_to_dicts(c, c.fetchall())

    c.execute("""
        SELECT p.nombre, p.codigo, p.precio_venta, p.stock_actual,
               SUM(dv.cantidad) as total_vendido,
               SUM(dv.subtotal) as ingresos,
               SUM(dv.ganancia) as ganancias,
               ROUND(CAST((p.precio_venta - p.precio_compra) * 100.0 / NULLIF(p.precio_venta,0) AS numeric),1) as margen_promedio
        FROM detalle_ventas dv
        JOIN productos p ON dv.producto_id = p.id
        JOIN ventas v ON dv.venta_id = v.id
        WHERE v.fecha >= NOW() - INTERVAL '30 days'
        GROUP BY p.id, p.nombre, p.codigo, p.precio_venta, p.stock_actual, p.precio_compra
        ORDER BY total_vendido DESC LIMIT 10
    """)
    top_productos = rows_to_dicts(c, c.fetchall())

    if not top_productos:
        c.execute("""
            SELECT p.nombre, p.codigo, p.precio_venta, p.stock_actual,
                   COALESCE(SUM(dv.cantidad),0) as total_vendido,
                   COALESCE(SUM(dv.subtotal),0) as ingresos,
                   COALESCE(SUM(dv.ganancia),0) as ganancias,
                   ROUND(CAST((p.precio_venta - p.precio_compra) * 100.0 / NULLIF(p.precio_venta,0) AS numeric),1) as margen_promedio
            FROM productos p
            LEFT JOIN detalle_ventas dv ON dv.producto_id = p.id
            LEFT JOIN ventas v ON dv.venta_id = v.id AND v.fecha >= NOW() - INTERVAL '30 days'
            WHERE p.activo=1
            GROUP BY p.id, p.nombre, p.codigo, p.precio_venta, p.stock_actual, p.precio_compra
            ORDER BY total_vendido DESC LIMIT 10
        """)
        top_productos = rows_to_dicts(c, c.fetchall())

    c.execute("""
        SELECT metodo_pago, COUNT(*) as c, SUM(total) as total
        FROM ventas GROUP BY metodo_pago
    """)
    metodos_pago = rows_to_dicts(c, c.fetchall())

    c.close(); conn.close()
    return jsonify({
        'ventas_diarias': ventas_30,
        'por_categoria': por_categoria,
        'top_productos': top_productos,
        'metodos_pago': metodos_pago
    })

@bp.route('/predicciones', methods=['GET'])
def predicciones():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM productos WHERE activo=1")
    cols = [desc[0] for desc in c.description]
    productos = [dict(zip(cols, r)) for r in c.fetchall()]
    resultados = []

    for p in productos:
        c.execute("""
            SELECT TO_CHAR(v.fecha,'YYYY-MM-DD') as dia, SUM(dv.cantidad) as qty
            FROM detalle_ventas dv
            JOIN ventas v ON dv.venta_id = v.id
            WHERE dv.producto_id = %s AND v.fecha >= NOW() - INTERVAL '30 days'
            GROUP BY dia ORDER BY dia
        """, (p['id'],))
        ventas = c.fetchall()

        dias_dict = {r[0]: r[1] for r in ventas}
        ventas_array = []
        for i in range(30):
            dia = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
            ventas_array.append(dias_dict.get(dia, 0))

        prediccion = calcular_prediccion(ventas_array, p['stock_actual'])

        c.execute("SELECT nombre FROM categorias WHERE id=%s", (p['categoria_id'],))
        cat_row = c.fetchone()

        item = {
            'id': p['id'],
            'nombre': p['nombre'],
            'codigo': p['codigo'],
            'stock_actual': p['stock_actual'],
            'stock_minimo': p['stock_minimo'],
            'stock_maximo': p['stock_maximo'],
            'precio_venta': p['precio_venta'],
            'precio_compra': p['precio_compra'],
            'categoria': cat_row[0] if cat_row else '',
            'prediccion': prediccion,
            'estado': 'critico' if p['stock_actual'] <= p['stock_minimo'] else
                      'bajo' if p['stock_actual'] <= p['stock_minimo'] * 2 else 'normal'
        }
        resultados.append(item)

    def sort_key(x):
        if x['estado'] == 'critico':
            return (0, x['prediccion']['dias_restantes'] if x['prediccion'] else 0)
        elif x['estado'] == 'bajo':
            return (1, x['prediccion']['dias_restantes'] if x['prediccion'] else 999)
        return (2, x['prediccion']['dias_restantes'] if x['prediccion'] else 9999)

    resultados.sort(key=sort_key)
    c.close(); conn.close()
    return jsonify(resultados)

@bp.route('/recomendaciones-reabastecimiento', methods=['GET'])
def recomendaciones():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT p.*, c.nombre as categoria
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo=1
    """)
    cols = [desc[0] for desc in c.description]
    productos = [dict(zip(cols, r)) for r in c.fetchall()]

    recomendaciones_list = []
    for p in productos:
        c.execute("""
            SELECT COALESCE(SUM(dv.cantidad), 0) as qty
            FROM detalle_ventas dv
            JOIN ventas v ON dv.venta_id = v.id
            WHERE dv.producto_id = %s AND v.fecha >= NOW() - INTERVAL '30 days'
        """, (p['id'],))
        ventas_30 = c.fetchone()[0]

        venta_diaria = ventas_30 / 30
        cantidad_recomendada = 0
        urgencia = 'normal'
        motivo = ''

        if p['stock_actual'] <= p['stock_minimo']:
            cantidad_recomendada = p['stock_maximo'] - p['stock_actual']
            urgencia = 'alta'
            motivo = f'Stock critico ({p["stock_actual"]} unidades). Por debajo del minimo ({p["stock_minimo"]})'
        elif p['stock_actual'] <= p['stock_minimo'] * 2:
            cantidad_recomendada = p['stock_maximo'] - p['stock_actual']
            urgencia = 'media'
            motivo = f'Stock bajo ({p["stock_actual"]} unidades). Se recomienda reabastecer pronto'
        elif venta_diaria > 0:
            dias_stock = p['stock_actual'] / venta_diaria
            if dias_stock < 15:
                cantidad_recomendada = p['stock_maximo'] - p['stock_actual']
                urgencia = 'media'
                motivo = f'Stock durara aproximadamente {round(dias_stock)} dias al ritmo actual de ventas'

        if cantidad_recomendada > 0:
            costo_estimado = cantidad_recomendada * p['precio_compra']
            ganancia_potencial = cantidad_recomendada * (p['precio_venta'] - p['precio_compra'])
            recomendaciones_list.append({
                'producto_id': p['id'],
                'nombre': p['nombre'],
                'codigo': p['codigo'],
                'categoria': p['categoria'],
                'stock_actual': p['stock_actual'],
                'stock_minimo': p['stock_minimo'],
                'stock_maximo': p['stock_maximo'],
                'cantidad_recomendada': int(cantidad_recomendada),
                'costo_estimado': round(costo_estimado, 0),
                'ganancia_potencial': round(ganancia_potencial, 0),
                'venta_diaria': round(venta_diaria, 2),
                'urgencia': urgencia,
                'motivo': motivo,
                'proveedor': p['proveedor']
            })

    recomendaciones_list.sort(key=lambda x: {'alta': 0, 'media': 1, 'normal': 2}[x['urgencia']])
    c.close(); conn.close()
    return jsonify(recomendaciones_list)

@bp.route('/ventas-semana', methods=['GET'])
def ventas_semana():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT EXTRACT(DOW FROM fecha)::int as dow,
               SUM(total) as total, SUM(ganancia) as ganancia, COUNT(*) as num
        FROM ventas
        WHERE fecha >= NOW() - INTERVAL '90 days'
        GROUP BY dow ORDER BY dow
    """)
    cols = [desc[0] for desc in c.description]
    rows = [dict(zip(cols, r)) for r in c.fetchall()]
    c.close(); conn.close()
    dias = ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado']
    return jsonify([{'dia': dias[int(r['dow'])], **r} for r in rows])
