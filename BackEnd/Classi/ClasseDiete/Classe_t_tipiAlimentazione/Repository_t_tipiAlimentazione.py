from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseDiete.Classe_t_tipiAlimentazione.Domain_t_tipiAlimentazione import TTipiAlimentazione
from datetime import datetime

class RepositoryTipiAlimentazione:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipiAlimentazione).all()
            # Trasformare i risultati in un formato JSON serializzabile
            data = [{'id': result.id, 
                    'fkTipoDieta': result.fkTipoDieta,
                    'descrizione': result.descrizione,
                    'note': result.note,
                    'ordinatore': result.ordinatore} for result in results]
            return data
        except Exception as e:
            # Restituire un errore e un codice di stato 500
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    


    