from fastapi import FastAPI
from passlib.context import CryptContext # Ferramenta para criptografar as senhas 
from dotenv import load_dotenv # Carrega as variáveis de ambientes (.env)
from fastapi.security import OAuth2PasswordBearer # Cria a estrutura de Token Bearer

import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY","").strip() # O método strip remove espaços em branco no início e no final da string
ALGORITHM = os.getenv("ALGORITHM", "").strip() # O método strip remove espaços em branco no início e no final da string
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES").strip())

app = FastAPI()

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl = "auth/login-form")  # Cria o esquema de autenticação OAuth2 com o prefixo "auth/login"

from auth_routes import auth_router
from order_routes import order_router


app.include_router(auth_router)
app.include_router(order_router)
 
 
# Framework - Conjunto de ferramentas de uma linguagem de programação que tem suas
# próprias regras. Cria-se um código dentro de um framewor, programa-se dentro do
#framework (neste caso, com a linguagem python), não o inverso.

# para rodar o nosso código , executar no terminal: uvicorn main:app --reload

# endpoint: # é o caminho que o usuário acessa para chegar a uma determinada funcionalidade do sistema.
# dominio.com/pedidos
# www.hastagtreinamentos.com.br/ordens
#/ordens (path)
# Json = formatos de respostas
# """ """  -> Doc String / Orientação de como utilizar a API e os endpoints criados

# Sempre que criado um endpoint, deverá ser criado seu caminho(path) e o tipo de requisição
# Para cada rota que for criada é interessante criar um arquivo específico para ela. 
# Por ex: rota de orders, rota de autenticação, rota de admin, etc.

# Rest APIs - Acessa os endpoints e faz requisições
# Get -> Leitura / Pegar
# Post -> Enviar / Criar
# Put/ Patch -> Editar
# Delete -> Deletar

#  Print para debug
#print("SECRET_KEY:", SECRET_KEY)
#print("ALGORITHM:", ALGORITHM)
#print("ACCESS_TOKEN_EXPIRE_MINUTES:", ACCESS_TOKEN_EXPIRE_MINUTES)


# Migrar banco de dados no terminal:
# criar a migração do banco de dados : alembic revision --autogenerate -m "nome da migração"
# executar a migração do banco de dados: alembic upgrade head