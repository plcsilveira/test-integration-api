from flask import Blueprint, request, jsonify
from app.services import FreteService
from app.repository import FreteRepository
from app.schemas import FreteCreateSchema, FreteSchema

frete_bp = Blueprint('frete', __name__)
repository = FreteRepository()
service = FreteService(repository)

@frete_bp.route('/', methods=['POST'])
def criar_frete():
    try:
        data = FreteCreateSchema(**request.json)
        frete = service.criar_frete(
            descricao=data.descricao,
            peso=data.peso,
            codigo_cliente=data.codigo_cliente,
            codigo_cidade=data.codigo_cidade
        )
        return jsonify(FreteSchema.from_orm(frete).dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@frete_bp.route('/cliente/<int:codigo_cliente>')
def listar_fretes_cliente(codigo_cliente):
    fretes = service.buscar_por_cliente(codigo_cliente)
    return jsonify([FreteSchema.from_orm(f).dict() for f in fretes])
