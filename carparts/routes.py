from flask import Blueprint, request, jsonify
from models import db, User, Warehouse, WarehouseSection, Product, InventoryLog, Client, Order, OrderItem, Supplier

main = Blueprint('main', __name__)


# User CRUD
@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201


@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])


@main.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})


@main.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})


@main.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})


# Warehouse CRUD
@main.route('/warehouses', methods=['POST'])
def create_warehouse():
    data = request.get_json()
    new_warehouse = Warehouse(name=data['name'], location=data['location'])
    db.session.add(new_warehouse)
    db.session.commit()
    return jsonify({'message': 'Warehouse created successfully!'}), 201


@main.route('/warehouses', methods=['GET'])
def get_warehouses():
    warehouses = Warehouse.query.all()
    return jsonify([{'id': w.id, 'name': w.name, 'location': w.location} for w in warehouses])


@main.route('/warehouses/<int:id>', methods=['GET'])
def get_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    return jsonify({'id': warehouse.id, 'name': warehouse.name, 'location': warehouse.location})


@main.route('/warehouses/<int:id>', methods=['PUT'])
def update_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    data = request.get_json()
    warehouse.name = data['name']
    warehouse.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Warehouse updated successfully!'})


@main.route('/warehouses/<int:id>', methods=['DELETE'])
def delete_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    db.session.delete(warehouse)
    db.session.commit()
    return jsonify({'message': 'Warehouse deleted successfully!'})


# WarehouseSection CRUD
@main.route('/warehouse_sections', methods=['POST'])
def create_warehouse_section():
    data = request.get_json()
    new_section = WarehouseSection(warehouse_id=data['warehouse_id'], name=data['name'], capacity=data['capacity'])
    db.session.add(new_section)
    db.session.commit()
    return jsonify({'message': 'Warehouse section created successfully!'}), 201


@main.route('/warehouse_sections', methods=['GET'])
def get_warehouse_sections():
    sections = WarehouseSection.query.all()
    return jsonify([{'id': s.id, 'warehouse_id': s.warehouse_id, 'name': s.name, 'capacity': s.capacity} for s in sections])


@main.route('/warehouse_sections/<int:id>', methods=['GET'])
def get_warehouse_section(id):
    section = WarehouseSection.query.get_or_404(id)
    return jsonify({'id': section.id, 'warehouse_id': section.warehouse_id, 'name': section.name, 'capacity': section.capacity})


@main.route('/warehouse_sections/<int:id>', methods=['PUT'])
def update_warehouse_section(id):
    section = WarehouseSection.query.get_or_404(id)
    data = request.get_json()
    section.name = data['name']
    section.capacity = data['capacity']
    db.session.commit()
    return jsonify({'message': 'Warehouse section updated successfully!'})


@main.route('/warehouse_sections/<int:id>', methods=['DELETE'])
def delete_warehouse_section(id):
    section = WarehouseSection.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({'message': 'Warehouse section deleted successfully!'})


# Product CRUD
@main.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], description=data.get('description'), price=data['price'], stock=data['stock'], supplier_id=data.get('supplier_id'), warehouse_section_id=data['warehouse_section_id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully!'}), 201


@main.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'stock': p.stock} for p in products])


@main.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock})
@main.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data['name']
    product.price = data['price']
    product.stock = data['stock']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully!'})


@main.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully!'})


# InventoryLog CRUD
@main.route('/inventory_logs', methods=['POST'])
def create_inventory_log():
    data = request.get_json()
    new_log = InventoryLog(product_id=data['product_id'], warehouse_id=data['warehouse_id'], section_id=data['section_id'], change_type=data['change_type'], quantity=data['quantity'], description=data.get('description'))
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Inventory log created successfully!'}), 201


@main.route('/inventory_logs', methods=['GET'])
def get_inventory_logs():
    logs = InventoryLog.query.all()
    return jsonify([{'id': l.id, 'product_id': l.product_id, 'change_type': l.change_type, 'quantity': l.quantity} for l in logs])


@main.route('/inventory_logs/<int:id>', methods=['GET'])
def get_inventory_log(id):
    log = InventoryLog.query.get_or_404(id)
    return jsonify({'id': log.id, 'product_id': log.product_id, 'change_type': log.change_type, 'quantity': log.quantity})


@main.route('/inventory_logs/<int:id>', methods=['PUT'])
def update_inventory_log(id):
    log = InventoryLog.query.get_or_404(id)
    data = request.get_json()
    log.change_type = data['change_type']
    log.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Inventory log updated successfully!'})


@main.route('/inventory_logs/<int:id>', methods=['DELETE'])
def delete_inventory_log(id):
    log = InventoryLog.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Inventory log deleted successfully!'})


# Client CRUD
@main.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    new_client = Client(name=data['name'], email=data['email'], phone=data['phone'], city=data['city'], address=data['address'])
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': 'Client created successfully!'}), 201


@main.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone} for c in clients])


