from flask import render_template, redirect, url_for, flash, request, session
from models import Order, db
from datetime import datetime


def view_orders(app):
    @app.route('/view_orders')
    def view_orders():
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')  # Default to ascending order
        if sort_order == 'asc':
            orders = Order.query.order_by(Order.created_at.asc()).all()
        else:
            orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('view_orders.html', orders=orders, sort_order=sort_order)


def add_order(app):
    @app.route('/add_order', methods=['GET', 'POST'])
    def add_order():
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            client_id = request.form['client_id']
            user_id = request.form['user_id']
            status = request.form.get('status', 'Pending')
            total_price = request.form['total_price']

            order = Order(
                client_id=client_id,
                user_id=user_id,
                status=status,
                total_price=total_price,
                created_at=datetime.utcnow()
            )

            try:
                db.session.add(order)
                db.session.commit()
                flash("Order added successfully!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_order.html')


def edit_order(app):
    @app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
    def edit_order(order_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        order = Order.query.get_or_404(order_id)

        if request.method == 'POST':
            order.client_id = request.form['client_id']
            order.user_id = request.form['user_id']
            order.status = request.form.get('status', 'Pending')
            order.total_price = request.form['total_price']

            try:
                db.session.commit()
                flash("Order updated successfully!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_order.html', order=order)


def delete_order(app):
    @app.route('/delete_order/<int:order_id>', methods=['POST'])
    def delete_order(order_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        order = Order.query.get_or_404(order_id)
        try:
            db.session.delete(order)
            db.session.commit()
            flash("Order deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_orders'))
