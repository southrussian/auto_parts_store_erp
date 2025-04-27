from models import *
from flask import render_template, redirect, url_for, flash, request, session
import subprocess


def setup_user_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if User.query.filter_by(username=username).first():
                flash('Пользователь с таким именем или email уже существует.', 'danger')
                return redirect(url_for('register'))

            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['id'] = user.id
                notify('Вход', f"Пользователь {user.username} вошел в систему", 'Blow')
                flash('Вход выполнен успешно!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Неверное имя пользователя или пароль.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('id', None)
        flash('Вы вышли из системы.', 'info')
        return redirect(url_for('login'))

    @app.route('/view_users')
    def view_users():
        users = User.query.all()
        return render_template('view_users.html', users=users)


def notify(title, text, sound):
    command = '''
    on run argv 
        display notification (item 2 of argv) with title (item 1 of argv) sound name (item 3 of argv)
    end run
    '''

    subprocess.call(['osascript', '-e', command, title, text, sound])
