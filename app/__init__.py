from flask import Flask
from .extensions import appbuilder, db
<<<<<<< Updated upstream
=======
from .views.categoria_view import CategoriaView
from .models.categoria import Categoria
from .views.menu_view import MenuView
from .models.menu import Menu
from .views.cliente_view import ClienteView
from .models.cliente import Cliente
>>>>>>> Stashed changes


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    with app.app_context():
        appbuilder.init_app(app, db.session)
        
        db.create_all()
<<<<<<< Updated upstream
=======
        
        appbuilder.add_view(CategoriaView, "Categorias", icon="fa-folder-open-o", category="Catálogos")
        appbuilder.add_view(MenuView, "Menus", icon="fa-cutlery", category="Catálogos")
        appbuilder.add_view(ClienteView, "Clientes", icon="fa-user", category="Ventas")
>>>>>>> Stashed changes
     
    return app
