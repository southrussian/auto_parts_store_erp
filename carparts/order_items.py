from flask import render_template, redirect, url_for, flash, request, session
from models import OrderItem, db, Product, Order


def setup_order_items_routes(app):
    @app.route('/view_order_items/<int:order_id>')
    def view_order_items(order_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        sort_order = request.args.get('sort', 'asc')

        # Загружаем OrderItem вместе с связанным Product
        query = OrderItem.query.options(db.joinedload(OrderItem.product)).filter_by(order_id=order_id)

        if sort_order == 'asc':
            items = query.order_by(OrderItem.id.asc()).all()
        else:
            items = query.order_by(OrderItem.id.desc()).all()

        # Получаем список доступных товаров
        available_products = Product.query.all()

        return render_template(
            'view_order_items.html',
            items=items,
            sort_order=sort_order,
            order_id=order_id,
            available_products=available_products
        )

    @app.route('/add_order_item/<int:order_id>', methods=['GET', 'POST'])
    def add_order_item(order_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        products = Product.query.all()
        order = Order.query.get_or_404(order_id)  # Добавляем получение заказа

        if request.method == 'POST':
            product_id = request.form['product_id']
            quantity = request.form['quantity']
            price = request.form['price']

            item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                price=price
            )

            try:
                db.session.add(item)
                db.session.commit()
                order.update_total_price()  # Обновляем сумму заказа
                flash("Order item added successfully!", "success")
                return redirect(url_for('view_order_items', order_id=order_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_order_item.html', order_id=order_id, products=products)

    @app.route('/edit_order_item/<int:item_id>', methods=['GET', 'POST'])
    def edit_order_item(item_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        item = OrderItem.query.get_or_404(item_id)
        order = Order.query.get_or_404(item.order_id)  # Добавляем получение заказа

        if request.method == 'POST':
            item.product_id = request.form['product_id']
            item.quantity = request.form['quantity']
            item.price = request.form['price']

            try:
                db.session.commit()
                order.update_total_price()  # Обновляем сумму заказа
                flash("Order item updated successfully!", "success")
                return redirect(url_for('view_order_items', order_id=item.order_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_order_item.html', item=item)

    @app.route('/delete_order_item/<int:item_id>', methods=['POST'])
    def delete_order_item(item_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        item = OrderItem.query.get_or_404(item_id)
        order = Order.query.get_or_404(item.order_id)  # Добавляем получение заказа
        order_id = item.order_id
        try:
            db.session.delete(item)
            db.session.commit()
            flash("Order item deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_order_items', order_id=order_id))
