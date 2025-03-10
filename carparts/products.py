from flask import render_template, redirect, url_for, flash, request, session
from models import Product, db
from datetime import datetime
from search_utils import generate_embedding


def view_products(app):
    @app.route('/view_products')
    def _view_products():
        if 'id' not in session:
            return redirect(url_for('login'))

        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            products = Product.query.order_by(Product.name.asc()).all()
        else:
            products = Product.query.order_by(Product.name.desc()).all()

        return render_template('view_products.html', products=products, sort_order=sort_order)


def add_product(app):
    @app.route('/add_product', methods=['GET', 'POST'])
    def _add_product():
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            stock = int(request.form['stock'])
            supplier_id = request.form.get('supplier_id')
            warehouse_section_id = int(request.form['warehouse_section_id'])

            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                supplier_id=supplier_id if supplier_id else None,
                warehouse_section_id=warehouse_section_id,
                created_at=datetime.now(),
                embedding=generate_embedding(f"{name} {description}")
            )

            try:
                db.session.add(product)
                db.session.commit()
                flash("Product added successfully!", "success")
                return redirect(url_for('_view_products'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_product.html')


def edit_product(app):
    @app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
    def _edit_product(product_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        product = Product.query.get_or_404(product_id)

        if request.method == 'POST':
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.stock = int(request.form['stock'])
            product.supplier_id = request.form.get('supplier_id')
            product.warehouse_section_id = int(request.form['warehouse_section_id'])
            product.embedding = generate_embedding(f"{product.name} {product.description}")

            try:
                db.session.commit()
                flash("Product updated successfully!", "success")
                return redirect(url_for('_view_products'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_product.html', product=product)


def delete_product(app):
    @app.route('/delete_product/<int:product_id>', methods=['POST'])
    def _delete_product(product_id):
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
        return redirect(url_for('_view_products'))


def search_products(app):
    @app.route('/search_products', methods=['GET', 'POST'])
    def _search_products():
        if 'id' not in session:
            return redirect(url_for('login'))

        results = []
        if request.method == 'POST':
            search_query = request.form['search_query']
            all_products = Product.query.all()
            from search_utils import find_similar_products
            results = find_similar_products(search_query, all_products)

        return render_template('search_products.html', results=results)
