# test-integration-api

```
test-integration-api/
│
├── app/                    # O pacote principal da sua aplicação Flask
│   ├── __init__.py         # Arquivo de inicialização que exporta as principais funções
│   ├── factory.py          # Contém a Application Factory (create_app)
│   ├── database.py         # Configuração e instância do banco de dados
│   │
│   ├── models/            # Camada de Modelo (SQLAlchemy + Validações)
│   │   ├── __init__.py     # Exporta os modelos
│   │   ├── cliente.py      # Modelo Cliente (nome, endereco, telefone)
│   │   ├── cidade.py       # Modelo Cidade (nome, uf, taxa)
│   │   ├── frete.py        # Modelo Frete (descricao, peso, valor, cliente_id, cidade_id)
│   │   
│   │
│   ├── schemas/           # Schemas Pydantic para validação da API
│   │   ├── __init__.py     # Exporta os schemas
│   │   ├── cliente.py      # Schema de Cliente (validações: campos obrigatórios)
│   │   ├── cidade.py       # Schema de Cidade (validações: campos obrigatórios)
│   │   └── frete.py        # Schema de Frete (validações + cálculo de valor)
│   │
│   ├── repository/        # Camada de Repositório (Operações no Banco)
│   │   ├── __init__.py     # Exporta os repositórios
│   │   ├── cliente.py      # ClienteRepo (cadastro, busca por telefone)
│   │   ├── cidade.py       # CidadeRepo (cadastro, busca por nome)
│   │   ├── frete.py        # FreteRepo (cadastro, busca por cliente, ordenação)
│   │   └── tests/          # Testes dos repositórios
│   │
│   ├── services/          # Camada de Serviço (Regras de Negócio)
│   │   ├── __init__.py     # Exporta os serviços
│   │   ├── cliente.py      # ClienteService (validações de negócio)
│   │   ├── cidade.py       # CidadeService (validações de negócio)
│   │   ├── frete.py        # FreteService (cálculo valor, validações, stats)
│   │   └── tests/          # Testes dos serviços
│   │
│   └── controllers/       # Camada de Controle (API REST)
│       ├── __init__.py     # Configuração dos blueprints
│       ├── cliente.py      # Endpoints de Cliente
│       ├── cidade.py       # Endpoints de Cidade
│       ├── frete.py        # Endpoints de Frete
│       └── tests/          # Testes dos controllers
│
├── tests/                 # Testes de Integração de Sistema
│   ├── __init__.py
│   ├── conftest.py        # Fixtures globais (app, client, db em memória)
│   └── test_integration_frete.py                   
│
├── config.py             # Arquivo de configurações
├── run.py                # Script para iniciar a aplicação
└── requirements.txt      # Lista de dependências do projeto

```
