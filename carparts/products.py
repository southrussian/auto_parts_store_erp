from flask import render_template, redirect, url_for, flash, request, session
from models import Product, db
from datetime import datetime


def view_products(app):
    @app.route('/view_products/<int:section_id>')
    def view_products(section_id):
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')  # Default to ascending order
        if sort_order == 'asc':
            products = Product.query.filter_by(warehouse_section_id=section_id).order_by(Product.name.asc()).all()
        else:
            products = Product.query.filter_by(warehouse_section_id=section_id).order_by(Product.name.desc()).all()
        return render_template('view_products.html', products=products, sort_order=sort_order, section_id=section_id)


def add_product(app):
    @app.route('/add_product/<int:section_id>', methods=['GET', 'POST'])
    def add_product(section_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            stock = request.form['stock']
            supplier_id = request.form.get('supplier_id')  # Supplier ID is optional

            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                supplier_id=supplier_id,
                warehouse_section_id=section_id,
                created_at=datetime.utcnow()
            )

            try:
                db.session.add(product)
                db.session.commit()
                flash("Product added successfully!", "success")
                return redirect(url_for('view_products', section_id=section_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_product.html', section_id=section_id)


def edit_product(app):
    @app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
    def edit_product(product_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        product = Product.query.get_or_404(product_id)

        if request.method == 'POST':
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = request.form['price']
            product.stock = request.form['stock']
            product.supplier_id = request.form.get('supplier_id')  # Supplier ID is optional

            try:
                db.session.commit()
                flash("Product updated successfully!", "success")
                return redirect(url_for('view_products', section_id=product.warehouse_section_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_product.html', product=product)


def delete_product(app):
    @app.route('/delete_product/<int:product_id>', methods=['POST'])
    def delete_product(product_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        product = Product.query.get_or_404(product_id)
        section_id = product.warehouse_section_id
        try:
            db.session.delete(product)
            db.session.commit()
            flash("Product deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_products', section_id=section_id))
