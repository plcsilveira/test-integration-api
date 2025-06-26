from .repositories import ClienteRepository # Exemplo

class FreteService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()
        # ... inicializar outros repositórios