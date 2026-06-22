from flask import Flask
from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    with app.app_context():
        appbuilder.init_app(app, db.session)

        from .views.categoria_view import CategoriaView
        from .models.categoria import Categoria
        from .views.menu_view import MenuView
        from .models.menu import Menu
        from .views.cliente_view import ClienteView
        from .models.cliente import Cliente
        from .views.venta_view import VentaView
        from .models.venta import Venta
        from .views.detalle_venta_view import DetalleVentaView
        from .models.detalle_venta import DetalleVenta
        from .views.ticket_view import TicketView
        from .models.ticket import Ticket

        db.create_all()

        appbuilder.add_view(CategoriaView, "Categorias", icon="fa-folder-open-o", category="Catálogos")
        appbuilder.add_view(MenuView, "Menus", icon="fa-cutlery", category="Catálogos")
        appbuilder.add_view(ClienteView, "Clientes", icon="fa-user", category="Ventas")
        appbuilder.add_view(VentaView, "Ventas", icon="fa-shopping-cart", category="Ventas")
        appbuilder.add_view(DetalleVentaView, "Detalle de Ventas", icon="fa-list", category="Ventas")
        appbuilder.add_view(TicketView, "Tickets", icon="fa-ticket", category="Ventas")
    return app