from app.database import db
from app.models.cliente import Cliente

class ClienteRepository:
    def save(self, cliente: Cliente) -> Cliente:
        db.session.add(cliente)
        db.session.commit()
        return cliente

    def find_by_telefone(self, telefone: str) -> Cliente | None:
        return Cliente.query.filter_by(telefone=telefone).first()

    def find_by_id(self, codigo_cliente: int) -> Cliente | None:
        return Cliente.query.get(codigo_cliente)
