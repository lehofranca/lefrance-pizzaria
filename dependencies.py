from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError

def pegar_sessao():
    try:    
        Session  = sessionmaker(bind=db)
        session = Session()
        yield session
    #except  - Realiza outra função caso a primeira tenha dado errado, mas não usaremos aqui
    finally: #executa função independente do resultado do try dar certo ou não, o que permite finalizar a sessão dessa dependencia. 
        session.close()
        
        
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        # decodifica o token
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub")) # se existir o sub, pega o id do usuário
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Token inválido ou expirado - Acesso Negado. Verifique a validade do token.")
    # verifica se o token é válido
    # extrai o id do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado - Acesso Inválido")
    return usuario
        