from models import db
import os
from flask import Flask, render_template, redirect, url_for, flash, session
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from clients import view_clients, add_client, edit_client, delete_client
from users import login, logout, register, view_users
from orders import view_orders, edit_order, add_order, delete_order
from products import view_products, add_product, edit_product, delete_product, search_products
from suppliers import view_suppliers, add_supplier, edit_supplier, delete_supplier
from warehouse_section import (view_warehouse_sections, add_warehouse_section, edit_warehouse_section,
                               delete_warehouse_section)
from flask_migrate import Migrate

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

login(app)
logout(app)
register(app)
view_users(app)

view_clients(app)
add_client(app)
edit_client(app)
delete_client(app)

view_orders(app)
add_order(app)
edit_order(app)
delete_order(app)

view_products(app)
add_product(app)
edit_product(app)
delete_product(app)
search_products(app)

view_suppliers(app)
add_supplier(app)
edit_supplier(app)
delete_supplier(app)

view_warehouse_sections(app)
add_warehouse_section(app)
edit_warehouse_section(app)
delete_warehouse_section(app)


@app.route('/')
def dashboard():
    if 'id' not in session:
        flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))
    app.logger.info(f"Доступ к панели управления пользователем ID: {session['id']}.")
    return render_template('dashboard.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
