from typing import List
from app.database import db
from app.models import Frete
from sqlalchemy import desc

class FreteRepository:
    def create(self, descricao: str, peso: float, valor: float, 
               codigo_cliente: int, codigo_cidade: int) -> Frete:
        frete = Frete(
            descricao=descricao,
            peso=peso,
            valor=valor,
            codigo_cliente=codigo_cliente,
            codigo_cidade=codigo_cidade
        )
        db.session.add(frete)
        db.session.commit()
        return frete
    
    def busca_por_cliente(self, codigo_cliente: int) -> List[Frete]:
        return Frete.query\
            .filter_by(codigo_cliente=codigo_cliente)\
            .order_by(desc(Frete.valor))\
            .all()
    
    def maior_valor(self) -> Frete:
        return Frete.query.order_by(desc(Frete.valor)).first()
