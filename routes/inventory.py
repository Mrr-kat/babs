from flask import Blueprint, request, jsonify
from database import get_db
from datetime import datetime

bp = Blueprint('inventory', __name__, url_prefix='/api/inventario')

@bp.route('/productos', methods=['GET'])
def get_productos():
    conn = get_db()
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')
    estado = request.args.get('estado', '')

    query = """
        SELECT p.id, p.nombre, p.codigo, p.categoria_id, p.precio_compra, p.precio_venta,
               p.stock_actual, p.stock_minimo, p.stock_maximo, p.unidad, p.proveedor,
               p.descripcion, p.activo, p.created_at, p.updated_at,
               p.imagen,
               c.nombre as categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = 1
    """
    params = []
    if search:
        query += " AND (p.nombre LIKE ? OR p.codigo LIKE ?)"
        params += [f'%{search}%', f'%{search}%']
    if categoria:
        query += " AND p.categoria_id = ?"
        params.append(categoria)
    if estado == 'critico':
        query += " AND p.stock_actual <= p.stock_minimo"
    elif estado == 'bajo':
        query += " AND p.stock_actual <= (p.stock_minimo * 2) AND p.stock_actual > p.stock_minimo"
    elif estado == 'normal':
        query += " AND p.stock_actual > (p.stock_minimo * 2)"

    query += " ORDER BY p.nombre"

    rows = conn.execute(query, params).fetchall()
    productos = []
    for r in rows:
        p = dict(r)
        if p['stock_actual'] <= p['stock_minimo']:
            p['estado_stock'] = 'critico'
        elif p['stock_actual'] <= p['stock_minimo'] * 2:
            p['estado_stock'] = 'bajo'
        else:
            p['estado_stock'] = 'normal'
        p['margen'] = round(((p['precio_venta'] - p['precio_compra']) / p['precio_venta'] * 100), 1) if p['precio_venta'] > 0 else 0
        productos.append(p)
    conn.close()
    return jsonify(productos)

