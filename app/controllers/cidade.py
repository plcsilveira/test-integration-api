from flask import Blueprint, request, jsonify
from app.services import CidadeService
from app.repository import CidadeRepository
from app.schemas import CidadeSchema

cidade_bp = Blueprint('cidade', __name__)
repository = CidadeRepository()
service = CidadeService(repository)

@cidade_bp.route('/', methods=['POST'])
def criar_cidade():
    try:
        data = CidadeSchema(**request.json)
        cidade = service.criar_cidade(
            nome=data.nome,
            uf=data.uf,
            taxa=data.taxa
        )
        return jsonify(CidadeSchema.from_orm(cidade).dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@cidade_bp.route('/busca/<nome>')
def buscar_por_nome(nome):
    cidade = service.buscar_por_nome(nome)
    if not cidade:
        return jsonify({'error': 'Cidade não encontrada'}), 404
    return jsonify(CidadeSchema.from_orm(cidade).dict())
