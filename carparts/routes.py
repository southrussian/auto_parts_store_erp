from clients import setup_clients_routes
from users import setup_user_routes
from orders import setup_orders_routes
from products import setup_products_routes
from suppliers import setup_suppliers_routes
from warehouse_section import setup_warehouse_sections_routes
from warehouses import setup_warehouses_routes
from order_items import setup_order_items_routes
from inventory_logs import setup_inventory_logs_routes
from gigachat_ask import setup_gigachat_routes


def setup_routes(app):
    setup_user_routes(app)
    setup_clients_routes(app)
    setup_orders_routes(app)
    setup_products_routes(app)
    setup_suppliers_routes(app)
    setup_warehouse_sections_routes(app)
    setup_warehouses_routes(app)
    setup_order_items_routes(app)
    setup_inventory_logs_routes(app)
    setup_gigachat_routes(app)
