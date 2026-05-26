import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_PATH = os.environ.get('DB_PATH', 'ferreteria.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT DEFAULT 'cliente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            categoria_id INTEGER,
            precio_compra REAL NOT NULL DEFAULT 0,
            precio_venta REAL NOT NULL DEFAULT 0,
            stock_actual INTEGER NOT NULL DEFAULT 0,
            stock_minimo INTEGER NOT NULL DEFAULT 5,
            stock_maximo INTEGER NOT NULL DEFAULT 100,
            unidad TEXT DEFAULT 'unidad',
            proveedor TEXT,
            descripcion TEXT,
            imagen TEXT,
            activo INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL DEFAULT 0,
            ganancia REAL NOT NULL DEFAULT 0,
            descuento REAL DEFAULT 0,
            metodo_pago TEXT DEFAULT 'efectivo',
            observaciones TEXT,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );

        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            precio_compra REAL NOT NULL,
            subtotal REAL NOT NULL,
            ganancia REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );

        CREATE TABLE IF NOT EXISTS movimientos_inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            stock_antes INTEGER NOT NULL,
            stock_despues INTEGER NOT NULL,
            motivo TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
    ''')

    # Add imagen column if upgrading existing DB
    try:
        c.execute("ALTER TABLE productos ADD COLUMN imagen TEXT")
        conn.commit()
    except Exception:
        pass

    # Add usuario_id column to ventas if upgrading
    try:
        c.execute("ALTER TABLE ventas ADD COLUMN usuario_id INTEGER")
        conn.commit()
    except Exception:
        pass

    conn.commit()

    # Seed data if empty
    count = c.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    if count == 0:
        _seed_data(conn)

    conn.close()

def _seed_data(conn):
    c = conn.cursor()

    categorias = [
        ('Herramientas Manuales', 'Martillos, destornilladores, llaves'),
        ('Herramientas Electricas', 'Taladros, pulidoras, sierras'),
        ('Plomeria', 'Tubos, llaves, accesorios de agua'),
        ('Electricidad', 'Cables, interruptores, tomacorrientes'),
        ('Pinturas', 'Pinturas, brochas, rodillos'),
        ('Fijacion', 'Tornillos, clavos, pernos, tuercas'),
        ('Construccion', 'Cemento, arena, materiales basicos'),
        ('Seguridad', 'Cascos, guantes, gafas protectoras'),
    ]

    for cat in categorias:
        c.execute("INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES (?,?)", cat)

    cat_ids = {row[0]: row[1] for row in c.execute("SELECT nombre, id FROM categorias")}

    productos = [
        ('Martillo de Carpintero 16oz', 'HM-001', cat_ids['Herramientas Manuales'], 18000, 32000, 45, 10, 80, 'unidad', 'Stanley'),
        ('Destornillador Phillips #2', 'HD-002', cat_ids['Herramientas Manuales'], 5000, 9500, 78, 15, 150, 'unidad', 'Stanley'),
        ('Juego de Llaves Mixtas x12', 'HM-003', cat_ids['Herramientas Manuales'], 35000, 65000, 22, 5, 40, 'juego', 'Urrea'),
        ('Nivel de Burbuja 60cm', 'HM-004', cat_ids['Herramientas Manuales'], 22000, 42000, 18, 5, 35, 'unidad', 'Stanley'),
        ('Alicate de Presion', 'HM-005', cat_ids['Herramientas Manuales'], 15000, 28000, 33, 8, 60, 'unidad', 'Urrea'),
        ('Taladro Percutor 700W', 'HE-001', cat_ids['Herramientas Electricas'], 120000, 195000, 12, 3, 20, 'unidad', 'Bosch'),
        ('Pulidora Angular 4.5"', 'HE-002', cat_ids['Herramientas Electricas'], 95000, 158000, 8, 3, 15, 'unidad', 'Dewalt'),
        ('Sierra Caladora 500W', 'HE-003', cat_ids['Herramientas Electricas'], 85000, 140000, 6, 2, 12, 'unidad', 'Bosch'),
        ('Tubo PVC 1/2" x 6m', 'PL-001', cat_ids['Plomeria'], 8500, 15000, 120, 30, 250, 'unidad', 'Pavco'),
        ('Tubo PVC 1" x 6m', 'PL-002', cat_ids['Plomeria'], 14000, 24000, 85, 20, 180, 'unidad', 'Pavco'),
        ('Llave de Paso 1/2"', 'PL-003', cat_ids['Plomeria'], 12000, 22000, 55, 15, 100, 'unidad', 'Plastiferr'),
        ('Codo PVC 90 1/2"', 'PL-004', cat_ids['Plomeria'], 800, 1800, 280, 50, 500, 'unidad', 'Pavco'),
        ('Cable THHN #12 x 100m', 'EL-001', cat_ids['Electricidad'], 85000, 145000, 20, 5, 40, 'rollo', 'Condumex'),
        ('Toma Corriente Doble', 'EL-002', cat_ids['Electricidad'], 4500, 9000, 145, 30, 300, 'unidad', 'Legrand'),
        ('Interruptor Sencillo', 'EL-003', cat_ids['Electricidad'], 3500, 7500, 160, 30, 300, 'unidad', 'Legrand'),
        ('Cinta Aislante 3M', 'EL-004', cat_ids['Electricidad'], 2800, 5500, 95, 20, 200, 'unidad', '3M'),
        ('Pintura Blanca Vinilo x4L', 'PI-001', cat_ids['Pinturas'], 28000, 48000, 35, 10, 80, 'galon', 'Pintuco'),
        ('Pintura Aceite Gris x1L', 'PI-002', cat_ids['Pinturas'], 18000, 32000, 28, 8, 60, 'litro', 'Pintuco'),
        ('Brocha 3" Cerda Natural', 'PI-003', cat_ids['Pinturas'], 6500, 12000, 65, 15, 120, 'unidad', 'Condor'),
        ('Rodillo Felpa 9"', 'PI-004', cat_ids['Pinturas'], 8000, 15500, 42, 10, 80, 'unidad', 'Condor'),
        ('Tornillos Drywall 1" x500', 'FI-001', cat_ids['Fijacion'], 9500, 18000, 88, 20, 180, 'caja', 'Hilti'),
        ('Tornillos Madera 2" x100', 'FI-002', cat_ids['Fijacion'], 5500, 10500, 112, 25, 200, 'caja', 'Hilti'),
        ('Pernos Hexagonales 5/16 x50', 'FI-003', cat_ids['Fijacion'], 7000, 13500, 75, 20, 150, 'caja', 'Grival'),
        ('Clavos 2" x1kg', 'FI-004', cat_ids['Fijacion'], 4500, 8500, 95, 25, 200, 'kg', 'Grival'),
        ('Cemento Gris x50kg', 'CO-001', cat_ids['Construccion'], 28000, 42000, 60, 15, 120, 'bulto', 'Cemex'),
        ('Arena de Construccion x50kg', 'CO-002', cat_ids['Construccion'], 8000, 14000, 40, 10, 80, 'bulto', 'Local'),
        ('Casco de Seguridad', 'SE-001', cat_ids['Seguridad'], 18000, 32000, 25, 8, 50, 'unidad', 'MSA'),
        ('Guantes de Nitrilo x12', 'SE-002', cat_ids['Seguridad'], 12000, 22000, 38, 10, 80, 'par', 'Ansell'),
        ('Gafas de Seguridad', 'SE-003', cat_ids['Seguridad'], 8500, 16000, 30, 10, 60, 'unidad', '3M'),
        ('Tapa Oidos Espuma x2', 'SE-004', cat_ids['Seguridad'], 3500, 7000, 55, 15, 100, 'par', '3M'),
    ]

    for p in productos:
        c.execute("""
            INSERT INTO productos (nombre, codigo, categoria_id, precio_compra, precio_venta,
                stock_actual, stock_minimo, stock_maximo, unidad, proveedor)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, p)

    # Generate 60 days of historical sales
    now = datetime.now()
    prod_ids = [row[0] for row in c.execute("SELECT id FROM productos")]
    popular = prod_ids[:12]

    for day in range(60, 0, -1):
        fecha = now - timedelta(days=day)
        num_ventas = random.randint(3, 8)
        for _ in range(num_ventas):
            items = random.sample(popular + random.sample(prod_ids, 3), random.randint(1, 4))
            total = 0
            ganancia = 0
            detalle_items = []
            for pid in items:
                row = c.execute("SELECT precio_venta, precio_compra FROM productos WHERE id=?", (pid,)).fetchone()
                if row:
                    qty = random.randint(1, 5)
                    sub = row[0] * qty
                    gan = (row[0] - row[1]) * qty
                    total += sub
                    ganancia += gan
                    detalle_items.append((pid, qty, row[0], row[1], sub, gan))

            if detalle_items:
                c.execute("""
                    INSERT INTO ventas (fecha, total, ganancia, metodo_pago)
                    VALUES (?, ?, ?, ?)
                """, (fecha.strftime('%Y-%m-%d %H:%M:%S'), total, ganancia,
                      random.choice(['efectivo', 'tarjeta', 'transferencia'])))
                vid = c.lastrowid
                for item in detalle_items:
                    c.execute("""
                        INSERT INTO detalle_ventas
                        (venta_id, producto_id, cantidad, precio_unitario, precio_compra, subtotal, ganancia)
                        VALUES (?,?,?,?,?,?,?)
                    """, (vid,) + item)

    conn.commit()
