from app.repository import FreteRepository
from app.models import Cliente, Cidade

VALOR_FIXO = 10.0  # R$ 10,00 por kg

class FreteService:
    def __init__(self, repository: FreteRepository):
        self.repository = repository
    
    def calcular_valor(self, peso: float, taxa_cidade: float) -> float:
        return peso * VALOR_FIXO + taxa_cidade
    
    def criar_frete(self, descricao: str, peso: float, 
                   codigo_cliente: int, codigo_cidade: int):
        # Verifica se cliente existe
        cliente = Cliente.query.get(codigo_cliente)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        # Verifica se cidade existe
        cidade = Cidade.query.get(codigo_cidade)
        if not cidade:
            raise ValueError("Cidade não encontrada")
        
        # Calcula valor do frete
        valor = self.calcular_valor(peso, cidade.taxa)
        
        # Cria o frete
        return self.repository.create(
            descricao=descricao,
            peso=peso,
            valor=valor,
            codigo_cliente=codigo_cliente,
            codigo_cidade=codigo_cidade
        )
    
    def buscar_por_cliente(self, codigo_cliente: int):
        return self.repository.busca_por_cliente(codigo_cliente)
    
    def frete_maior_valor(self):
        return self.repository.maior_valor()
