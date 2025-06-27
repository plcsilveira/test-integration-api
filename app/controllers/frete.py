from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.factory import create_frete_service  # Importa a factory
from app.schemas.frete import FreteCreateSchema, FreteSchema

frete_bp = Blueprint('frete', __name__)

# Usa a factory para criar a instância do serviço
frete_service = create_frete_service()

@frete_bp.route('/', methods=['POST'])
def criar_frete():
    try:
        # Pydantic validation
        data = FreteCreateSchema(**request.json)
        frete = frete_service.criar_frete(
            descricao=data.descricao,
            peso=data.peso,
            codigo_cliente=data.codigo_cliente,
            codigo_cidade=data.codigo_cidade
        )
        return jsonify(FreteSchema.from_orm(frete).dict()), 201
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@frete_bp.route('/maior-valor', methods=['GET'])
def get_frete_maior_valor():
    frete = frete_service.frete_maior_valor()
    if frete:
        return jsonify(FreteSchema.from_orm(frete).dict())
    return jsonify({'message': 'Nenhum frete encontrado'}), 404

@frete_bp.route('/cidade-mais-fretes', methods=['GET'])
def get_cidade_com_mais_fretes():
    resultado = frete_service.cidade_com_mais_fretes()
    if resultado:
        codigo_cidade, total_fretes = resultado
        return jsonify({'codigo_cidade': codigo_cidade, 'total_fretes': total_fretes})
    return jsonify({'message': 'Nenhum frete encontrado'}), 404
