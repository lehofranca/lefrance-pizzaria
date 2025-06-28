from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
# JWT - Json Web Tokens | Estrutura de tokens
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter (prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token  # hora de agora + 30 minutos (UTC= 0h, by Gr)
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info,SECRET_KEY,ALGORITHM)
    # JWT
    #id_usuario
    #data_expericarao
    #dic_info = dicionario de informações
  
    return jwt_codificado



def autenticar_usuario(email,senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

#dominio/auth/

@auth_router.get("/")
async def home():       #Home / autenticar
    """ 
    Essa é a rota padrão de autenticação do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return{"mensagem": "você acessou a rota padrão de autenticação", "autenticado":False}

@auth_router.post("/criar_conta")
async def criar_conta (usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail= "Email do usuário ja cadastrado")
    else:
        senha_criptografada =  bcrypt_context.hash(usuario_schema.senha)      #Hash é um codigo criptografado
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        
        return {"mensagem": "usuário cadastrado com sucesso {usuario_schema.email}"}
    
    
    
    
# JWT - Json Web Tokens | Estrutura de tokens

@auth_router.post("/login")
async def login (login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
       #usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
        # Sempre que quiser buscar algo no banco de dados, usar a função session.query () e incluir dentro dos parenteses
        # a tabela escolhida para busca dos registros
        usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
        if not usuario:
            raise HTTPException(status_code=400, detail= "Usuário não encontrado ou credenciais inválidas")
        else:
            access_token = criar_token(usuario.id)
            refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
            return {
                "access_token": access_token,
                   "refresh_token": refresh_token,
                   "token_type": "Bearer"
            }
            
@auth_router.post("/login-form")
async def login_form (dados_formulario: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(pegar_sessao)):
        usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
        # Sempre que quiser buscar algo no banco de dados, usar a função session.query () e incluir dentro dos parenteses
        # a tabela escolhida para busca dos registros
        # Dependendo do tipo de autenticação, pode ser necessário usar o Depends para pegar o token
        if not usuario:
            raise HTTPException(status_code=400, detail= "Usuário não encontrado ou credenciais inválidas")
        else:
            access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }

            
   # JWT Bearer
   # headers = {"Acess-Token": "Bearer - Token"}   
            
        
# Pegar um refresh token
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    #Verificar Token
    access_token = criar_token(usuario.id)
    return { 
            "access_token": access_token,
            "token_type": "Bearer"
         }