from flask import Flask
from config import Config
from .database import db
from .controllers import cliente_bp, cidade_bp, frete_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa o SQLAlchemy
    db.init_app(app)

    # Registra os blueprints
    app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
    app.register_blueprint(cidade_bp, url_prefix='/api/cidades')
    app.register_blueprint(frete_bp, url_prefix='/api/fretes')

    return app
