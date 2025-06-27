import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.factory import create_app
from app.database import db as _db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Usa banco em memória para testes

# Ativar foreign keys para SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture(scope='function')
def test_app():
    """Cria uma instância da aplicação Flask para cada teste."""
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='function')
def db(test_app):
    """Cria e limpa o banco de dados para cada teste."""
    with test_app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
def client(test_app):
    """Fornece um cliente de teste para a aplicação."""
    return test_app.test_client()
