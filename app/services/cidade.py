from app.repository import CidadeRepository

class CidadeService:
    def __init__(self, repository: CidadeRepository):
        self.repository = repository
    
    def criar_cidade(self, nome: str, uf: str, taxa: float):
        # Verifica se já existe cidade com esse nome
        cidade_existente = self.repository.busca_por_nome(nome)
        if cidade_existente:
            raise ValueError("Já existe uma cidade com este nome")
        
        return self.repository.create(
            nome=nome,
            uf=uf,
            taxa=taxa
        )
    
    def buscar_por_nome(self, nome: str):
        return self.repository.busca_por_nome(nome)
