from flask import render_template, redirect, url_for, flash, request, session
from models import Client, db
from datetime import datetime


def view_clients(app):
    @app.route('/view_clients')
    def _view_clients():
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            clients = Client.query.order_by(Client.name.asc()).all()
        else:
            clients = Client.query.order_by(Client.name.desc()).all()
        return render_template('view_clients.html', clients=clients, sort_order=sort_order)


def add_client(app):
    @app.route('/add_client', methods=['GET', 'POST'])
    def _add_client():
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            city = request.form['city']
            address = request.form['address']

            client = Client(
                name=name,
                email=email,
                phone=phone,
                city=city,
                address=address,
                created_at=datetime.now()
            )

            try:
                db.session.add(client)
                db.session.commit()
                flash("Client added successfully!", "success")
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_client.html')


def edit_client(app):
    @app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
    def _edit_client(client_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        client = Client.query.get_or_404(client_id)

        if request.method == 'POST':
            client.name = request.form['name']
            client.email = request.form['email']
            client.phone = request.form['phone']
            client.city = request.form['city']
            client.address = request.form['address']

            try:
                db.session.commit()
                flash("Client updated successfully!", "success")
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_client.html', client=client)


def delete_client(app):
    @app.route('/delete_client/<int:client_id>', methods=['POST'])
    def _delete_client(client_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        client = Client.query.get_or_404(client_id)
        try:
            db.session.delete(client)
            db.session.commit()
            flash("Client deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_clients'))
