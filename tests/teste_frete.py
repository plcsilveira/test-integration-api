import unittest
from app import create_app
from app.database import db

class FreteIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_criar_cliente_cidade_e_frete(self):
        # Cria cliente
        resp_cliente = self.client.post('/clientes', json={
            'nome': 'João',
            'telefone': '989999999',
            'endereco': 'Rua A'
        })
        self.assertEqual(resp_cliente.status_code, 201)
        cliente_id = resp_cliente.get_json()['id']

        # Cria cidade
        resp_cidade = self.client.post('/cidades', json={
            'nome': 'São Luís',
            'estado': 'MA',
            'taxa_entrega': 5.0
        })
        self.assertEqual(resp_cidade.status_code, 201)
        cidade_id = resp_cidade.get_json()['id']

        # Cria frete
        resp_frete = self.client.post('/fretes', json={
            'codigo': 'F001',
            'descricao': 'Entrega 1',
            'peso': 2.0,
            'cliente_id': cliente_id,
            'cidade_id': cidade_id
        })
        self.assertEqual(resp_frete.status_code, 201)
        dados = resp_frete.get_json()
        self.assertIn('valor', dados)
        self.assertEqual(dados['valor'], 2.0 * 10.0 + 5.0)  # VALOR_FIXO = 10.0

    def test_frete_com_cliente_inexistente(self):
        # Cria cidade
        resp_cidade = self.client.post('/cidades', json={
            'nome': 'Imperatriz',
            'estado': 'MA',
            'taxa_entrega': 8.0
        })
        cidade_id = resp_cidade.get_json()['id']

        # Tenta criar frete com cliente inexistente
        resp_frete = self.client.post('/fretes', json={
            'codigo': 'F002',
            'descricao': 'Entrega 2',
            'peso': 1.5,
            'cliente_id': 999,  # inexistente
            'cidade_id': cidade_id
        })
        self.assertEqual(resp_frete.status_code, 400)
        self.assertIn('erro', resp_frete.get_json())

    def test_consulta_fretes_por_cliente(self):
        # Cria cliente e cidade
        cliente_resp = self.client.post('/clientes', json={
            'nome': 'Maria',
            'telefone': '988888888',
            'endereco': 'Rua B'
        })
        cliente_id = cliente_resp.get_json()['id']

        cidade_resp = self.client.post('/cidades', json={
            'nome': 'Bacabal',
            'estado': 'MA',
            'taxa_entrega': 7.0
        })
        cidade_id = cidade_resp.get_json()['id']

        # Cria dois fretes
        self.client.post('/fretes', json={
            'codigo': 'F003',
            'descricao': 'Entrega 3',
            'peso': 1,
            'cliente_id': cliente_id,
            'cidade_id': cidade_id
        })
        self.client.post('/fretes', json={
            'codigo': 'F004',
            'descricao': 'Entrega 4',
            'peso': 3,
            'cliente_id': cliente_id,
            'cidade_id': cidade_id
        })

        # Consulta fretes por cliente
        resp = self.client.get(f'/fretes/cliente/{cliente_id}')
        self.assertEqual(resp.status_code, 200)
        lista = resp.get_json()
        self.assertEqual(len(lista), 2)
        self.assertLessEqual(lista[0]['valor'], lista[1]['valor'])  # ordenado por valor

if __name__ == '__main__':
    unittest.main()