from app.repository import ClienteRepository

class ClienteService:
    def __init__(self, repository: ClienteRepository):
        self.repository = repository
    
    def criar_cliente(self, nome: str, endereco: str, telefone: str):
        # Verifica se já existe cliente com esse telefone
        cliente_existente = self.repository.busca_por_telefone(telefone)
        if cliente_existente:
            raise ValueError("Já existe um cliente com este telefone")
        
        return self.repository.create(
            nome=nome,
            endereco=endereco,
            telefone=telefone
        )
    
    def buscar_por_telefone(self, telefone: str):
        return self.repository.busca_por_telefone(telefone)
