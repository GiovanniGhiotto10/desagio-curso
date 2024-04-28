from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

    contas = relationship("Conta", back_populates="cliente")

class Conta(Base):
    __tablename__ = 'conta'
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    saldo = Column(Integer)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    cliente = relationship("Cliente", back_populates="contas")

# Criando o banco de dados e as tabelas
engine = create_engine('sqlite:///banco.db')
Base.metadata.create_all(engine)

# Criando uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserindo dados de exemplo
cliente1 = Cliente(nome='João', idade=30)
cliente2 = Cliente(nome='Maria', idade=25)
session.add_all([cliente1, cliente2])
session.commit()

conta1 = Conta(numero='123', saldo=1000, cliente=cliente1)
conta2 = Conta(numero='456', saldo=2000, cliente=cliente2)
session.add_all([conta1, conta2])
session.commit()

# Recuperando dados
clientes = session.query(Cliente).all()
for cliente in clientes:
    print(f"Cliente: {cliente.nome}, Idade: {cliente.idade}")
    for conta in cliente.contas:
        print(f"Conta: {conta.numero}, Saldo: {conta.saldo}")

session.close()