@bp.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    conn = get_db()
    row = conn.execute("""
        SELECT p.*, c.nombre as categoria_nombre
        FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    """, (id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify(dict(row))

@bp.route('/productos', methods=['POST'])
def create_producto():
    # Support both JSON and multipart form data
    if request.content_type and 'multipart' in request.content_type:
        data = request.form.to_dict()
        imagen_b64 = None
        if 'imagen' in request.files:
            f = request.files['imagen']
            if f and f.filename:
                import base64
                ext = f.filename.rsplit('.', 1)[-1].lower()
                mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp', 'gif': 'image/gif'}.get(ext, 'image/jpeg')
                b64 = base64.b64encode(f.read()).decode('utf-8')
                imagen_b64 = f"data:{mime};base64,{b64}"
    else:
        data = request.json or {}
        imagen_b64 = data.get('imagen')

    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO productos (nombre, codigo, categoria_id, precio_compra, precio_venta,
                stock_actual, stock_minimo, stock_maximo, unidad, proveedor, descripcion, imagen)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (data['nombre'], data['codigo'], data.get('categoria_id'),
              float(data['precio_compra']), float(data['precio_venta']),
              int(data.get('stock_actual', 0)),
              int(data.get('stock_minimo', 5)), int(data.get('stock_maximo', 100)),
              data.get('unidad', 'unidad'), data.get('proveedor', ''),
              data.get('descripcion', ''), imagen_b64))
        conn.commit()
        pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        if int(data.get('stock_actual', 0)) > 0:
            conn.execute("""
                INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
                VALUES (?, 'entrada', ?, 0, ?, 'Stock inicial')
            """, (pid, int(data.get('stock_actual', 0)), int(data.get('stock_actual', 0))))
            conn.commit()
        conn.close()
        return jsonify({'success': True, 'id': pid})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@bp.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    if request.content_type and 'multipart' in request.content_type:
        data = request.form.to_dict()
        nueva_imagen = None
        if 'imagen' in request.files:
            f = request.files['imagen']
            if f and f.filename:
                import base64
                ext = f.filename.rsplit('.', 1)[-1].lower()
                mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp', 'gif': 'image/gif'}.get(ext, 'image/jpeg')
                b64 = base64.b64encode(f.read()).decode('utf-8')
                nueva_imagen = f"data:{mime};base64,{b64}"
    else:
        data = request.json or {}
        nueva_imagen = data.get('imagen')

    conn = get_db()
    try:
        old = conn.execute("SELECT stock_actual, imagen FROM productos WHERE id=?", (id,)).fetchone()

        # Use existing image if no new one provided
        imagen_final = nueva_imagen if nueva_imagen else (old['imagen'] if old else None)

        conn.execute("""
            UPDATE productos SET nombre=?, codigo=?, categoria_id=?, precio_compra=?,
            precio_venta=?, stock_actual=?, stock_minimo=?, stock_maximo=?,
            unidad=?, proveedor=?, descripcion=?, imagen=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (data['nombre'], data['codigo'], data.get('categoria_id'),
              float(data['precio_compra']), float(data['precio_venta']),
              int(data['stock_actual']), int(data['stock_minimo']), int(data['stock_maximo']),
              data.get('unidad', 'unidad'), data.get('proveedor', ''),
              data.get('descripcion', ''), imagen_final, id))

        if old and old['stock_actual'] != int(data['stock_actual']):
            diff = int(data['stock_actual']) - old['stock_actual']
            tipo = 'entrada' if diff > 0 else 'salida'
            conn.execute("""
                INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
                VALUES (?,?,?,?,?,'Ajuste manual')
            """, (id, tipo, abs(diff), old['stock_actual'], int(data['stock_actual'])))

        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    conn = get_db()
    conn.execute("UPDATE productos SET activo=0 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@bp.route('/categorias', methods=['GET'])
def get_categorias():
    conn = get_db()
    rows = conn.execute("SELECT * FROM categorias ORDER BY nombre").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@bp.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?,?)",
                 (data['nombre'], data.get('descripcion', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@bp.route('/abastecer/<int:id>', methods=['POST'])
def abastecer(id):
    data = request.json
    cantidad = int(data.get('cantidad', 0))
    if cantidad <= 0:
        return jsonify({'error': 'Cantidad invalida'}), 400
    conn = get_db()
    old = conn.execute("SELECT stock_actual FROM productos WHERE id=?", (id,)).fetchone()
    if not old:
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    nuevo_stock = old['stock_actual'] + cantidad
    conn.execute("UPDATE productos SET stock_actual=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                 (nuevo_stock, id))
    conn.execute("""
        INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
        VALUES (?, 'entrada', ?, ?, ?, 'Reabastecimiento')
    """, (id, cantidad, old['stock_actual'], nuevo_stock))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'nuevo_stock': nuevo_stock})

@bp.route('/stats', methods=['GET'])
def stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as c FROM productos WHERE activo=1").fetchone()['c']
    criticos = conn.execute("SELECT COUNT(*) as c FROM productos WHERE activo=1 AND stock_actual <= stock_minimo").fetchone()['c']
    bajo = conn.execute("SELECT COUNT(*) as c FROM productos WHERE activo=1 AND stock_actual > stock_minimo AND stock_actual <= stock_minimo*2").fetchone()['c']
    valor = conn.execute("SELECT COALESCE(SUM(stock_actual * precio_compra),0) as v FROM productos WHERE activo=1").fetchone()['v']
    valor_venta = conn.execute("SELECT COALESCE(SUM(stock_actual * precio_venta),0) as v FROM productos WHERE activo=1").fetchone()['v']
    conn.close()
    return jsonify({
        'total_productos': total,
        'stock_critico': criticos,
        'stock_bajo': bajo,
        'valor_inventario': round(valor, 0),
        'valor_venta_potencial': round(valor_venta, 0),
        'ganancia_potencial': round(valor_venta - valor, 0)
    })
