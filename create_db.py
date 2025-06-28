from models import Base, db

Base.metadata.create_all(bind=db)
print("Banco criado com sucesso!")