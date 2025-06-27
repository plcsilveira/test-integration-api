from pydantic import BaseModel, Field
from typing import Annotated

class CidadeSchema(BaseModel):
    nome: Annotated[str, Field(min_length=1, max_length=30)]
    UF: Annotated[str, Field(min_length=1, max_length=30)]
    taxa: Annotated[float, Field(gt=0)]
    
    class Config:
        from_attributes = True
