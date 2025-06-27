import pytest
from sqlalchemy.exc import IntegrityError

from app.models.cidade import Cidade
from app.repository.cidade import CidadeRepository

def test_save_cidade(db):
    repo = CidadeRepository()
    cidade = Cidade(
        nome="São Luís",
        UF="MA",
        taxa=15.0
    )
    
    saved_cidade = repo.save(cidade)
    
    assert saved_cidade.codigo_cidade is not None
    assert saved_cidade.nome == "São Luís"
    
    retrieved_cidade = db.session.get(Cidade, saved_cidade.codigo_cidade)
    assert retrieved_cidade is not None
    assert retrieved_cidade.nome == "São Luís"

def test_find_by_nome(db):
    repo = CidadeRepository()
    cidade = Cidade(nome="Imperatriz", UF="MA", taxa=25.0)
    repo.save(cidade)
    
    found_cidade = repo.find_by_nome("Imperatriz")
    
    assert found_cidade is not None
    assert found_cidade.nome == "Imperatriz"
    assert found_cidade.UF == "MA"

def test_find_by_nome_not_found(db):
    repo = CidadeRepository()
    found_cidade = repo.find_by_nome("Cidade Inexistente")
    assert found_cidade is None

def test_save_cidade_raises_integrity_error_on_null_nome(db):
    repo = CidadeRepository()
    cidade = Cidade(nome=None, UF="MA", taxa=10.0)
    
    with pytest.raises(IntegrityError):
        repo.save(cidade)
        db.session.rollback()
