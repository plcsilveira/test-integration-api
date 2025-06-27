import pytest
from unittest.mock import Mock
from app.models import Cliente, Cidade, Frete
from app.services.frete import FreteService

# Fixture para configurar os mocks dos repositórios e o serviço
@pytest.fixture
def setup_mocks():
    mock_frete_repo = Mock()
    mock_cliente_repo = Mock()
    mock_cidade_repo = Mock()
    service = FreteService(
        frete_repo=mock_frete_repo,
        cliente_repo=mock_cliente_repo,
        cidade_repo=mock_cidade_repo
    )
    return service, mock_frete_repo, mock_cliente_repo, mock_cidade_repo

def test_calcular_valor_frete(setup_mocks):
    """Testa o cálculo do valor do frete de forma unitária."""
    service, _, _, _ = setup_mocks
    peso = 2.5
    taxa_cidade = 5.0
    valor_esperado = 2.5 * 10.0 + 5.0  # VALOR_FIXO = 10.0
    assert service.calcular_valor(peso, taxa_cidade) == valor_esperado

def test_criar_frete_cliente_inexistente(setup_mocks):
    """Testa a criação de frete com cliente inexistente."""
    service, _, mock_cliente_repo, _ = setup_mocks
    mock_cliente_repo.find_by_id.return_value = None  # Simula cliente não encontrado

    with pytest.raises(ValueError, match="Cliente não encontrado"):
        service.criar_frete("Teste", 1.0, 999, 1)

def test_criar_frete_cidade_inexistente(setup_mocks):
    """Testa a criação de frete com cidade inexistente."""
    service, _, mock_cliente_repo, mock_cidade_repo = setup_mocks
    mock_cliente_repo.find_by_id.return_value = Cliente(codigo_cliente=1, nome="Teste")
    mock_cidade_repo.find_by_id.return_value = None  # Simula cidade não encontrada

    with pytest.raises(ValueError, match="Cidade não encontrada"):
        service.criar_frete("Teste", 1.0, 1, 999)

def test_criar_frete_sucesso(setup_mocks):
    """Testa a criação de frete com sucesso usando mocks."""
    service, mock_frete_repo, mock_cliente_repo, mock_cidade_repo = setup_mocks
    
    # Configura os mocks para retornar objetos válidos
    mock_cliente_repo.find_by_id.return_value = Cliente(codigo_cliente=1, nome="Cliente Mock")
    mock_cidade_repo.find_by_id.return_value = Cidade(codigo_cidade=1, nome="Cidade Mock", taxa=5.0)
    
    # O método save do repo deve retornar o objeto que foi passado para ele
    mock_frete_repo.save.side_effect = lambda frete: frete

    frete = service.criar_frete(
        descricao="Frete Sucesso",
        peso=2.5,
        codigo_cliente=1,
        codigo_cidade=1
    )

    # Verifica se o método save foi chamado
    mock_frete_repo.save.assert_called_once()
    
    # Verifica os valores calculados
    assert frete.valor == 30.0 # 2.5 * 10.0 + 5.0
    assert frete.descricao == "Frete Sucesso"

def test_frete_maior_valor(setup_mocks):
    """Testa a busca pelo frete de maior valor."""
    service, mock_frete_repo, _, _ = setup_mocks
    mock_frete_repo.find_maior_valor.return_value = Frete(valor=100.0)
    
    frete = service.frete_maior_valor()
    
    assert frete.valor == 100.0
    mock_frete_repo.find_maior_valor.assert_called_once()

def test_cidade_com_mais_fretes(setup_mocks):
    """Testa a busca pela cidade com mais fretes."""
    service, mock_frete_repo, _, _ = setup_mocks
    mock_frete_repo.find_cidade_com_mais_fretes.return_value = (1, 15) # (codigo_cidade, total)

    codigo_cidade, total = service.cidade_com_mais_fretes()

    assert codigo_cidade == 1
    assert total == 15
    mock_frete_repo.find_cidade_com_mais_fretes.assert_called_once()
