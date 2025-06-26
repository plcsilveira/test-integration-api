# test-integration-api

---
transportadora_api/
│
├── app/                  # O pacote principal da sua aplicação Flask
│   ├── __init__.py       # Arquivo de inicialização (contém a Application Factory)
│   ├── models.py         # Camada de Modelo (classes do SQLAlchemy)
│   ├── schemas.py        # Para validação de dados da API (com Pydantic)
│   ├── repositories.py   # Camada de Repositório
│   ├── services.py       # Camada de Serviço (lógica de negócio)
│   └── routes.py         # Camada de Controle (endpoints da API)
│
├── tests/                # Pasta para todos os seus testes
│   ├── __init__.py
│   ├── conftest.py       # Arquivo para fixtures do Pytest (ex: app de teste)
│   ├── test_repositories.py
│   ├── test_services.py
│   └── test_api.py
│
├── config.py             # Arquivo de configurações
├── run.py                # Script para iniciar a aplicação
└── requirements.txt      # Lista de dependências do projeto

---