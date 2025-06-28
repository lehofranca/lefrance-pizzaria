from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, ForeignKey
# permite criar um banco de dados 
from sqlalchemy.orm import declarative_base, relationship # criar a base do banco de dados; 
# Relationship  permite criar relacionamentos entre tabelas
from sqlalchemy_utils.types import ChoiceType
# cria a conexão do banco de dados
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados
Base = declarative_base()

# criar as classes/tabelas do banco de dados
# Usuario
class Usuario (Base): # por padrão, o banco cria um "s" ao nome de cada classe, mas é possível criar uma função para nomear a classe\tabela.
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable = False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default= False) # Com isso, é possível criar um usuário, sem ele necessariamente ser admin.
    
    def __init__(self, nome, email, senha, ativo=True, admin=False):# init, função que será realizada a cada criação de usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
    
# Pedido
class Pedido (Base):
    __tablename__ = "pedidos"
    
    #STATUS_PEDIDOS = (
       # ("PENDENTE", "PENTENDE"),
       # ("CANCELADO","CANCELADO"),
       # ("FINALIZADO", "FINALIZADO")
        
       # ) 
       #(chave, valor) - lista de tuplas ou tuplas de tuplas; Após importo choice type é possivel determinar uma regra pra string de status pedido
        # Na pratica, se tentar colocar qqr outro status na coluna status, não vai funcionar.
        #Garantia da integridade do banco de dados
    
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # pendente, cancelado e finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido",cascade="all, delete")
    # cacade permite que, ao deletar um pedido, todos os itens relacionados a ele também sejam deletados. 
    # backref permite acessar os itens do pedido a partir do pedido, e o pedido a partir dos itens.
    
    def __init__(self, usuario, status ="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco
        
    def calcular_preco(self):
  
        # Método para calcular o preço total do pedido.
        # Deve ser chamado sempre que um item for adicionado ou removido do pedido.
       
        # Percorrer todos os itens do pedido 
        # Somar todos os itens do pedido
        # Editar no campo "preço" o valor final do pedido
        preco_pedido = 0
        #for item in self.itens:   
        # preco_item = item.preco_unitario * item.quantidade
        # preco_pedido += preco_item
        
            # Aqui você pode implementar a lógica para calcular o preço total do pedido
            # Por exemplo, somando os preços de todos os itens do pedido
           
        # Atualiza o preço do pedido total
        # Aqui você pode implementar a lógica para calcular o preço total do pedido
        # Por exemplo, somando os preços de todos os itens do pedido
        
    # o codigo comentado acima é um exemplo de como calcular o preço do pedido, mas não está implementado.
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens) 
        #for itens in self.itens: # Percorre todos os itens do pedido (lista de itens)
    
# ItensPedido

class ItemPedido(Base):
     __tablename__ = "itens_pedido"
     
     id = Column("id", Integer, primary_key=True, autoincrement=True)
     quantidade = Column ("quantidade", Integer)
     sabor = Column("sabor", String)
     tamanho = Column("tamanho", String)
     preco_unitario = Column("preco_unitario", Float)
     pedido = Column("pedido", Integer, ForeignKey("pedidos.id"))

     
    
     def  __init__ (self,quantidade, sabor, tamanho, preco_unitario, pedido): 
        
         self.quantidade = quantidade
         self.sabor = sabor
         self.tamanho = tamanho
         self.preco_unitario = preco_unitario
         self.pedido = pedido
     

# executa a criação dos metadados do banco de dados ( cria efetivamente o db)  - Processo de migração