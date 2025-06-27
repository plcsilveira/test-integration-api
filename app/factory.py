from flask import Flask
from config import Config
from .database import db

# Importações de repositórios e serviços
from .repository.frete import FreteRepository
from .repository.cliente import ClienteRepository
from .repository.cidade import CidadeRepository
from .services.frete import FreteService

def create_frete_service() -> FreteService:
    """Cria uma instância do FreteService com suas dependências."""
    frete_repo = FreteRepository()
    cliente_repo = ClienteRepository()
    cidade_repo = CidadeRepository()
    return FreteService(frete_repo=frete_repo, cliente_repo=cliente_repo, cidade_repo=cidade_repo)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa o SQLAlchemy
    db.init_app(app)

    # Importa e registra os blueprints para evitar importação circular
    from .controllers import cliente_bp, cidade_bp, frete_bp
    app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
    app.register_blueprint(cidade_bp, url_prefix='/api/cidades')
    app.register_blueprint(frete_bp, url_prefix='/api/fretes')

    return app
