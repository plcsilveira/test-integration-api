import pytest
from app.models import Cliente, Cidade
from app.repository import FreteRepository
from app.services.frete import FreteService
from app.database import db

def test_calcular_valor_frete():
    """Testa o cálculo do valor do frete"""
    repository = FreteRepository()
    service = FreteService(repository)
    
    # VALOR_FIXO é 10.0, definido no serviço
    peso = 2.5
    taxa_cidade = 5.0
    
    valor_esperado = peso * 10.0 + taxa_cidade  # 2.5 * 10 + 5 = 30
    assert service.calcular_valor(peso, taxa_cidade) == valor_esperado

def test_criar_frete_cliente_inexistente(test_app):
    """Testa a criação de frete com cliente inexistente"""
    with test_app.app_context():
        repository = FreteRepository()
        service = FreteService(repository)
        
        # Cria apenas a cidade
        cidade = Cidade(nome='Teste', uf='MA', taxa=5.0)
        db.session.add(cidade)
        db.session.commit()
        
        with pytest.raises(ValueError, match="Cliente não encontrado"):
            service.criar_frete(
                descricao="Teste",
                peso=1.0,
                codigo_cliente=999,  # cliente inexistente
                codigo_cidade=cidade.codigo_cidade
            )

def test_criar_frete_cidade_inexistente(test_app):
    """Testa a criação de frete com cidade inexistente"""
    with test_app.app_context():
        repository = FreteRepository()
        service = FreteService(repository)
        
        # Cria apenas o cliente
        cliente = Cliente(nome='João', endereco='Rua X', telefone='123')
        db.session.add(cliente)
        db.session.commit()
        
        with pytest.raises(ValueError, match="Cidade não encontrada"):
            service.criar_frete(
                descricao="Teste",
                peso=1.0,
                codigo_cliente=cliente.codigo_cliente,
                codigo_cidade=999  # cidade inexistente
            )

def test_criar_frete_sucesso(test_app):
    """Testa a criação de frete com sucesso"""
    with test_app.app_context():
        repository = FreteRepository()
        service = FreteService(repository)
        
        # Cria cliente e cidade
        cliente = Cliente(nome='João', endereco='Rua X', telefone='123')
        cidade = Cidade(nome='Teste', uf='MA', taxa=5.0)
        db.session.add_all([cliente, cidade])
        db.session.commit()
        
        frete = service.criar_frete(
            descricao="Teste",
            peso=2.5,
            codigo_cliente=cliente.codigo_cliente,
            codigo_cidade=cidade.codigo_cidade
        )
        
        assert frete.descricao == "Teste"
        assert frete.peso == 2.5
        assert frete.valor == 30.0  # 2.5 * 10 + 5
        assert frete.codigo_cliente == cliente.codigo_cliente
        assert frete.codigo_cidade == cidade.codigo_cidade

def test_buscar_fretes_por_cliente(test_app):
    """Testa a busca de fretes por cliente"""
    with test_app.app_context():
        repository = FreteRepository()
        service = FreteService(repository)
        
        # Cria cliente e cidade
        cliente = Cliente(nome='João', endereco='Rua X', telefone='123')
        cidade = Cidade(nome='Teste', uf='MA', taxa=5.0)
        db.session.add_all([cliente, cidade])
        db.session.commit()
        
        # Cria dois fretes para o mesmo cliente
        frete1 = service.criar_frete("Frete 1", 1.0, cliente.codigo_cliente, cidade.codigo_cidade)
        frete2 = service.criar_frete("Frete 2", 2.0, cliente.codigo_cliente, cidade.codigo_cidade)
        
        fretes = service.buscar_por_cliente(cliente.codigo_cliente)
        
        assert len(fretes) == 2
        # Verifica se estão ordenados por valor (decrescente)
        assert fretes[0].valor > fretes[1].valor

def test_frete_maior_valor(test_app):
    """Testa a busca do frete com maior valor"""
    with test_app.app_context():
        repository = FreteRepository()
        service = FreteService(repository)
        
        # Cria cliente e cidade
        cliente = Cliente(nome='João', endereco='Rua X', telefone='123')
        cidade = Cidade(nome='Teste', uf='MA', taxa=5.0)
        db.session.add_all([cliente, cidade])
        db.session.commit()
        
        # Cria três fretes com valores diferentes
        service.criar_frete("Frete 1", 1.0, cliente.codigo_cliente, cidade.codigo_cidade)
        service.criar_frete("Frete 2", 3.0, cliente.codigo_cliente, cidade.codigo_cidade)
        service.criar_frete("Frete 3", 2.0, cliente.codigo_cliente, cidade.codigo_cidade)
        
        maior_frete = service.frete_maior_valor()
        
        assert maior_frete.peso == 3.0  # O frete com maior peso terá o maior valor
