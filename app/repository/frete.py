from typing import List
from app.database import db
from app.models import Frete, Cliente
from sqlalchemy import func

class FreteRepository:
    def save(self, frete: Frete) -> Frete:
        db.session.add(frete)
        db.session.commit()
        return frete

    def find_by_cliente_ordenado_por_valor(self, cliente: Cliente) -> list[Frete]:
        return Frete.query.filter_by(cliente=cliente).order_by(Frete.valor.desc()).all()

    def find_maior_valor(self) -> Frete | None:
        return Frete.query.order_by(Frete.valor.desc()).first()

    def find_cidade_com_mais_fretes(self):
        # Consulta para contar fretes por cidade e ordenar
        cidade_mais_fretes = db.session.query(Frete.codigo_cidade, func.count(Frete.codigo_frete).label('total_fretes')) \
            .group_by(Frete.codigo_cidade) \
            .order_by(func.count(Frete.codigo_frete).desc()) \
            .first()

        if cidade_mais_fretes:
            # Retorna o codigo_cidade e a contagem
            return cidade_mais_fretes.codigo_cidade, cidade_mais_fretes.total_fretes
        return None
