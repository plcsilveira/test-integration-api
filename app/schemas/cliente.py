from pydantic import BaseModel, constr

class ClienteSchema(BaseModel):
    nome: constr(min_length=1, max_length=30)
    endereco: constr(min_length=1, max_length=30)
    telefone: constr(min_length=1, max_length=30)
    
    class Config:
        from_attributes = True  # permite conversão de SQLAlchemy model para Pydantic
