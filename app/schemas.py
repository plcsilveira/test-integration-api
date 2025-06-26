from pydantic import BaseModel, constr

class ClienteSchema(BaseModel):
    nome: constr(max_length=30)
    endereco: constr(max_length=30)
    telefone: constr(max_length=30)