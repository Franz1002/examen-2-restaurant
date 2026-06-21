from flask_appbuilder import ModelView
from app.models.menu import Menu  
from flask_appbuilder.models.sqla.interface import SQLAInterface

class MenuView(ModelView):
    datamodel = SQLAInterface(Menu)  
      
    list_columns = ['img','nombre', 'categoria.nombre', 'precio', 'detalle', 'estado']
    add_columns = ['nombre', 'categoria', 'precio', 'detalle', 'img', 'estado']
    edit_columns = ['nombre', 'categoria', 'precio', 'detalle', 'img', 'estado']
    show_columns = ['id', 'nombre', 'categoria', 'precio', 'detalle', 'img', 'estado']
    
    