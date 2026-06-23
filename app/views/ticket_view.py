from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.ticket import Ticket


class TicketView(ModelView):
    datamodel = SQLAInterface(Ticket)

    list_columns = ['id', 'fecha_emision', 'venta', 'cliente', 'total', 'cambio']
    add_columns = ['venta', 'cliente', 'numero_pedido', 'descuento', 'total', 'efectivo_recibido', 'cambio']
    edit_columns = ['venta', 'cliente', 'numero_pedido', 'descuento', 'total', 'efectivo_recibido', 'cambio']
    show_columns = ['fecha_emision', 'venta', 'cliente', 'numero_pedido', 'descuento', 'total', 'efectivo_recibido', 'cambio', 'emitido_por']

    def pre_add(self, item):
        from flask_login import current_user
        item.emitido_por = current_user.id