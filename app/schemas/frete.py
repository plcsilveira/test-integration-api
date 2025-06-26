from pydantic import BaseModel, constr, confloat
from typing import Optional

class FreteBaseSchema(BaseModel):
    descricao: constr(min_length=1, max_length=30)
    peso: confloat(gt=0)
    
    class Config:
        from_attributes = True

class FreteCreateSchema(FreteBaseSchema):
    codigo_cliente: int
    codigo_cidade: int

class FreteSchema(FreteBaseSchema):
    codigo_frete: int
    valor: float  # será calculado pelo serviço
