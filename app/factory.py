from flask import Flask
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa o SQLAlchemy com a configuração da nossa aplicação
    db.init_app(app)

    # Importar e registrar as rotas da API aqui no futuro
    # from .routes import main_bp
    # app.register_blueprint(main_bp)

    return app
