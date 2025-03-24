from flask import render_template, redirect, url_for, flash, request, session
from models import Supplier, db
from datetime import datetime


def setup_suppliers_routes(app):
    @app.route('/view_suppliers')
    def view_suppliers():
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            suppliers = Supplier.query.order_by(Supplier.name.asc()).all()
        else:
            suppliers = Supplier.query.order_by(Supplier.name.desc()).all()
        return render_template('view_suppliers.html', suppliers=suppliers, sort_order=sort_order)

    @app.route('/add_supplier', methods=['GET', 'POST'])
    def add_supplier():
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            name = request.form['name']
            contact_info = request.form['contact_info']
            city = request.form['city']

            supplier = Supplier(
                name=name,
                contact_info=contact_info,
                city=city,
                created_at=datetime.now()
            )

            try:
                db.session.add(supplier)
                db.session.commit()
                flash("Supplier added successfully!", "success")
                return redirect(url_for('view_suppliers'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_supplier.html')

    @app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
    def edit_supplier(supplier_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        supplier = Supplier.query.get_or_404(supplier_id)

        if request.method == 'POST':
            supplier.name = request.form['name']
            supplier.contact_info = request.form['contact_info']
            supplier.city = request.form['city']

            try:
                db.session.commit()
                flash("Supplier updated successfully!", "success")
                return redirect(url_for('view_suppliers'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_supplier.html', supplier=supplier)

    @app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
    def delete_supplier(supplier_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        supplier = Supplier.query.get_or_404(supplier_id)
        try:
            db.session.delete(supplier)
            db.session.commit()
            flash("Supplier deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_suppliers'))
