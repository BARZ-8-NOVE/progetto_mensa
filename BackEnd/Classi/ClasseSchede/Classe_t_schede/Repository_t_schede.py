from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schede.Domani_t_schede import TSchede
from datetime import datetime

class RepositoryTSchede:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TSchede).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 
                'fkTipoAlimentazione': result.fkTipoAlimentazione, 
                'fkTipoMenu': result.fkTipoMenu,
                'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                'nome': result.nome, 
                'titolo': result.titolo, 
                'titolo': result.sottotitolo, 
                'descrizione': result.descrizione, 
                'backgroundColor': result.backgroundColor, 
                'color': result.color, 
                'dipendente': result.dipendente, 
                'note': result.note,
                'inizio': result.inizio,
                'fine': result.fine,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione, 
                'nominativa': result.nominativa 
                 
                } for result in results]
    

