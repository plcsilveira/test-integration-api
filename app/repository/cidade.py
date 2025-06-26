from app.database import db
from app.models import Cidade

class CidadeRepository:
    def create(self, nome: str, uf: str, taxa: float) -> Cidade:
        cidade = Cidade(
            nome=nome,
            uf=uf,
            taxa=taxa
        )
        db.session.add(cidade)
        db.session.commit()
        return cidade
    
    def busca_por_nome(self, nome: str) -> Cidade:
        return Cidade.query.filter_by(nome=nome).first()
