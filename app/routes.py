from flask import Blueprint, request, jsonify
from app.database import db
from app.models.cliente import Cliente
from app.models.cidade import Cidade
from app.models.frete import Frete

bp = Blueprint('api', __name__)

VALOR_FIXO = 10.0  # usado no cálculo do frete

# ---------------------------
# CLIENTES
# ---------------------------

@bp.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.get_json()
    try:
        cliente = Cliente(
            nome=data['nome'],
            telefone=data['telefone'],
            endereco=data['endereco']
        )
        db.session.add(cliente)
        db.session.commit()
        return jsonify({'id': cliente.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


# ---------------------------
# CIDADES
# ---------------------------

@bp.route('/cidades', methods=['POST'])
def add_cidade():
    data = request.get_json()
    try:
        cidade = Cidade(
            nome=data['nome'],
            estado=data['estado'],
            taxa_entrega=data['taxa_entrega']
        )
        db.session.add(cidade)
        db.session.commit()
        return jsonify({'id': cidade.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


# ---------------------------
# FRETES
# ---------------------------

@bp.route('/fretes', methods=['POST'])
def add_frete():
    data = request.get_json()
    cliente = Cliente.query.get(data['cliente_id'])
    cidade = Cidade.query.get(data['cidade_id'])

    if not cliente or not cidade:
        return jsonify({'erro': 'Cliente ou cidade não encontrados'}), 400

    valor = data['peso'] * VALOR_FIXO + cidade.taxa_entrega

    try:
        frete = Frete(
            codigo=data['codigo'],
            descricao=data['descricao'],
            peso=data['peso'],
            valor=valor,
            cliente_id=cliente.id,
            cidade_id=cidade.id
        )
        db.session.add(frete)
        db.session.commit()
        return jsonify({'id': frete.id, 'valor': valor}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


# ---------------------------
# CONSULTA FRETES POR CLIENTE
# ---------------------------

@bp.route('/fretes/cliente/<int:cliente_id>', methods=['GET'])
def fretes_por_cliente(cliente_id):
    fretes = Frete.query.filter_by(cliente_id=cliente_id).order_by(Frete.valor).all()
    return jsonify([
        {
            'id': f.id,
            'codigo': f.codigo,
            'descricao': f.descricao,
            'peso': f.peso,
            'valor': f.valor
        } for f in fretes
    ])