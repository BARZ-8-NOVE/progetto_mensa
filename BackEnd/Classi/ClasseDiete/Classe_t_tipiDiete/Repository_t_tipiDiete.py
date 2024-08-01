from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseDiete.Classe_t_tipiDiete.Domain_t_tipiDiete import TTipiDiete
from datetime import datetime

class RepositoryTipiDiete:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipiDiete).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 
                 'descrizione': result.descrizione,
                 'note': result.note,
                } for result in results]
    

    


