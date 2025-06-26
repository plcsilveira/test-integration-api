import pytest
from app.models import Cliente
from app.database import db

def test_cliente_model_campos_obrigatorios(test_app):
    """Testa se o modelo Cliente valida campos obrigatórios"""
    with test_app.app_context():
        cliente = Cliente(
            nome="João Silva",
            telefone="123456789",
            endereco="Rua X, 123"
        )
        db.session.add(cliente)
        db.session.commit()
        
        assert cliente.nome == "João Silva"
        assert cliente.telefone == "123456789"
        assert cliente.endereco == "Rua X, 123"
