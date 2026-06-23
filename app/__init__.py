from flask import Flask
from .extensions import appbuilder, db
from datetime import datetime
from sqlalchemy import func


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
        from .views.registrar_venta_view import RegistrarVentaView
        from .views.reportes_view import ReportesView

        db.create_all()

        appbuilder.add_view(CategoriaView, "Categorias", icon="fa-folder-open-o", category="Catálogos")
        appbuilder.add_view(MenuView, "Menus", icon="fa-cutlery", category="Catálogos")
        appbuilder.add_view(RegistrarVentaView, "Registrar Venta", icon="fa-cash-register", category="Compras y ventas", href="/registrar-venta/")
        appbuilder.add_view(ClienteView, "Clientes", icon="fa-user", category="Ventas")
        appbuilder.add_view(VentaView, "Ventas", icon="fa-shopping-cart", category="Ventas")
        appbuilder.add_view(DetalleVentaView, "Detalle Ventas", icon="fa-list", category="Ventas")
        appbuilder.add_view(TicketView, "Tickets", icon="fa-ticket", category="Ventas")
        appbuilder.add_view(ReportesView, "Productos Vendidos", icon="fa-bar-chart", category="Reportes", href="/reportes/productos-vendidos")
        appbuilder.add_link("Clientes y Compras", icon="fa-users", category="Reportes", href="/reportes/clientes-compras")
        appbuilder.add_link("Corte de Caja", icon="fa-calendar", category="Reportes", href="/reportes/ventas-por-fecha")

        from .security_setup import setup_roles_and_permissions
        setup_roles_and_permissions(appbuilder)

        @app.context_processor
        def inject_arqueo():
            from flask_login import current_user
            if current_user.is_authenticated:
                hoy = datetime.now().date()
                arqueo = db.session.query(
                    func.sum(Venta.total_venta).label('total_vendido'),
                    func.sum(Ticket.descuento).label('total_descuentos'),
                    func.sum(Ticket.efectivo_recibido).label('efectivo_recibido'),
                    func.sum(Ticket.cambio).label('cambio_entregado'),
                    func.count(Ticket.id).label('num_tickets')
                ).join(Ticket, Venta.id == Ticket.venta_id
                ).filter(func.date(Venta.fecha_venta) == hoy
                ).first()
                return dict(arqueo=arqueo)
            return dict(arqueo=None)

    return app