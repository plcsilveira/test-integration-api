from app.database import db
from app.models.cliente import Cliente
from app.models.cidade import Cidade
from app.models.frete import Frete
from sqlalchemy import func

VALOR_FIXO = 10.0

class FreteService:

    @staticmethod
    def cadastrar_frete(dados):
        cliente = Cliente.query.get(dados['cliente_id'])
        cidade = Cidade.query.get(dados['cidade_id'])

        if not cliente or not cidade:
            raise ValueError("Cliente ou cidade não encontrados")

        valor = dados['peso'] * VALOR_FIXO + cidade.taxa_entrega

        frete = Frete(
            codigo=dados['codigo'],
            descricao=dados['descricao'],
            peso=dados['peso'],
            valor=valor,
            cliente_id=cliente.id,
            cidade_id=cidade.id
        )

        db.session.add(frete)
        db.session.commit()

        return frete

    @staticmethod
    def maior_frete():
        return Frete.query.order_by(Frete.valor.desc()).first()

    @staticmethod
    def cidade_mais_fretes():
        result = db.session.query(
            Frete.cidade_id, func.count(Frete.id).label('qtd')
        ).group_by(Frete.cidade_id).order_by(func.count(Frete.id).desc()).first()

        if result:
            return Cidade.query.get(result.cidade_id)
        return None