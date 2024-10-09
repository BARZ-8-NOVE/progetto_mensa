from sqlalchemy import Column, Integer, String, Time, Boolean, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TOrariOrdini(Base):
    __tablename__ = 't_order_time_limits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nomeOrdine = Column(String(50), nullable=False)  # Definizione corretta del tipo VARCHAR(50)
    fkServizio = Column(Integer, ForeignKey('t_servizi.id'), nullable=True)  # Definizione corretta della Foreign Key
    tempoLimite = Column(Time, nullable=False)  # TIME in SQL viene tradotto come Time in SQLAlchemy
    ordineDipendente = Column(Boolean, nullable=False, default=True)  # BOOLEAN con default a True
    ordinePerOggi = Column(Boolean, nullable=False, default=True)  # BOOLEAN con default a True
    ultimoUpdated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))  # Timestamp auto-aggiornante
    utenteModifica = Column(String(50), nullable=True)  # Campo utenteModifica, String(50)

    # Relazione con la tabella t_servizi (assuming you have a TServizi class)
    servizi = relationship("TServizi", backref="ordini")

# Se hai una classe TServizi, dovrai anche definirla nella tua applicazione.
