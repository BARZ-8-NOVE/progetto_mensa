from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseDiete.Classe_t_tipiAlimentazione.Domain_t_tipAlimentazione import TTipiAlimentazione
from datetime import datetime

class RepositoryTipiAlimentazione:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipiAlimentazione).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 
                 'fkTipoDieta': result.fkTipoDieta,
                 'descrizione': result.descrizione,
                 'note': result.note,
                 'ordinatore': result.ordinatore} for result in results]
    


    