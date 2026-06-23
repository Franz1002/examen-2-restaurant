from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.detalle_venta import DetalleVenta


class DetalleVentaView(ModelView):
    datamodel = SQLAInterface(DetalleVenta)

    list_columns = ['venta', 'menu.nombre', 'cantidad', 'subtotal']
    add_columns = ['venta', 'menu', 'cantidad', 'subtotal']
    edit_columns = ['venta', 'menu', 'cantidad', 'subtotal']
    show_columns = ['venta', 'menu', 'cantidad', 'subtotal']