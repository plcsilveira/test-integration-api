import unittest
from app import create_app
from app.database import db
from app.models.cliente import Cliente
from app.models.cidade import Cidade
from app.services.frete_service import FreteService

class FreteServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            self.cliente = Cliente(nome='João', telefone='991234567', endereco='Rua X')
            self.cidade = Cidade(nome='Caxias', estado='MA', taxa_entrega=5.0)
            db.session.add_all([self.cliente, self.cidade])
            db.session.commit()

    def test_cadastrar_frete_com_sucesso(self):
        with self.app.app_context():
            frete = FreteService.cadastrar_frete({
                'codigo': 'F010',
                'descricao': 'Frete Teste',
                'peso': 2.5,
                'cliente_id': self.cliente.id,
                'cidade_id': self.cidade.id
            })
            self.assertIsNotNone(frete.id)
            self.assertEqual(frete.valor, 2.5 * 10 + 5.0)

    def test_erro_cliente_ou_cidade_inexistente(self):
        with self.app.app_context():
            with self.assertRaises(ValueError):
                FreteService.cadastrar_frete({
                    'codigo': 'F011',
                    'descricao': 'Frete Falha',
                    'peso': 1.0,
                    'cliente_id': 999,
                    'cidade_id': self.cidade.id
                })

    def test_maior_valor_frete(self):
        with self.app.app_context():
            FreteService.cadastrar_frete({
                'codigo': 'F012',
                'descricao': 'Frete 1',
                'peso': 1.0,
                'cliente_id': self.cliente.id,
                'cidade_id': self.cidade.id
            })
            FreteService.cadastrar_frete({
                'codigo': 'F013',
                'descricao': 'Frete 2',
                'peso': 4.0,
                'cliente_id': self.cliente.id,
                'cidade_id': self.cidade.id
            })

            frete = FreteService.maior_frete()
            self.assertEqual(frete.codigo, 'F013')

    def test_cidade_com_mais_fretes(self):
        with self.app.app_context():
            c2 = Cidade(nome='Codó', estado='MA', taxa_entrega=8.0)
            db.session.add(c2)
            db.session.commit()

            for i in range(2):
                FreteService.cadastrar_frete({
                    'codigo': f'F1{i}',
                    'descricao': 'Frete Codó',
                    'peso': 1.0,
                    'cliente_id': self.cliente.id,
                    'cidade_id': c2.id
                })

            FreteService.cadastrar_frete({
                'codigo': 'F20',
                'descricao': 'Frete Caxias',
                'peso': 1.0,
                'cliente_id': self.cliente.id,
                'cidade_id': self.cidade.id
            })

            mais_fretes = FreteService.cidade_mais_fretes()
            self.assertEqual(mais_fretes.nome, 'Codó')

if __name__ == '__main__':
    unittest.main()