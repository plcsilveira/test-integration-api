import pytest
from sqlalchemy.exc import IntegrityError

from app.models.cliente import Cliente
from app.models.cidade import Cidade
from app.models.frete import Frete
from app.repository.frete import FreteRepository
from app.repository.cliente import ClienteRepository
from app.repository.cidade import CidadeRepository

def create_cliente_cidade(db):
    cliente_repo = ClienteRepository()
    cidade_repo = CidadeRepository()
    
    cliente = Cliente(nome="Frete Cliente", endereco="Rua Frete", telefone="999-8888")
    cidade = Cidade(nome="Cidade Frete", UF="CF", taxa=10.0)
    
    saved_cliente = cliente_repo.save(cliente)
    saved_cidade = cidade_repo.save(cidade)
    
    return saved_cliente, saved_cidade

def test_save_frete(db):
    repo = FreteRepository()
    cliente, cidade = create_cliente_cidade(db)
    
    frete = Frete(
        descricao="Caixa pequena",
        peso=1.5,
        valor=25.0,
        codigo_cliente=cliente.codigo_cliente,
        codigo_cidade=cidade.codigo_cidade
    )
    
    saved_frete = repo.save(frete)
    
    assert saved_frete.codigo_frete is not None
    assert saved_frete.descricao == "Caixa pequena"
    
    retrieved_frete = db.session.get(Frete, saved_frete.codigo_frete)
    assert retrieved_frete is not None
    assert retrieved_frete.codigo_cliente == cliente.codigo_cliente

def test_find_by_cliente_ordenado_por_valor(db):
    repo = FreteRepository()
    cliente, cidade = create_cliente_cidade(db)
    
    frete1 = Frete(descricao="F1", peso=1, valor=50.0, codigo_cliente=cliente.codigo_cliente, codigo_cidade=cidade.codigo_cidade)
    frete2 = Frete(descricao="F2", peso=2, valor=100.0, codigo_cliente=cliente.codigo_cliente, codigo_cidade=cidade.codigo_cidade)
    frete3 = Frete(descricao="F3", peso=3, valor=20.0, codigo_cliente=cliente.codigo_cliente, codigo_cidade=cidade.codigo_cidade)
    
    repo.save(frete1)
    repo.save(frete2)
    repo.save(frete3)
    
    fretes = repo.find_by_cliente_ordenado_por_valor(cliente)
    
    assert len(fretes) == 3
    assert fretes[0].valor == 100.0
    assert fretes[1].valor == 50.0
    assert fretes[2].valor == 20.0

def test_save_frete_raises_integrity_error_on_invalid_cliente(db):
    repo = FreteRepository()
    _, cidade = create_cliente_cidade(db)
    
    frete = Frete(
        descricao="Teste FK",
        peso=1.0,
        valor=1.0,
        codigo_cliente=999,
        codigo_cidade=cidade.codigo_cidade
    )
    
    with pytest.raises(IntegrityError):
        repo.save(frete)
        db.session.rollback()
