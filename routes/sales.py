from flask import Blueprint, request, jsonify
from database import get_db
from datetime import datetime

bp = Blueprint('sales', __name__, url_prefix='/api/ventas')

@bp.route('', methods=['GET'])
def get_ventas():
    conn = get_db()
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    fecha_desde = request.args.get('desde', '')
    fecha_hasta = request.args.get('hasta', '')

    query = "SELECT * FROM ventas WHERE 1=1"
    params = []
    if fecha_desde:
        query += " AND fecha >= ?"
        params.append(fecha_desde)
    if fecha_hasta:
        query += " AND fecha <= ?"
        params.append(fecha_hasta + ' 23:59:59')
    query += " ORDER BY fecha DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    rows = conn.execute(query, params).fetchall()
    ventas = []
    for v in rows:
        vd = dict(v)
        detalles = conn.execute("""
            SELECT dv.*, p.nombre as producto_nombre, p.codigo
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        """, (v['id'],)).fetchall()
        vd['detalles'] = [dict(d) for d in detalles]
        ventas.append(vd)
    conn.close()
    return jsonify(ventas)

@bp.route('', methods=['POST'])
def create_venta():
    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'No hay items en la venta'}), 400

    conn = get_db()
    total = 0
    ganancia = 0
    detalle_list = []

    for item in items:
        prod = conn.execute("SELECT * FROM productos WHERE id=? AND activo=1", (item['producto_id'],)).fetchone()
        if not prod:
            conn.close()
            return jsonify({'error': f'Producto {item["producto_id"]} no encontrado'}), 404
        if prod['stock_actual'] < item['cantidad']:
            conn.close()
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

    conn.execute("""
        INSERT INTO ventas (total, ganancia, descuento, metodo_pago, observaciones)
        VALUES (?,?,?,?,?)
    """, (total_final, ganancia_final, descuento,
          data.get('metodo_pago', 'efectivo'), data.get('observaciones', '')))
    vid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    for item in detalle_list:
        conn.execute("""
            INSERT INTO detalle_ventas
            (venta_id, producto_id, cantidad, precio_unitario, precio_compra, subtotal, ganancia)
            VALUES (?,?,?,?,?,?,?)
        """, (vid, item['producto_id'], item['cantidad'], item['precio_unitario'],
              item['precio_compra'], item['subtotal'], item['ganancia']))
        nuevo_stock = item['stock_actual'] - item['cantidad']
        conn.execute("UPDATE productos SET stock_actual=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                     (nuevo_stock, item['producto_id']))
        conn.execute("""
            INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
            VALUES (?,?,?,?,?,?)
        """, (item['producto_id'], 'salida', item['cantidad'],
              item['stock_actual'], nuevo_stock, f'Venta #{vid}'))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'venta_id': vid, 'total': total_final, 'ganancia': ganancia_final})

@bp.route('/buscar-producto', methods=['GET'])
def buscar_producto():
    q = request.args.get('q', '')
    conn = get_db()
    rows = conn.execute("""
        SELECT id, nombre, codigo, precio_venta, stock_actual, unidad
        FROM productos WHERE activo=1 AND stock_actual > 0
        AND (nombre LIKE ? OR codigo LIKE ?)
        LIMIT 10
    """, (f'%{q}%', f'%{q}%')).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@bp.route('/stats', methods=['GET'])
def stats_ventas():
    conn = get_db()
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    hoy_r = conn.execute("SELECT COALESCE(SUM(total),0) as t, COALESCE(SUM(ganancia),0) as g, COUNT(*) as c FROM ventas WHERE fecha >= ?", (hoy,)).fetchone()
    mes_r = conn.execute("SELECT COALESCE(SUM(total),0) as t, COALESCE(SUM(ganancia),0) as g, COUNT(*) as c FROM ventas WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')").fetchone()
    total_r = conn.execute("SELECT COALESCE(SUM(total),0) as t, COALESCE(SUM(ganancia),0) as g, COUNT(*) as c FROM ventas").fetchone()

    top = conn.execute("""
        SELECT p.nombre, p.codigo, SUM(dv.cantidad) as total_vendido,
               SUM(dv.subtotal) as ingresos, SUM(dv.ganancia) as ganancias
        FROM detalle_ventas dv JOIN productos p ON dv.producto_id = p.id
        GROUP BY p.id ORDER BY total_vendido DESC LIMIT 5
    """).fetchall()

    conn.close()
    return jsonify({
        'hoy': {'ventas': hoy_r['c'], 'total': round(hoy_r['t'], 0), 'ganancia': round(hoy_r['g'], 0)},
        'mes': {'ventas': mes_r['c'], 'total': round(mes_r['t'], 0), 'ganancia': round(mes_r['g'], 0)},
        'total': {'ventas': total_r['c'], 'total': round(total_r['t'], 0), 'ganancia': round(total_r['g'], 0)},
        'top_productos': [dict(r) for r in top]
    })