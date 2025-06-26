from app.database import db
from app.models import Cliente

class ClienteRepository:
    def create(self, nome: str, endereco: str, telefone: str) -> Cliente:
        cliente = Cliente(
            nome=nome,
            endereco=endereco,
            telefone=telefone
        )
        db.session.add(cliente)
        db.session.commit()
        return cliente
    
    def busca_por_telefone(self, telefone: str) -> Cliente:
        return Cliente.query.filter_by(telefone=telefone).first()
