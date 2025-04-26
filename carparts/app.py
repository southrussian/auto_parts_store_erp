from models import *
import os
from flask import Flask, render_template, redirect, url_for, flash, session
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from routes import setup_routes
from flask_migrate import Migrate
from sqlalchemy import extract

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carparts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('carparts_app.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)

app.logger.info("Приложение Flask запущено.")


db.init_app(app)
migrate = Migrate(app, db)
setup_routes(app)


@app.route('/')
def dashboard():
    if 'id' not in session:
        flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))
    app.logger.info(f"Доступ к панели управления пользователем ID: {session['id']}.")

    clients_count = Client.query.count()
    products_count = Product.query.count()
    logs_count = InventoryLog.query.count()

    current_month = datetime.now().month
    monthly_sales = Order.query.filter(extract('month', Order.created_at) == current_month).count()

    return render_template('dashboard.html', clients_count=clients_count, products_count=products_count,
                           monthly_sales=monthly_sales, logs_count=logs_count)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=6006)
