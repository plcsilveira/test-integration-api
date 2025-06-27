from app.database import db
from app.models.cidade import Cidade

class CidadeRepository:
    def save(self, cidade: Cidade) -> Cidade:
        db.session.add(cidade)
        db.session.commit()
        return cidade

    def find_by_nome(self, nome: str) -> Cidade | None:
        return Cidade.query.filter_by(nome=nome).first()

    def find_by_id(self, codigo_cidade: int) -> Cidade | None:
        return Cidade.query.get(codigo_cidade)
