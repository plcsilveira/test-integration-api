import pytest
from app.factory import create_frete_service
from app.models import Cliente, Cidade, Frete
from app.database import db

@pytest.fixture
def frete_service(test_app):
    """Fixture que retorna uma instância do FreteService com acesso ao app_context."""
    with test_app.app_context():
        yield create_frete_service()

@pytest.fixture
def setup_data(db):
    """Fixture para popular o banco de dados com dados de teste."""
    cliente1 = Cliente(nome="Cliente A", telefone="111", endereco="Rua A")
    cidade1 = Cidade(nome="Cidade X", UF="XX", taxa=10.0)
    cliente2 = Cliente(nome="Cliente B", telefone="222", endereco="Rua B")
    cidade2 = Cidade(nome="Cidade Y", UF="YY", taxa=20.0)
    db.session.add_all([cliente1, cidade1, cliente2, cidade2])
    db.session.commit()

    frete1 = Frete(descricao="Frete 1", peso=1.0, valor=20.0, codigo_cliente=cliente1.codigo_cliente, codigo_cidade=cidade1.codigo_cidade)
    frete2 = Frete(descricao="Frete 2", peso=2.0, valor=40.0, codigo_cliente=cliente1.codigo_cliente, codigo_cidade=cidade1.codigo_cidade) # Cidade 1 tem 2 fretes
    frete3 = Frete(descricao="Frete 3", peso=3.0, valor=90.0, codigo_cliente=cliente2.codigo_cliente, codigo_cidade=cidade2.codigo_cidade) # Maior valor
    db.session.add_all([frete1, frete2, frete3])
    db.session.commit()
    return cliente1, cidade1, cliente2, cidade2, frete3.codigo_frete

def test_criar_frete_sucesso(frete_service, db, setup_data):
    cliente1, cidade1, _, _, _ = setup_data
    novo_frete = frete_service.criar_frete(
        descricao="Novo Frete",
        peso=5.0,
        codigo_cliente=cliente1.codigo_cliente,
        codigo_cidade=cidade1.codigo_cidade
    )
    assert novo_frete.codigo_frete is not None
    assert novo_frete.valor == 60.0 # 5.0 * 10 + 10.0

def test_criar_frete_cliente_invalido(frete_service, db, setup_data):
    _, cidade1, _, _, _ = setup_data
    with pytest.raises(ValueError, match="Cliente não encontrado"):
        frete_service.criar_frete(
            descricao="Teste",
            peso=1.0,
            codigo_cliente=999,
            codigo_cidade=cidade1.codigo_cidade
        )

def test_frete_maior_valor(frete_service, db, setup_data):
    _, _, _, _, frete_maior_valor_id = setup_data
    frete = frete_service.frete_maior_valor()
    assert frete is not None
    assert frete.codigo_frete == frete_maior_valor_id

def test_cidade_com_mais_fretes(frete_service, db, setup_data):
    _, cidade1, _, _, _ = setup_data
    resultado = frete_service.cidade_com_mais_fretes()
    assert resultado is not None
    codigo_cidade, total_fretes = resultado
    assert codigo_cidade == cidade1.codigo_cidade
    assert total_fretes == 2
