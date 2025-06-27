import pytest
from sqlalchemy.exc import IntegrityError

from app.models.cliente import Cliente
from app.repository.cliente import ClienteRepository


def test_save_cliente(db):
    repo = ClienteRepository()
    cliente = Cliente(
        nome="John Doe",
        endereco="123 Main St",
        telefone="555-1234"
    )
    
    saved_cliente = repo.save(cliente)
    
    assert saved_cliente.codigo_cliente is not None
    assert saved_cliente.nome == "John Doe"
    
    retrieved_cliente = db.session.get(Cliente, saved_cliente.codigo_cliente)
    assert retrieved_cliente is not None
    assert retrieved_cliente.nome == "John Doe"

def test_find_by_telefone(db):
    repo = ClienteRepository()
    cliente = Cliente(
        nome="Jane Doe",
        endereco="456 Oak Ave",
        telefone="555-5678"
    )
    repo.save(cliente)
    
    found_cliente = repo.find_by_telefone("555-5678")
    
    assert found_cliente is not None
    assert found_cliente.nome == "Jane Doe"
    assert found_cliente.telefone == "555-5678"

def test_find_by_telefone_not_found(db):
    repo = ClienteRepository()
    found_cliente = repo.find_by_telefone("000-0000")
    assert found_cliente is None

def test_save_cliente_raises_integrity_error_on_duplicate_telefone(db):
    repo = ClienteRepository()
    cliente1 = Cliente(nome="Test", endereco="Addr", telefone="111-2222")
    repo.save(cliente1)
    
    cliente2 = Cliente(nome="Test 2", endereco="Addr 2", telefone="111-2222")
    
    with pytest.raises(IntegrityError):
        repo.save(cliente2)
        db.session.rollback()

def test_save_cliente_raises_integrity_error_on_null_nome(db):
    repo = ClienteRepository()
    cliente = Cliente(nome=None, endereco="Addr", telefone="333-4444")
    
    with pytest.raises(IntegrityError):
        repo.save(cliente)
        db.session.rollback()
