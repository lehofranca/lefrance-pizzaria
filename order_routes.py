from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido


order_router = APIRouter (prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

#dominio/order/

@order_router.get("/") # prefixo order/ pedidos
async def pedidos():

    """ 
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"mensagem": "você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario = pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    
    return {"mensagem": f" Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}



@order_router.post("/pedido/cancelar/{id_pedido}") # passar uma rota como parâmetro dever ser dentro de conchetes / chaves e também
#incluir na função como parâmetro
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    # usuario_admin = True # para testes, mas depois deve ser retirado
    # usuario_id = pedido.usuario # pegar o id do usuário que está fazendo o pedido
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first() 
    # session_query é uma busca no banco de dados, filtrando pelo id do pedido.
    # .first() retorna o primeiro resultado encontrado ou None se não houver resultados.
    
    if not pedido:
        raise HTTPException (status_code=400, detail = "Pedido não encontrado")
    
    # Criação de diferentes tipos de acessos
    # Passar como argumento da rota uma dependência de autenticação, que vai verificar quem é o usuário que está fazendo a requisição.
    # Usar o usuário para criar um if e verificar se o usuário é admin ou se o usuário que está fazendo a requisição é o mesmo que fez o pedido.
    # Criar condição que vai interromper a execução do código (rota) caso o usuário não seja admin e não seja o usuário que fez o pedido.
    if not usuario.admin and usuario.id != pedido.usuario:  # Nível de acesso do usuário
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para cancelar este pedido.")
    
    pedido.status = "CANCELADO"
    session.commit() # salvar a edicação do pedido (cancelamento)
    # não é incluido session.add, porque neste caso o pedido já existe e apenas está sendo atualizado o status dele.
    # Não precisando incluir na sessão novamente, apenas atualizando o status do pedido existente.
    
    return {
        "mensagem": f"Pedido número {pedido.id} cancelado com sucesso.",
        "pedido": pedido 
    }
# pedido: pedido vai descrever os itens que estão dentro do pedido, como o id, status, usuario e preço, ainda que cancelado.

@order_router.get('/listar')
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para essa operação (acessar listar pedidos).")       
    else:
        pedidos = session.query(Pedido).all()
        return {
            "mensagem": "Lista de pedidos",
            "pedidos": pedidos
        }
        
@order_router.post('/pedido/adicionar-item/{id_pedido}') 
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para essa operação(adicionar itens a este pedido).")
    item_pedido = ItemPedido(item_pedido_schema.quantidade,item_pedido_schema.sabor,
                             item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    #editando o campo preço do pedido, sempre que um item for adicionado ou removido do pedido.
    session.add(item_pedido) 
    pedido.calcular_preco()
    session.commit()
    return {" mensagem": "Item criado com sucesso.",
            "item_pedido": item_pedido.id,
            "preco_pedido": pedido.preco
            }
    
@order_router.post('/pedido/remover-item/{id_item_pedido}') #metódo post pois está enviando uma informação para ser editada
async def remover_item_pedido(id_item_pedido: int,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para essa operação(adicionar itens a este pedido).")
    session.delete(item_pedido)
    #editando o campo preço do pedido, sempre que um item for adicionado ou removido do pedido.
    
    pedido.calcular_preco()
    session.commit()
    return {" mensagem": "Item removido com sucesso.",
            "quantidade_itens_pedido": len(pedido.itens), # função len faz a contagem de quantos itens estão dentro do pedido
            "pedido": pedido
            }
    # sempre que editar um item do pedido, deve atualizar o preço do pedido, criando na classe Pedido um método (função) para atualizar o preço.
    # no arquivo models função : def calcular_preco(self):
    
    
    # Rota Finalizar Pedido
@order_router.post('/pedido/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido: int,  
                            session: Session = Depends(pegar_sessao),
                            usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para essa operação(finalizar este pedido).")
    
    pedido.status = "FINALIZADO"
    session.commit()
    
    return {
        "mensagem": f"Pedido número {pedido.id} finalizado com sucesso.",
        "pedido": pedido
    }
    
    # Rota Visualizar 1 Pedido
@order_router.get('/pedido/{id_pedido}')
async def visualizar_pedido(id_pedido: int,
                            session: Session = Depends(pegar_sessao),
                            usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para essa operação(visualizar este pedido).")
    
    return {
        "mensagem": f"Pedido número {pedido.id} encontrado com sucesso.",
        "pedido": pedido
    }   
    
    # Rota visualizar todos os pedidos de um usuário
@order_router.get('/pedidos-usuario')
async def pedidos_usuario(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    
    if not pedidos:
        raise HTTPException(status_code=400, detail="Nenhum pedido encontrado para este usuário")
    
    return {
        "mensagem": f"Pedidos do usuário {usuario.id} encontrados com sucesso.",
        "pedidos": pedidos
    }
    
    # Endpoints são os caminhos de cada rota que temos em um site, como por exemplo:
    # www.lefrancepizzaria.com.br/pedidos
    