from flask import Blueprint, request, jsonify
from database import get_db
from datetime import datetime
import pytz

bp = Blueprint('sales', __name__, url_prefix='/api/ventas')

def bogota_now():
    """Retorna la fecha/hora actual en zona horaria de Bogotá (UTC-5)."""
    tz = pytz.timezone('America/Bogota')
    return datetime.now(tz).replace(tzinfo=None)  # naive datetime en hora local

@bp.route('', methods=['GET'])
def get_ventas():
    conn = get_db()
    c = conn.cursor()
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    fecha_desde = request.args.get('desde', '')
    fecha_hasta = request.args.get('hasta', '')

    query = "SELECT * FROM ventas WHERE 1=1"
    params = []
    if fecha_desde:
        query += " AND fecha >= %s"
        params.append(fecha_desde)
    if fecha_hasta:
        query += " AND fecha <= %s"
        params.append(fecha_hasta + ' 23:59:59')
    query += " ORDER BY fecha DESC LIMIT %s OFFSET %s"
    params += [limit, offset]

    c.execute(query, params)
    cols = [desc[0] for desc in c.description]
    rows = c.fetchall()

    ventas = []
    for v in rows:
        vd = dict(zip(cols, v))
        # Convertir fecha a string si es datetime
        if vd.get('fecha') and hasattr(vd['fecha'], 'strftime'):
            vd['fecha'] = vd['fecha'].strftime('%Y-%m-%d %H:%M:%S')

        c.execute("""
            SELECT dv.*, p.nombre as producto_nombre, p.codigo
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = %s
        """, (vd['id'],))
        det_cols = [desc[0] for desc in c.description]
        detalles = c.fetchall()
        vd['detalles'] = [dict(zip(det_cols, d)) for d in detalles]
        ventas.append(vd)

    c.close()
    conn.close()
    return jsonify(ventas)

@bp.route('', methods=['POST'])
def create_venta():
    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'No hay items en la venta'}), 400

    conn = get_db()
    c = conn.cursor()
    total = 0
    ganancia = 0
    detalle_list = []

    for item in items:
        c.execute("SELECT * FROM productos WHERE id=%s AND activo=1", (item['producto_id'],))
        cols = [desc[0] for desc in c.description]
        row = c.fetchone()
        if not row:
            c.close(); conn.close()
            return jsonify({'error': f'Producto {item["producto_id"]} no encontrado'}), 404
        prod = dict(zip(cols, row))

        if prod['stock_actual'] < item['cantidad']:
            c.close(); conn.close()
            return jsonify({'error': f'Stock insuficiente para {prod["nombre"]}. Disponible: {prod["stock_actual"]}'}), 400

        precio = item.get('precio_unitario', prod['precio_venta'])
        subtotal = precio * item['cantidad']
        gan = (precio - prod['precio_compra']) * item['cantidad']
        total += subtotal
        ganancia += gan
        detalle_list.append({
            'producto_id': item['producto_id'],
            'cantidad': item['cantidad'],
            'precio_unitario': precio,
            'precio_compra': prod['precio_compra'],
            'subtotal': subtotal,
            'ganancia': gan,
            'stock_actual': prod['stock_actual']
        })

    descuento = data.get('descuento', 0)
    total_final = total - descuento
    ganancia_final = ganancia - descuento

    # Insertar con la fecha actual en zona horaria de Bogotá
    fecha_bogota = bogota_now()
    c.execute("""
        INSERT INTO ventas (fecha, total, ganancia, descuento, metodo_pago, observaciones)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id
    """, (fecha_bogota, total_final, ganancia_final, descuento,
          data.get('metodo_pago', 'efectivo'), data.get('observaciones', '')))
    vid = c.fetchone()[0]

    for item in detalle_list:
        c.execute("""
            INSERT INTO detalle_ventas
            (venta_id, producto_id, cantidad, precio_unitario, precio_compra, subtotal, ganancia)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (vid, item['producto_id'], item['cantidad'], item['precio_unitario'],
              item['precio_compra'], item['subtotal'], item['ganancia']))
        nuevo_stock = item['stock_actual'] - item['cantidad']
        c.execute("UPDATE productos SET stock_actual=%s, updated_at=NOW() WHERE id=%s",
                  (nuevo_stock, item['producto_id']))
        c.execute("""
            INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (item['producto_id'], 'salida', item['cantidad'],
              item['stock_actual'], nuevo_stock, f'Venta #{vid}'))

    conn.commit()
    c.close()
    conn.close()
    return jsonify({'success': True, 'venta_id': vid, 'total': total_final, 'ganancia': ganancia_final})

@bp.route('/buscar-producto', methods=['GET'])
def buscar_producto():
    q = request.args.get('q', '')
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT id, nombre, codigo, precio_venta, stock_actual, unidad
        FROM productos WHERE activo=1 AND stock_actual > 0
        AND (nombre ILIKE %s OR codigo ILIKE %s)
        LIMIT 10
    """, (f'%{q}%', f'%{q}%'))
    cols = [desc[0] for desc in c.description]
    rows = c.fetchall()
    c.close()
    conn.close()
    return jsonify([dict(zip(cols, r)) for r in rows])

@bp.route('/stats', methods=['GET'])
def stats_ventas():
    conn = get_db()
    c = conn.cursor()

    # Fecha de hoy en Bogotá
    hoy = bogota_now().strftime('%Y-%m-%d')

    c.execute("SELECT COALESCE(SUM(total),0), COALESCE(SUM(ganancia),0), COUNT(*) FROM ventas WHERE fecha >= %s", (hoy,))
    hoy_r = c.fetchone()
    c.execute("SELECT COALESCE(SUM(total),0), COALESCE(SUM(ganancia),0), COUNT(*) FROM ventas WHERE TO_CHAR(fecha,'YYYY-MM') = TO_CHAR(NOW(),'YYYY-MM')")
    mes_r = c.fetchone()
    c.execute("SELECT COALESCE(SUM(total),0), COALESCE(SUM(ganancia),0), COUNT(*) FROM ventas")
    total_r = c.fetchone()

    c.execute("""
        SELECT p.nombre, p.codigo, SUM(dv.cantidad) as total_vendido,
               SUM(dv.subtotal) as ingresos, SUM(dv.ganancia) as ganancias
        FROM detalle_ventas dv JOIN productos p ON dv.producto_id = p.id
        GROUP BY p.id, p.nombre, p.codigo ORDER BY total_vendido DESC LIMIT 5
    """)
    top_cols = [desc[0] for desc in c.description]
    top = [dict(zip(top_cols, r)) for r in c.fetchall()]

    c.close()
    conn.close()
    return jsonify({
        'hoy': {'ventas': hoy_r[2], 'total': round(hoy_r[0], 0), 'ganancia': round(hoy_r[1], 0)},
        'mes': {'ventas': mes_r[2], 'total': round(mes_r[0], 0), 'ganancia': round(mes_r[1], 0)},
        'total': {'ventas': total_r[2], 'total': round(total_r[0], 0), 'ganancia': round(total_r[1], 0)},
        'top_productos': top
    })
