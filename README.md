# Sistema Backend para Pizzaria - FastAPI

Este é um backend desenvolvido em **FastAPI** para gerenciar uma pizzaria, com funcionalidades para:  
- Cadastro e autenticação de usuários  
- Criação e gerenciamento de pedidos  
- Controle de sessões e permissões  
- Modelagem do banco de dados usando SQLAlchemy  
- Validação e serialização de dados com Pydantic schemas  

## Funcionalidades

- Registro e login de usuários com segurança  
- CRUD completo para pedidos e usuários  
- Controle de status dos pedidos  
- Integração com banco de dados relacional (ex: PostgreSQL, SQLite)  
- Tratamento de erros e validações  

## Tecnologias utilizadas

- Python 3.10+  
- FastAPI  
- SQLAlchemy  
- Pydantic  
- Alembic (para migrations)  
- JWT (JSON Web Tokens) para autenticação  
- Uvicorn (servidor ASGI)  

## Como rodar o projeto

1. Clone o repositório:  
git clone https://github.com/lehofranca/lefrance-pizzaria



2. Crie e ative um ambiente virtual (recomendado):
python -m venv venv
source venv/bin/activate # Linux/Mac  
venv\Scripts\activate    # Windows



3. Instale as dependências:
pip install -r requirements.txt


4. Configure variáveis de ambiente (exemplo .env):

DATABASE_URL=sqlite:///./db.sqlite3
SECRET_KEY=sua_chave_secreta

5. Rode as migrations:
alembic upgrade head

6. Execute o servidor:
 uvicorn main:app --reload

Endpoints principais
/users/ - Gerenciamento de usuários

/auth/ - Autenticação e geração de tokens

/orders/ - Criação e gerenciamento de pedidos





Contato
Para dúvidas ou sugestões, entre em contato:

GitHub:https://github.com/lehofranca

LinkedIn:https://www.linkedin.com/in/leonardo-mendes-de-fran%C3%A7a-2a8a75193/
