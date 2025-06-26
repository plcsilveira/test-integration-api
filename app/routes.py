from flask import Blueprint, request, jsonify
from .schemas import ClienteSchema
from pydantic import ValidationError

main_bp = Blueprint('main', __name__)

@main_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    try:
        # Valida os dados de entrada com o schema
        dados_cliente = ClienteSchema(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    # ... chama o serviço para criar o cliente ...
    return jsonify({"message": "Cliente criado com sucesso"}), 201