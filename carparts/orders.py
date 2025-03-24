from flask import render_template, redirect, url_for, flash, request, session
from models import *
from datetime import datetime


def setup_orders_routes(app):
    @app.route('/view_orders')
    def view_orders():
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            orders = Order.query.order_by(Order.created_at.asc()).all()
        else:
            orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('view_orders.html', orders=orders, sort_order=sort_order)

    @app.route('/add_order', methods=['GET', 'POST'])
    def _add_order():
        if 'id' not in session:
            return redirect(url_for('login'))

        users = User.query.all()
        clients = Client.query.all()

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
                created_at=datetime.now()
            )

            try:
                db.session.add(order)
                db.session.commit()
                flash("Order added successfully!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_order.html', clients=clients, users=users)

    @app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
    def _edit_order(order_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        order = Order.query.get_or_404(order_id)
        old_status = order.status

        if request.method == 'POST':
            order.client_id = request.form['client_id']
            order.user_id = request.form['user_id']
            new_status = request.form.get('status', 'Pending')
            order.status = new_status
            order.total_price = request.form['total_price']

            try:
                # Если статус изменился на Paid/Completed
                if new_status in ['Paid', 'Completed'] and old_status not in ['Paid', 'Completed']:
                    for item in order.order_items:
                        product = Product.query.get(item.product_id)

                        if product.stock < item.quantity:
                            raise Exception(
                                f"Недостаточно товара: {product.name}. "
                                f"Доступно: {product.stock}, Требуется: {item.quantity}"
                            )

                        # Списание товара
                        product.stock -= item.quantity

                        # Создаем запись в InventoryLog
                        log = InventoryLog(
                            product_id=product.id,
                            warehouse_id=product.section.warehouse_id,
                            section_id=product.warehouse_section_id,
                            change_type='out',
                            quantity=item.quantity,
                            description=f"Списание по заказу #{order.id} ({new_status})",
                            created_at=datetime.now()
                        )
                        db.session.add(log)

                db.session.commit()
                flash("Заказ успешно обновлен!", "success")
                return redirect(url_for('view_orders'))

            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка: {str(e)}", "danger")
                return redirect(url_for('_edit_order', order_id=order_id))

        # Для GET запроса
        clients = Client.query.all()
        users = User.query.all()
        return render_template(
            'edit_order.html',
            order=order,
            clients=clients,
            users=users,
            statuses=['Pending', 'Paid', 'Completed']
        )

    @app.route('/delete_order/<int:order_id>', methods=['POST'])
    def _delete_order(order_id):
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
