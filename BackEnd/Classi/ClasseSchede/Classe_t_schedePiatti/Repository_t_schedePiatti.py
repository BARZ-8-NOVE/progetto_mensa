from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schedePiatti.Domain_t_schedePiatti import TSchedePiatti
from datetime import datetime

class RepositoryTSchedePiatti:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TSchedePiatti).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 
  
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'note': result.note,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione

                 
                } for result in results]
 