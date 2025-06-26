from pydantic import BaseModel, constr, confloat

class CidadeSchema(BaseModel):
    nome: constr(min_length=1, max_length=30)
    uf: constr(min_length=2, max_length=2)
    taxa: confloat(gt=0)  # valor deve ser maior que 0
    
    class Config:
        from_attributes = True
