from flask import Flask
from config import Config
from .models import db
from .routes import main_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)

    # Registra os blueprints (rotas da API)
    app.register_blueprint(main_bp)

    return app