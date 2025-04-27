from flask import render_template, redirect, url_for, flash, request, session
from models import Product, db, Order, OrderItem, WarehouseSection
from datetime import datetime
from search_utils import generate_embedding


def setup_products_routes(app):
    @app.route('/view_products')
    def view_products():
        if 'id' not in session:
            return redirect(url_for('login'))

        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            products = Product.query.order_by(Product.name.asc()).all()
        else:
            products = Product.query.order_by(Product.name.desc()).all()

        # Получаем активные заказы (например, со статусом "Pending")
        active_orders = Order.query.filter(
            Order.status.in_(['Активный'])
        ).all()

        return render_template(
            'view_products.html',
            products=products,
            sort_order=sort_order,
            active_orders=active_orders
        )

    @app.route('/add_product', methods=['GET', 'POST'])
    def add_product():
        if 'id' not in session:
            return redirect(url_for('login'))

        sections = WarehouseSection.query.all()

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            category = request.form['category']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            supplier_id = request.form.get('supplier_id')
            warehouse_section_id = int(request.form['warehouse_section_id'])

            product = Product(
                name=name,
                description=description,
                category=category,
                price=price,
                stock=stock,
                supplier_id=supplier_id if supplier_id else None,
                warehouse_section_id=warehouse_section_id,
                created_at=datetime.now(),
                embedding=generate_embedding(f"{name} {description} {category}")
            )

            try:
                db.session.add(product)
                db.session.commit()
                flash("Product added successfully!", "success")
                return redirect(url_for('view_products'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_product.html', sections=sections)

    @app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
    def edit_product(product_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        product = Product.query.get_or_404(product_id)
        sections = WarehouseSection.query.all()

        if request.method == 'POST':
            product.name = request.form['name']
            product.category = request.form['category']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.stock = int(request.form['stock'])
            product.supplier_id = request.form.get('supplier_id')
            product.warehouse_section_id = int(request.form['warehouse_section_id'])
            product.embedding = generate_embedding(f"{product.name} {product.description} {product.category}")

            try:
                db.session.commit()
                flash("Product updated successfully!", "success")
                return redirect(url_for('view_products'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_product.html', product=product, sections=sections)

    @app.route('/delete_product/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        product = Product.query.get_or_404(product_id)
        try:
            db.session.delete(product)
            db.session.commit()
            flash("Product deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_products'))

    @app.route('/search_products', methods=['GET', 'POST'])
    def search_products():
        if 'id' not in session:
            return redirect(url_for('login'))

        results = []
        if request.method == 'POST':
            search_query = request.form['search_query']
            all_products = Product.query.all()
            from search_utils import find_similar_products
            results = find_similar_products(search_query, all_products)

        return render_template('search_products.html', results=results)

    @app.route('/add_to_order', methods=['POST'])
    def add_to_order():
        if 'id' not in session:
            return redirect(url_for('login'))

        try:
            # Проверяем наличие order_id в запросе
            if 'order_id' not in request.form or not request.form['order_id']:
                flash("Не выбран заказ", "danger")
                return redirect(url_for('view_products'))

            order_id = request.form['order_id']
            product_ids = request.form.getlist('product_ids')

            # Проверяем, что выбраны товары
            if not product_ids:
                flash("Не выбрано ни одного товара", "danger")
                return redirect(url_for('view_products'))

            order = Order.query.get(order_id)
            if not order:
                flash("Заказ не найден", "danger")
                return redirect(url_for('view_products'))

            added_products = False

            for product_id in product_ids:
                quantity = int(request.form.get(f'quantity_{product_id}', 1))
                product = Product.query.get(product_id)

                if not product:
                    flash(f"Товар с ID {product_id} не найден", "danger")
                    continue

                if quantity <= 0:
                    flash(f"Некорректное количество для товара {product.name}", "danger")
                    continue

                # Проверяем наличие товара на складе
                if product.stock < quantity:
                    flash(f"Недостаточно товара {product.name} на складе (доступно: {product.stock})", "danger")
                    continue

                # Проверяем, есть ли уже такой товар в заказе
                existing_item = OrderItem.query.filter_by(
                    order_id=order_id,
                    product_id=product_id
                ).first()

                if existing_item:
                    existing_item.quantity += quantity
                else:
                    new_item = OrderItem(
                        order_id=order_id,
                        product_id=product_id,
                        quantity=quantity,
                        price=product.price
                    )
                    db.session.add(new_item)

                added_products = True

            if added_products:
                # Обновляем общую сумму заказа
                order.total_price = sum(
                    item.quantity * item.price
                    for item in order.order_items
                )
                db.session.commit()
                flash("Товары успешно добавлены в заказ", "success")
            else:
                flash("Не удалось добавить ни одного товара в заказ", "warning")

        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при добавлении товаров в заказ: {str(e)}", "danger")

        return redirect(url_for('view_products'))
