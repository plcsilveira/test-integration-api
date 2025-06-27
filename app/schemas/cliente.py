from pydantic import BaseModel, Field
from typing import Annotated

class ClienteSchema(BaseModel):
    nome: Annotated[str, Field(max_length=30)]
    endereco: Annotated[str, Field(max_length=30)]
    telefone: Annotated[str, Field(max_length=30)]
    
    class Config:
        from_attributes = True  # permite conversão de SQLAlchemy model para Pydantic
