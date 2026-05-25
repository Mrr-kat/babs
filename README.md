# Sistema Inteligente de Inventario — Ferreteria

Sistema de gestion de inventario con prediccion de stock, registro de ventas, analitica y alertas inteligentes.

## Tecnologias

- **Backend**: Python + Flask
- **Base de datos**: SQLite (automatica, sin configuracion)
- **Frontend**: HTML + CSS + JS + Chart.js
- **Despliegue**: Railway

---

## Estructura del proyecto

```
ferreteria/
├── app.py                  # Aplicacion principal Flask
├── database.py             # Inicializacion de base de datos y datos de prueba
├── requirements.txt
├── Procfile                # Para Railway/Heroku
├── railway.toml
├── routes/
│   ├── __init__.py
│   ├── inventory.py        # API de inventario
│   ├── sales.py            # API de ventas
│   ├── analytics.py        # API de analitica
│   └── alerts.py           # API de alertas
├── templates/
│   ├── base.html           # Layout base con sidebar
│   ├── index.html          # Panel general
│   ├── inventario.html     # Gestion de inventario
│   ├── ventas.html         # Registro de ventas
│   ├── analytics.html      # Analitica e inteligencia
│   └── alertas.html        # Alertas y recomendaciones
└── static/
    └── css/
        └── main.css
```

---

## Correr en local

```bash
# 1. Clonar o descomprimir el proyecto
# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr
python app.py
```

Abrir en el navegador: `http://localhost:5000`

La base de datos SQLite se crea automaticamente con datos de prueba al iniciar por primera vez.

---

## Desplegar en Railway

1. Subir el proyecto a un repositorio de GitHub
2. Entrar a [railway.app](https://railway.app) y crear un nuevo proyecto desde GitHub
3. Railway detecta automaticamente el `Procfile` y `requirements.txt`
4. Agregar la variable de entorno: `SECRET_KEY=tu-clave-secreta-aqui`
5. El sitio queda disponible en la URL que Railway asigna

> La base de datos SQLite se almacena en el sistema de archivos del contenedor. Para persistencia entre reinicios en Railway, se puede usar un volumen o migrar a PostgreSQL.

---

## Funcionalidades

| Modulo | Descripcion |
|---|---|
| Panel General | Resumen de ventas, ganancias, graficas del mes |
| Inventario | CRUD de productos, reabastecer, filtros por estado |
| Ventas | Registrar ventas con autocomplete, historial filtrable |
| Analitica | Ventas diarias, por categoria, top productos, dia de semana |
| Prediccion | Dias estimados de stock por producto con confianza |
| Reabastecimiento | Lista priorizada con inversion y ganancia potencial |
| Alertas | Criticos, advertencias, predicciones y oportunidades |
