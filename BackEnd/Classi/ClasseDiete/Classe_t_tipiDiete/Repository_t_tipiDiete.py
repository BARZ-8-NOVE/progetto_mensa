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
            # Recupera tutti i record dalla tabella TTipiDiete
            results = self.session.query(TTipiDiete).all()
            
            # Trasforma i risultati in un formato JSON serializzabile
            data = [{'id': result.id, 
                    'descrizione': result.descrizione,
                    'note': result.note}
                    for result in results]
            
            return data
        except Exception as e:
            # Restituisce un messaggio di errore e un codice di stato 500
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    


