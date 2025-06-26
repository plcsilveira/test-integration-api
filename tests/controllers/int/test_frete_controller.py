import pytest
from app.models import Cliente, Cidade, Frete
from app.database import db

def test_frete_integracao_fluxo_completo(test_app, test_client):
    """Testa o fluxo completo de criação de frete, incluindo cliente e cidade"""
    with test_app.app_context():
        # Criar cliente
        cliente = Cliente(nome="João", telefone="123", endereco="Rua X")
        cidade = Cidade(nome="São Paulo", uf="SP", taxa=5.0)
        db.session.add_all([cliente, cidade])
        db.session.commit()

        # Criar frete via API
        response = test_client.post('/api/fretes', json={
            'descricao': 'Frete teste',
            'peso': 2.5,
            'codigo_cliente': cliente.codigo_cliente,
            'codigo_cidade': cidade.codigo_cidade
        })
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Verificar se o frete foi criado corretamente
        frete = Frete.query.get(data['codigo_frete'])
        assert frete is not None
        assert frete.valor == 30.0  # 2.5 * 10 + 5.0
