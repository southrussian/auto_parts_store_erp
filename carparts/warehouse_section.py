from flask import render_template, redirect, url_for, flash, request, session
from models import WarehouseSection, db
from datetime import datetime


def setup_warehouse_sections_routes(app):
    @app.route('/view_warehouse_sections/<int:warehouse_id>')
    def view_warehouse_sections(warehouse_id):
        if 'id' not in session:
            return redirect(url_for('login'))
        sort_order = request.args.get('sort', 'asc')
        if sort_order == 'asc':
            sections = (WarehouseSection.query.filter_by(warehouse_id=warehouse_id).
                        order_by(WarehouseSection.name.asc()).all())
        else:
            sections = (WarehouseSection.query.filter_by(warehouse_id=warehouse_id).
                        order_by(WarehouseSection.name.desc()).all())
        return render_template('view_warehouse_sections.html', sections=sections,
                               sort_order=sort_order, warehouse_id=warehouse_id)

    @app.route('/add_warehouse_section/<int:warehouse_id>', methods=['GET', 'POST'])
    def add_warehouse_section(warehouse_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            name = request.form['name']
            capacity = request.form['capacity']

            section = WarehouseSection(
                warehouse_id=warehouse_id,
                name=name,
                capacity=capacity,
                created_at=datetime.now()
            )

            try:
                db.session.add(section)
                db.session.commit()
                flash("Warehouse section added successfully!", "success")
                return redirect(url_for('view_warehouse_sections', warehouse_id=warehouse_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_warehouse_section.html', warehouse_id=warehouse_id)

    @app.route('/edit_warehouse_section/<int:section_id>', methods=['GET', 'POST'])
    def edit_warehouse_section(section_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        section = WarehouseSection.query.get_or_404(section_id)

        if request.method == 'POST':
            section.name = request.form['name']
            section.capacity = request.form['capacity']

            try:
                db.session.commit()
                flash("Warehouse section updated successfully!", "success")
                return redirect(url_for('view_warehouse_sections', warehouse_id=section.warehouse_id))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_warehouse_section.html', section=section)

    @app.route('/delete_warehouse_section/<int:section_id>', methods=['POST'])
    def delete_warehouse_section(section_id):
        if 'id' not in session:
            return redirect(url_for('login'))

        section = WarehouseSection.query.get_or_404(section_id)
        warehouse_id = section.warehouse_id
        try:
            db.session.delete(section)
            db.session.commit()
            flash("Warehouse section deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_warehouse_sections', warehouse_id=warehouse_id))
