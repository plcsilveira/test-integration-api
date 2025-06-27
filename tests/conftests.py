import pytest
from app import create_app
from app.database import db as _db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Usa banco em memória para testes

@pytest.fixture(scope='function')
def app():
    """Cria uma instância da aplicação Flask para cada teste."""
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='function')
def db(app):
    """Cria e limpa o banco de dados para cada teste."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Fornece um cliente de teste para a aplicação."""
    return app.test_client()
