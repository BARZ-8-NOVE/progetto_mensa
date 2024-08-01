from sqlalchemy import Column, Integer, String, Text, Date, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TSchede(Base):
    __tablename__ = 't_schede'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fkTipoAlimentazione = Column(Integer, ForeignKey('t_tipialimentazione.id'), nullable=True)
    fkTipoMenu = Column(Integer, ForeignKey('t_tipimenu.id'), nullable=True)
    fkSchedaPreconfezionata = Column(Integer, nullable=True)  # Se non è una chiave esterna, usa Column(Integer)
    nome = Column(String(50), nullable=True)
    titolo = Column(String(100), nullable=True)
    sottotitolo = Column(String(100), nullable=True)
    descrizione = Column(String(50), nullable=True)
    backgroundColor = Column(String(7), nullable=True)
    color = Column(String(7), nullable=True)
    dipendente = Column(SmallInteger, default=0, nullable=False)
    note = Column(Text, nullable=True)
    inizio = Column(Date, nullable=True)
    fine = Column(Date, nullable=True)
    ordinatore = Column(Integer, default=0, nullable=False)
    dataInserimento = Column(DateTime(timezone=True), nullable=True)
    utenteInserimento = Column(String(20), nullable=True)
    dataCancellazione = Column(DateTime(timezone=True), nullable=True)
    utenteCancellazione = Column(String(20), nullable=True)
    nominativa = Column(SmallInteger, default=1, nullable=False)

    # Definizione delle relazioni
    tipo_alimentazione = relationship('TTipiAlimentazione', backref='schede')
    tipo_menu = relationship('TTipiMenu', backref='schede')


