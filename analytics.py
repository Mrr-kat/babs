from flask import Blueprint, request, jsonify
from database import get_db

bp = Blueprint('inventory', __name__, url_prefix='/api/inventario')

def rows_to_dicts(cursor, rows):
    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, r)) for r in rows]

def row_to_dict(cursor, row):
    if row is None:
        return None
    cols = [desc[0] for desc in cursor.description]
    return dict(zip(cols, row))

@bp.route('/productos', methods=['GET'])
def get_productos():
    conn = get_db()
    c = conn.cursor()
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')
    estado = request.args.get('estado', '')

    query = """
        SELECT p.id, p.nombre, p.codigo, p.categoria_id, p.precio_compra, p.precio_venta,
               p.stock_actual, p.stock_minimo, p.stock_maximo, p.unidad, p.proveedor,
               p.descripcion, p.activo, p.created_at, p.updated_at,
               p.imagen, c.nombre as categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = 1
    """
    params = []
    if search:
        query += " AND (p.nombre ILIKE %s OR p.codigo ILIKE %s)"
        params += [f'%{search}%', f'%{search}%']
    if categoria:
        query += " AND p.categoria_id = %s"
        params.append(categoria)
    if estado == 'critico':
        query += " AND p.stock_actual <= p.stock_minimo"
    elif estado == 'bajo':
        query += " AND p.stock_actual <= (p.stock_minimo * 2) AND p.stock_actual > p.stock_minimo"
    elif estado == 'normal':
        query += " AND p.stock_actual > (p.stock_minimo * 2)"
    query += " ORDER BY p.nombre"

    c.execute(query, params)
    productos = []
    for r in rows_to_dicts(c, c.fetchall()):
        if r['stock_actual'] <= r['stock_minimo']:
            r['estado_stock'] = 'critico'
        elif r['stock_actual'] <= r['stock_minimo'] * 2:
            r['estado_stock'] = 'bajo'
        else:
            r['estado_stock'] = 'normal'
        r['margen'] = round(((r['precio_venta'] - r['precio_compra']) / r['precio_venta'] * 100), 1) if r['precio_venta'] > 0 else 0
        # Serialize datetimes
        for k in ('created_at', 'updated_at'):
            if r.get(k) and hasattr(r[k], 'strftime'):
                r[k] = r[k].strftime('%Y-%m-%d %H:%M:%S')
        productos.append(r)
    c.close(); conn.close()
    return jsonify(productos)

@bp.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT p.*, c.nombre as categoria_nombre FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id WHERE p.id = %s", (id,))
    row = row_to_dict(c, c.fetchone())
    c.close(); conn.close()
    if not row:
        return jsonify({'error': 'Producto no encontrado'}), 404
    for k in ('created_at', 'updated_at'):
        if row.get(k) and hasattr(row[k], 'strftime'):
            row[k] = row[k].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(row)

