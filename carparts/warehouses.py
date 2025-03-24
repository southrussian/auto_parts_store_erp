from flask import render_template, redirect, url_for, flash, request, session
from models import Warehouse, db
from datetime import datetime


def view_warehouses(app):
    @app.route('/view_warehouses')
    def _view_warehouses():
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            warehouses = Warehouse.query.order_by(Warehouse.name.asc()).all()
        else:
            warehouses = Warehouse.query.order_by(Warehouse.name.desc()).all()
        return render_template('view_warehouses.html', warehouses=warehouses, sort_order=sort_order)


def add_warehouse(app):
    @app.route('/add_warehouse', methods=['GET', 'POST'])
    def _add_warehouse():
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            name = request.form['name']
            location = request.form['location']

            warehouse = Warehouse(
                name=name,
                location=location,
                created_at=datetime.now()
            )

            try:
                db.session.add(warehouse)
                db.session.commit()
                flash("Warehouse added successfully!", "success")
                return redirect(url_for('view_warehouses'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_warehouse.html')


def edit_warehouse(app):
    @app.route('/edit_warehouse/<int:warehouse_id>', methods=['GET', 'POST'])
    def _edit_warehouse(warehouse_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        warehouse = Warehouse.query.get_or_404(warehouse_id)

        if request.method == 'POST':
            warehouse.name = request.form['name']
            warehouse.location = request.form['location']

            try:
                db.session.commit()
                flash("Warehouse updated successfully!", "success")
                return redirect(url_for('view_warehouses'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_warehouse.html', warehouse=warehouse)


def delete_warehouse(app):
    @app.route('/delete_warehouse/<int:warehouse_id>', methods=['POST'])
    def _delete_warehouse(warehouse_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        warehouse = Warehouse.query.get_or_404(warehouse_id)
        try:
            db.session.delete(warehouse)
            db.session.commit()
            flash("Warehouse deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_warehouses'))
