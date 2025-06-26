import pytest
from app.repository import ClienteRepository
from app.models import Cliente
from app.database import db

def test_cliente_repository_busca_por_telefone(test_app):
    """Testa o método de busca por telefone do repositório de Cliente"""
    with test_app.app_context():
        # Arrange
        repository = ClienteRepository()
        cliente = Cliente(
            nome="João Silva",
            telefone="987654321",
            endereco="Rua Y, 456"
        )
        db.session.add(cliente)
        db.session.commit()
        
        # Act
        cliente_encontrado = repository.busca_por_telefone("987654321")
        
        # Assert
        assert cliente_encontrado is not None
        assert cliente_encontrado.nome == "João Silva"
