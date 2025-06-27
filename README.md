# API de Transportadora com Flask

Esta é uma API REST desenvolvida em Flask para gerenciar operações de uma transportadora, incluindo o cadastro de clientes, cidades e o cálculo de fretes. A aplicação segue uma arquitetura em camadas (Controllers, Services, Repositories) para garantir a separação de responsabilidades e facilitar a manutenção e os testes.

## Estrutura do Projeto

A estrutura do projeto foi organizada da seguinte forma para promover a modularidade e a testabilidade:

```
test-integration-api/
│
├── app/                    # O pacote principal da sua aplicação Flask
│   ├── __init__.py         # Arquivo de inicialização que exporta as principais funções
│   ├── factory.py          # Contém a Application Factory (create_app)
│   ├── database.py         # Configuração e instância do banco de dados
│   │
│   ├── models/            # Camada de Modelo (SQLAlchemy)
│   ├── schemas/           # Schemas Pydantic para validação da API
│   ├── repository/        # Camada de Repositório (Operações no Banco)
│   ├── services/          # Camada de Serviço (Regras de Negócio)
│   └── controllers/       # Camada de Controle (API REST)
│
├── tests/                 # Testes do projeto
│   ├── conftest.py        # Fixtures globais (app, client, db em memória)
│   ├── controllers/       # Testes dos controllers (integração)
│   ├── services/          # Testes dos serviços (unitários e integração)
│   └── repository/        # Testes dos repositórios (integração)
│
├── config.py             # Arquivo de configurações
├── run.py                # Script para iniciar a aplicação
└── requirements.txt      # Lista de dependências do projeto
```

## Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd test-integration-api
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *No Windows, use `venv\Scripts\activate`.*

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Execução

Para iniciar a aplicação Flask, execute o seguinte comando na raiz do projeto:

```bash
flask run
```

A API estará disponível em `http://127.0.0.1:5000`.

## Testes

O projeto utiliza `pytest` para testes unitários e de integração. A configuração dos testes garante o uso de um banco de dados SQLite em memória para isolar o ambiente de teste do ambiente de desenvolvimento.

Para rodar todos os testes, execute:

```bash
pytest
```

Para verificar a cobertura de testes, utilize o `pytest-cov`:

```bash
pytest --cov=app
```

### Tipos de Testes

-   **Testes Unitários (`/tests/services/unit`):** Focados em testar a lógica de negócio na camada de serviço de forma isolada, utilizando mocks para simular as dependências (como os repositórios).
-   **Testes de Integração (`/tests/repository/int`, `/tests/controllers/int`):** Testam a interação entre as diferentes camadas da aplicação, como a comunicação do controller com o serviço e do serviço com o banco de dados em memória.

## Endpoints da API

A seguir estão os principais endpoints disponíveis na API.

### Fretes

-   `POST /fretes/`: Cria um novo frete.
    -   **Payload:** `{"descricao": "string", "peso": float, "codigo_cliente": int, "codigo_cidade": int}`
-   `GET /fretes/cliente/<int:cliente_id>`: Retorna os fretes de um cliente específico, ordenados pelo valor.
-   `GET /fretes/maior-valor`: Retorna o frete com o maior valor.
-   `GET /fretes/cidade/estatisticas`: Retorna a cidade com o maior número de fretes registrados.

*Observação: Outros endpoints para Clientes e Cidades também estão disponíveis, seguindo o padrão REST.*
