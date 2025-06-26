from .models import db, Cliente

class ClienteRepository:
    def find_by_telefone(self, telefone: str) -> Cliente | None:
        return Cliente.query.filter_by(telefone=telefone).first()
    # ... resto dos repositórios