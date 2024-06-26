from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

username = 'root'
password = 'Mulini24!'
host = '127.0.0.1'
port = '3306'
database = 'cucina'

engine = create_engine(f'mysql+mysqldb://{username}:{password}@{host}:{port}/{database}')

Base = declarative_base()

class t_utente(Base):
    __tablename__ = 't_utenti'
    id = Column(Integer, primary_key= True, autoincrement= True)
    username = Column(String(50))

Base.metadata.create_all(engine)