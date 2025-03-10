from flask import render_template, redirect, url_for, flash, request, session
from models import InventoryLog, db
from datetime import datetime


def view_inventory_logs(app):
    @app.route('/view_inventory_logs/<int:product_id>')
    def _view_inventory_logs(product_id):
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            logs = InventoryLog.query.filter_by(product_id=product_id).order_by(InventoryLog.created_at.asc()).all()
        else:
            logs = InventoryLog.query.filter_by(product_id=product_id).order_by(InventoryLog.created_at.desc()).all()
        return render_template('view_inventory_logs.html', logs=logs, sort_order=sort_order, product_id=product_id)


def add_inventory_log(app):
    @app.route('/add_inventory_log/<int:product_id>', methods=['GET', 'POST'])
    def _add_inventory_log(product_id=None):
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            warehouse_id = request.form['warehouse_id']
            section_id = request.form['section_id']
            change_type = request.form['change_type']
            quantity = int(request.form['quantity'])
            description = request.form['description']

            log = InventoryLog(
                product_id=product_id,
                warehouse_id=warehouse_id,
                section_id=section_id,
                change_type=change_type,
                quantity=quantity,
                description=description,
                created_at=datetime.now()
            )

            try:
                db.session.add(log)
                db.session.commit()
                flash("Inventory log added successfully!", "success")
                return redirect(url_for('_view_inventory_logs', product_id=product_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_inventory_log.html', product_id=product_id)


def edit_inventory_log(app):
    @app.route('/edit_inventory_log/<int:log_id>', methods=['GET', 'POST'])
    def _edit_inventory_log(log_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        log = InventoryLog.query.get_or_404(log_id)

        if request.method == 'POST':
            log.warehouse_id = request.form['warehouse_id']
            log.section_id = request.form['section_id']
            log.change_type = request.form['change_type']
            log.quantity = int(request.form['quantity'])
            log.description = request.form['description']

            try:
                db.session.commit()
                flash("Inventory log updated successfully!", "success")
                return redirect(url_for('_view_inventory_logs', product_id=log.product_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_inventory_log.html', log=log)


def delete_inventory_log(app):
    @app.route('/delete_inventory_log/<int:log_id>', methods=['POST'])
    def _delete_inventory_log(log_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        log = InventoryLog.query.get_or_404(log_id)
        product_id = log.product_id
        try:
            db.session.delete(log)
            db.session.commit()
            flash("Inventory log deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('_view_inventory_logs', product_id=product_id))
