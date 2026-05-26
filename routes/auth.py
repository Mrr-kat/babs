from flask import Blueprint, request, jsonify, session
import os
import hashlib

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'ferreteria123')

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

@bp.route('/login', methods=['POST'])
def login():
    from database import get_db
    data = request.json or {}
    usuario = data.get('usuario', '').strip()
    contrasena = data.get('contrasena', '').strip()

    # Check hardcoded admin first
    if usuario == ADMIN_USER and contrasena == ADMIN_PASS:
        session['admin'] = True
        session['usuario'] = 'Administrador'
        session['usuario_id'] = None
        session.permanent = True
        return jsonify({'success': True, 'admin': True, 'nombre': 'Administrador'})

    # Check DB users
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM usuarios WHERE (usuario=? OR email=?) AND contrasena=?",
        (usuario, usuario, hash_pass(contrasena))
    ).fetchone()
    conn.close()

    if row:
        user = dict(row)
        session['admin'] = (user['rol'] == 'admin')
        session['usuario'] = user['nombre']
        session['usuario_id'] = user['id']
        session.permanent = True
        return jsonify({'success': True, 'admin': session['admin'], 'nombre': user['nombre']})

    return jsonify({'success': False, 'error': 'Credenciales incorrectas'}), 401

@bp.route('/register', methods=['POST'])
def register():
    from database import get_db
    data = request.json or {}
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip().lower()
    usuario = data.get('usuario', '').strip()
    contrasena = data.get('contrasena', '').strip()

    if not nombre or not email or not usuario or not contrasena:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    if len(contrasena) < 6:
        return jsonify({'error': 'La contrasena debe tener al menos 6 caracteres'}), 400
    if '@' not in email:
        return jsonify({'error': 'Email invalido'}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO usuarios (nombre, email, usuario, contrasena, rol) VALUES (?,?,?,?,?)",
            (nombre, email, usuario, hash_pass(contrasena), 'cliente')
        )
        conn.commit()
        row = conn.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,)).fetchone()
        user = dict(row)
        conn.close()

        session['admin'] = False
        session['usuario'] = user['nombre']
        session['usuario_id'] = user['id']
        session.permanent = True
        return jsonify({'success': True, 'nombre': user['nombre']})
    except Exception as e:
        conn.close()
        msg = str(e)
        if 'UNIQUE' in msg and 'email' in msg:
            return jsonify({'error': 'Ese email ya esta registrado'}), 409
        if 'UNIQUE' in msg and 'usuario' in msg:
            return jsonify({'error': 'Ese nombre de usuario ya existe'}), 409
        return jsonify({'error': 'Error al registrar'}), 400

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@bp.route('/me', methods=['GET'])
def me():
    return jsonify({
        'admin': session.get('admin', False),
        'loggedIn': 'usuario' in session,
        'nombre': session.get('usuario', None),
        'usuario_id': session.get('usuario_id', None)
    })
