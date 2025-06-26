from flask import Blueprint
from .cliente import cliente_bp
from .cidade import cidade_bp
from .frete import frete_bp

# Cria um blueprint principal para agrupar todos os outros
api_bp = Blueprint('api', __name__)

# Registra os blueprints das entidades
api_bp.register_blueprint(cliente_bp, url_prefix='/clientes')
api_bp.register_blueprint(cidade_bp, url_prefix='/cidades')
api_bp.register_blueprint(frete_bp, url_prefix='/fretes')
