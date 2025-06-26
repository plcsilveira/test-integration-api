from flask import Blueprint, request, jsonify
from app.services import ClienteService
from app.repository import ClienteRepository
from app.schemas import ClienteSchema

cliente_bp = Blueprint('cliente', __name__)
repository = ClienteRepository()
service = ClienteService(repository)

@cliente_bp.route('/', methods=['POST'])
def criar_cliente():
    try:
        data = ClienteSchema(**request.json)
        cliente = service.criar_cliente(
            nome=data.nome,
            endereco=data.endereco,
            telefone=data.telefone
        )
        return jsonify(ClienteSchema.from_orm(cliente).dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@cliente_bp.route('/busca/<telefone>')
def buscar_por_telefone(telefone):
    cliente = service.buscar_por_telefone(telefone)
    if not cliente:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    return jsonify(ClienteSchema.from_orm(cliente).dict())
