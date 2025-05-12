# Dashboard Backend

Este é o backend de um sistema de dashboard desenvolvido com **FastAPI** e **PostgreSQL**. A aplicação utiliza **Docker** para facilitar a execução local.

## Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Como executar o projeto localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/guilhermeytalo/SmartMartBack.git
cd SmartMartBack
```

### 2. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Certifique-se de que as variáveis no arquivo `.env` estão configuradas corretamente. Por padrão, o banco de dados será configurado com as seguintes credenciais:

```plaintext
  DATABASE_URL=postgresql://admin:admin@db:5432/dashboard
  POSTGRES_USER=admin
  POSTGRES_PASSWORD=admin
  POSTGRES_DB=dashboard
```

### 3. Construir e iniciar os containers

Para construir e iniciar os containers, execute:

```bash
docker-compose up --build
```

Ou, se os containers já estiverem construídos:

```bash
docker-compose up
```

### 4. Aplicar as migrações do banco de dados

Após os containers estarem em execução, aplique as migrações do banco de dados:

```bash
docker exec -it dashboard-backend alembic upgrade head
```

### 5. Acessar a aplicação

Acesse a documentação interativa da API no navegador:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Estrutura do Projeto

```plaintext
dashboard-backend/
│
├── static/
│   ├── sample_products.csv 
├── alembic/
│   ├── versions/  
│   ├── env.py 
├── app/
│   ├── main.py                                         ✅ ponto de entrada
│   ├── domain/                                         ✅ lógica de negócio e regras
│   │   ├── entities/                                   → entidades puras
│   │   │   └── product.py
│   │   ├── repositories/                               → contratos (interfaces)
│   │   │   └── product_repository.py
│   │   └── services/                                   → lógica específica (ex: cálculo de lucro)
│   │       └── profit_calculator.py
│   ├── application/                                    ✅ casos de uso (orquestram regras)
│   │   └── use_cases/
│   │       ├── create_product.py
│   │       └── list_products.py
│   ├── infrastructure/                                 ✅ implementações técnicas
│   │   └── db/                                         → banco de dados, repositórios concretos
│   │       ├── models/
│   │       │  ├── category.py
│   │       │  └── product.py
│   │       ├── database.py
│   │       └── product_repository_impl.py
│   └── interfaces/                                     ✅ camada de entrada
│       └── dtos/
│           └── product_dto.py 
│       └── routes/                                     → endpoints FastAPI
│           └── products.py
├── venv/
├── .env
├── .envrc
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
└── README.md
```

### Exemplos de Uso

#### Criar um produto com uma categoria existente (por ID)

```json
{
  "name": "iPhone 15",
  "price": 999.99,
  "brand": "Apple",
  "quantity": 10,
  "category": {
    "id": 1
  }
}
```

#### Criar um produto com uma nova categoria

```json
{
  "name": "Galaxy S24",
  "price": 899.99,
  "brand": "Samsung",
  "quantity": 5,
  "category": {
    "name": "Premium Phones",
    "description": "Flagship smartphones"
  }
}
```

#### Importar produtos via CSV

Você pode importar produtos utilizando um arquivo CSV. O formato esperado é:

```csv
id,name,description,price,category_id,category_name,brand,quantity
1,Samsung 65" QLED TV,65-inch 4K Smart TV with HDR,1299.99,1,TVs,Samsung,10
```

Envie o arquivo para o endpoint `/products/import-csv`.

#### Baixar um exemplo de CSV

Você pode baixar um exemplo de CSV no endpoint `/products/sample-csv`.

### Encerrar os containers

Para encerrar os containers, pressione `Ctrl+C` ou execute:

```bash
docker-compose down
```

### Limpar volumes do Docker (opcional)

Se desejar limpar os volumes do Docker, execute:

```bash
docker-compose down -v
```

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Docker**: Para containerização da aplicação.
- **Alembic**: Para controle de migrações do banco de dados.

## Deploy
Você pode ver a API aqui neste [link](https://smartmartbackonrender.com/docs)