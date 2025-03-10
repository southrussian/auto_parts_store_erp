from models import db
from flask import Flask, render_template, redirect, url_for, flash, session
import logging
from logging.handlers import RotatingFileHandler
from clients import view_clients, add_client, edit_client, delete_client
from users import login, logout, register, view_users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carparts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oxxxymiron'

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('carparts_app.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)

app.logger.info("Приложение Flask запущено.")


db.init_app(app)

login(app)
logout(app)
register(app)
view_users(app)

view_clients(app)
add_client(app)
edit_client(app)
delete_client(app)


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