@main.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    client = Client.query.get_or_404(id)
    return jsonify({'id': client.id, 'name': client.name, 'email': client.email, 'phone': client.phone})


@main.route('/clients/<int:id>', methods=['PUT'])
def update_client(id):
    client = Client.query.get_or_404(id)
    data = request.get_json()
    client.name = data['name']
    client.email = data['email']
    client.phone = data['phone']
    client.city = data['city']
    client.address = data['address']
    db.session.commit()
    return jsonify({'message': 'Client updated successfully!'})


@main.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted successfully!'})


# Order CRUD
@main.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    client = Client.query.get_or_404(data['client_id'])
    user = User.query.get_or_404(data['user_id'])
    order = Order(client_id=client.id, user_id=user.id, total_price=0.0)
    db.session.add(order)
    db.session.commit()

    for item in data['items']:
        product = Product.query.get_or_404(item['product_id'])
        if product.stock < item['quantity']:
            db.session.delete(order)
            db.session.commit()
            return jsonify({'message': f'Not enough stock for product: {product.name}'}), 400

        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item['quantity'], price=product.price)
        db.session.add(order_item)
        order.total_price += product.price * item['quantity']
        product.stock -= item['quantity']

        # Log inventory change
        inventory_log = InventoryLog(product_id=product.id, warehouse_id=product.section.warehouse_id, section_id=product.section.id, change_type='Sale', quantity=item['quantity'], description=f'Order {order.id}')
        db.session.add(inventory_log)

    db.session.commit()
    return jsonify({'message': 'Order created successfully!', 'order_id': order.id}), 201


# Business Logic: Pay for Order
@main.route('/orders/<int:id>/pay', methods=['POST'])
def pay_order(id):
    order = Order.query.get_or_404(id)
    if order.status != 'Pending':
        return jsonify({'message': 'Order is not in a pending state'}), 400

    order.status = 'Paid'
    db.session.commit()
    return jsonify({'message': 'Order paid successfully!'})


# Business Logic: Dispense Order Items
@main.route('/orders/<int:id>/dispense', methods=['POST'])
def dispense_order(id):
    order = Order.query.get_or_404(id)
    if order.status != 'Paid':
        return jsonify({'message': 'Order has not been paid yet'}), 400

    for item in order.order_items:
        product = Product.query.get(item.product_id)
        if product.stock < item.quantity:
            return jsonify({'message': f'Not enough stock for product: {product.name}'}), 400

        product.stock -= item.quantity

        # Log inventory change
        inventory_log = InventoryLog(product_id=product.id, warehouse_id=product.section.warehouse_id, section_id=product.section.id, change_type='Dispensed', quantity=item.quantity, description=f'Order {order.id} dispensed')
        db.session.add(inventory_log)

    order.status = 'Completed'
    db.session.commit()
    return jsonify({'message': 'Order items dispensed successfully!'})


@main.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'client_id': o.client_id, 'status': o.status, 'total_price': o.total_price} for o in orders])


@main.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({'id': order.id, 'client_id': order.client_id, 'status': order.status, 'total_price': order.total_price})


@main.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order updated successfully!'})


@main.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully!'})


# OrderItem CRUD
@main.route('/order_items', methods=['POST'])
def create_order_item():
    data = request.get_json()
    new_item = OrderItem(order_id=data['order_id'], product_id=data['product_id'], quantity=data['quantity'], price=data['price'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Order item created successfully!'}), 201


@main.route('/order_items', methods=['GET'])
def get_order_items():
    items = OrderItem.query.all()
    return jsonify([{'id': i.id, 'order_id': i.order_id, 'product_id': i.product_id, 'quantity': i.quantity} for i in items])


@main.route('/order_items/<int:id>', methods=['GET'])
def get_order_item(id):
    item = OrderItem.query.get_or_404(id)
    return jsonify({'id': item.id, 'order_id': item.order_id, 'product_id': item.product_id, 'quantity': item.quantity})


@main.route('/order_items/<int:id>', methods=['PUT'])
def update_order_item(id):
    item = OrderItem.query.get_or_404(id)
    data = request.get_json()
    item.quantity = data['quantity']
    item.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Order item updated successfully!'})


@main.route('/order_items/<int:id>', methods=['DELETE'])
def delete_order_item(id):
    item = OrderItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Order item deleted successfully!'})


# Supplier CRUD
@main.route('/suppliers', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = Supplier(name=data['name'], contact_info=data.get('contact_info'), city=data['city'])
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier created successfully!'}), 201


@main.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'city': s.city} for s in suppliers])


@main.route('/suppliers/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    return jsonify({'id': supplier.id, 'name': supplier.name, 'city': supplier.city})


@main.route('/suppliers/<int:id>', methods=['PUT'])
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    data = request.get_json()
    supplier.name = data['name']
    supplier.contact_info = data.get('contact_info')
    supplier.city = data['city']
    db.session.commit()
    return jsonify({'message': 'Supplier updated successfully!'})


@main.route('/suppliers/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully!'})
