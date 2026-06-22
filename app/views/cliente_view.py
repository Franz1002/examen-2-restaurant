from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.cliente import Cliente


class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    list_columns = ['nombre', 'documento', 'celular', 'fecha_registro']
    add_columns = ['nombre', 'documento', 'celular']
    edit_columns = ['nombre', 'documento', 'celular']
    show_columns = ['id', 'nombre', 'documento', 'celular', 'fecha_registro']