@bp.route('/productos', methods=['POST'])
def create_producto():
    if request.content_type and 'multipart' in request.content_type:
        data = request.form.to_dict()
        imagen_b64 = None
        if 'imagen' in request.files:
            f = request.files['imagen']
            if f and f.filename:
                import base64
                ext = f.filename.rsplit('.', 1)[-1].lower()
                mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp', 'gif': 'image/gif'}.get(ext, 'image/jpeg')
                imagen_b64 = f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    else:
        data = request.json or {}
        imagen_b64 = data.get('imagen')

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO productos (nombre, codigo, categoria_id, precio_compra, precio_venta,
                stock_actual, stock_minimo, stock_maximo, unidad, proveedor, descripcion, imagen)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
        """, (data['nombre'], data['codigo'], data.get('categoria_id'),
              float(data['precio_compra']), float(data['precio_venta']),
              int(data.get('stock_actual', 0)),
              int(data.get('stock_minimo', 5)), int(data.get('stock_maximo', 100)),
              data.get('unidad', 'unidad'), data.get('proveedor', ''),
              data.get('descripcion', ''), imagen_b64))
        pid = c.fetchone()[0]
        if int(data.get('stock_actual', 0)) > 0:
            c.execute("""
                INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
                VALUES (%s,'entrada',%s,0,%s,'Stock inicial')
            """, (pid, int(data.get('stock_actual', 0)), int(data.get('stock_actual', 0))))
        conn.commit()
        c.close(); conn.close()
        return jsonify({'success': True, 'id': pid})
    except Exception as e:
        conn.rollback()
        c.close(); conn.close()
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
                nueva_imagen = f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    else:
        data = request.json or {}
        nueva_imagen = data.get('imagen')

    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("SELECT stock_actual, imagen FROM productos WHERE id=%s", (id,))
        old = c.fetchone()
        imagen_final = nueva_imagen if nueva_imagen else (old[1] if old else None)

        c.execute("""
            UPDATE productos SET nombre=%s, codigo=%s, categoria_id=%s, precio_compra=%s,
            precio_venta=%s, stock_actual=%s, stock_minimo=%s, stock_maximo=%s,
            unidad=%s, proveedor=%s, descripcion=%s, imagen=%s, updated_at=NOW()
            WHERE id=%s
        """, (data['nombre'], data['codigo'], data.get('categoria_id'),
              float(data['precio_compra']), float(data['precio_venta']),
              int(data['stock_actual']), int(data['stock_minimo']), int(data['stock_maximo']),
              data.get('unidad', 'unidad'), data.get('proveedor', ''),
              data.get('descripcion', ''), imagen_final, id))

        if old and old[0] != int(data['stock_actual']):
            diff = int(data['stock_actual']) - old[0]
            tipo = 'entrada' if diff > 0 else 'salida'
            c.execute("""
                INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
                VALUES (%s,%s,%s,%s,%s,'Ajuste manual')
            """, (id, tipo, abs(diff), old[0], int(data['stock_actual'])))

        conn.commit()
        c.close(); conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        c.close(); conn.close()
        return jsonify({'error': str(e)}), 400

@bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE productos SET activo=0 WHERE id=%s", (id,))
    conn.commit()
    c.close(); conn.close()
    return jsonify({'success': True})

@bp.route('/categorias', methods=['GET'])
def get_categorias():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM categorias ORDER BY nombre")
    result = rows_to_dicts(c, c.fetchall())
    c.close(); conn.close()
    return jsonify(result)

@bp.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s,%s)",
              (data['nombre'], data.get('descripcion', '')))
    conn.commit()
    c.close(); conn.close()
    return jsonify({'success': True})

@bp.route('/abastecer/<int:id>', methods=['POST'])
def abastecer(id):
    data = request.json
    cantidad = int(data.get('cantidad', 0))
    if cantidad <= 0:
        return jsonify({'error': 'Cantidad invalida'}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT stock_actual FROM productos WHERE id=%s", (id,))
    old = c.fetchone()
    if not old:
        c.close(); conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    nuevo_stock = old[0] + cantidad
    c.execute("UPDATE productos SET stock_actual=%s, updated_at=NOW() WHERE id=%s", (nuevo_stock, id))
    c.execute("""
        INSERT INTO movimientos_inventario (producto_id, tipo, cantidad, stock_antes, stock_despues, motivo)
        VALUES (%s,'entrada',%s,%s,%s,'Reabastecimiento')
    """, (id, cantidad, old[0], nuevo_stock))
    conn.commit()
    c.close(); conn.close()
    return jsonify({'success': True, 'nuevo_stock': nuevo_stock})

@bp.route('/stats', methods=['GET'])
def stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM productos WHERE activo=1")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM productos WHERE activo=1 AND stock_actual <= stock_minimo")
    criticos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM productos WHERE activo=1 AND stock_actual > stock_minimo AND stock_actual <= stock_minimo*2")
    bajo = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(stock_actual * precio_compra),0) FROM productos WHERE activo=1")
    valor = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(stock_actual * precio_venta),0) FROM productos WHERE activo=1")
    valor_venta = c.fetchone()[0]
    c.close(); conn.close()
    return jsonify({
        'total_productos': total,
        'stock_critico': criticos,
        'stock_bajo': bajo,
        'valor_inventario': round(valor, 0),
        'valor_venta_potencial': round(valor_venta, 0),
        'ganancia_potencial': round(valor_venta - valor, 0)
    })
