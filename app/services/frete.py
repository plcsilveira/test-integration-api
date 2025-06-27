from app.repository.cliente import ClienteRepository
from app.repository.cidade import CidadeRepository
from app.repository.frete import FreteRepository
from app.models.frete import Frete

VALOR_FIXO = 10.0  # R$ 10,00 por kg

class FreteService:
    def __init__(self, frete_repo: FreteRepository, cliente_repo: ClienteRepository, cidade_repo: CidadeRepository):
        self.frete_repo = frete_repo
        self.cliente_repo = cliente_repo
        self.cidade_repo = cidade_repo
    
    def calcular_valor(self, peso: float, taxa_cidade: float) -> float:
        return peso * VALOR_FIXO + taxa_cidade
    
    def criar_frete(self, descricao: str, peso: float, codigo_cliente: int, codigo_cidade: int) -> Frete:
        cliente = self.cliente_repo.find_by_id(codigo_cliente)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        cidade = self.cidade_repo.find_by_id(codigo_cidade)
        if not cidade:
            raise ValueError("Cidade não encontrada")
        valor = self.calcular_valor(peso, cidade.taxa)
        frete = Frete(
            descricao=descricao,
            peso=peso,
            valor=valor,
            codigo_cliente=codigo_cliente,
            codigo_cidade=codigo_cidade
        )
        return self.frete_repo.save(frete)

    def frete_maior_valor(self) -> Frete | None:
        return self.frete_repo.find_maior_valor()

    def cidade_com_mais_fretes(self):
        return self.frete_repo.find_cidade_com_mais_fretes()
