from flask import Flask, render_template
from database import init_db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ferreteria-2024-key')

with app.app_context():
    init_db()

from routes.inventory import bp as inv_bp
from routes.sales import bp as sales_bp
from routes.analytics import bp as analytics_bp
from routes.alerts import bp as alerts_bp

app.register_blueprint(inv_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(alerts_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    return render_template('inventario.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/alertas')
def alertas():
    return render_template('alertas.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
