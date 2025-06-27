import pytest
from app.models import Cliente, Cidade
from app.models.frete import Frete


def test_frete_integracao_fluxo_completo(db, client):
    """Testa o fluxo completo de criação de frete, incluindo cliente e cidade"""
    # Criar cliente
    cliente = Cliente(nome="João", telefone="123", endereco="Rua X")
    cidade = Cidade(nome="São Paulo", UF="SP", taxa=5.0)
    db.session.add(cliente)
    db.session.add(cidade)
    db.session.commit()

    # Dados do frete
    frete_data = {
        "descricao": "Frete de teste",
        "peso": 10.5,
        "cliente_id": cliente.codigo_cliente,
        "cidade_id": cidade.codigo_cidade
    }

    # Enviar requisição POST
    response = client.post("/api/fretes", json=frete_data)

    # Verificar resposta
    assert response.status_code == 201
    data = response.get_json()
    assert data["descricao"] == "Frete de teste"
    assert data["valor"] is not None # O valor deve ser calculado

    # Verificar se o frete foi salvo no banco
    frete_salvo = db.session.get(Frete, data["codigo_frete"])
    assert frete_salvo is not None
    assert frete_salvo.descricao == "Frete de teste"
