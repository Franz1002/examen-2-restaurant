from flask_appbuilder import ModelView
from app.models.categoria import Categoria   
from flask_appbuilder.models.sqla.interface import SQLAInterface

class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)  
      
    list_columns = ['nombre', 'descripcion']
    add_columns = ['nombre', 'descripcion']
    edit_columns = ['nombre', 'descripcion']
    show_columns = ['id','nombre', 'descripcion']
