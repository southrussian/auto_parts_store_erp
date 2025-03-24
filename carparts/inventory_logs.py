from flask import render_template, redirect, url_for, flash, request, session
from models import InventoryLog, db


def register_inventory_logs_routes(app):
    @app.route('/view_inventory_logs')
    def view_inventory_logs():
        """Просмотр всех журнальных записей инвентаря"""
        if 'id' not in session:
            return redirect(url_for('login'))

        sort_order = request.args.get('sort', 'asc')
        logs_query = InventoryLog.query.options(
            db.joinedload(InventoryLog.product),
            db.joinedload(InventoryLog.warehouse),
            db.joinedload(InventoryLog.section)
        )

        logs = logs_query.order_by(
            InventoryLog.created_at.asc() if sort_order == 'asc'
            else InventoryLog.created_at.desc()
        ).all()

        return render_template('view_inventory_logs.html',
                               logs=logs,
                               sort_order=sort_order)

    @app.route('/inventory_logs/delete/<int:log_id>', methods=['POST'])
    def delete_inventory_log(log_id):
        """Удаление записи из журнала инвентаря"""
        if 'id' not in session:
            return redirect(url_for('login'))

        log = InventoryLog.query.get_or_404(log_id)
        product_id = log.product_id

        try:
            db.session.delete(log)
            db.session.commit()
            flash("Запись успешно удалена!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка: {str(e)}", "danger")

        return redirect(url_for('view_product_inventory_logs',
                                product_id=product_id))
