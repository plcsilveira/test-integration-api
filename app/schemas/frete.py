from pydantic import BaseModel, Field
from typing import Annotated

class FreteBaseSchema(BaseModel):
    descricao: Annotated[str, Field(min_length=1, max_length=30)]
    peso: Annotated[float, Field(gt=0)]
    
    class Config:
        from_attributes = True

class FreteCreateSchema(FreteBaseSchema):
    codigo_cliente: int
    codigo_cidade: int

class FreteSchema(FreteBaseSchema):
    codigo_frete: int
    valor: float  # será calculado pelo serviço
