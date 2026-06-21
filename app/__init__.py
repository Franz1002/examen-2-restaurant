from flask import Flask
from .extensions import appbuilder, db
from .views.categoria_view import CategoriaView
from .models.categoria import Categoria


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    with app.app_context():
        appbuilder.init_app(app, db.session)
        
        db.create_all()
        
        appbuilder.add_view(CategoriaView, "Categorias", icon="fa-folder-open-o", category="Catálogos")
     
    return app