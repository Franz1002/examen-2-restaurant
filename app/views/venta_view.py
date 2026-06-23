from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_login import current_user
from app.models.venta import Venta


class VentaView(ModelView):
    datamodel = SQLAInterface(Venta)

    list_columns = ['id', 'fecha_venta', 'usuario_id', 'total_venta']
    add_columns = ['total_venta']
    edit_columns = ['total_venta']
    show_columns = ['id', 'fecha_venta', 'usuario_id', 'total_venta']

    def pre_add(self, item):
        item.usuario_id = current_user.id