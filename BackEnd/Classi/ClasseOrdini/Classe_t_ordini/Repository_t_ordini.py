from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_ordini.Domain_t_ordini import TOrdini
from datetime import datetime

class RepositoryOrdini:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TOrdini).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 
                'data': result.data, 
                 'fkServizio': result.fkServizio
                 } for result in results]

    def get_by_id(self, id):
        try:
            # Esegui la query per recuperare il record con l'id specificato
            result = self.session.query(TOrdini).filter_by(id=id).first()
            
            # Verifica se è stato trovato un record
            if result:
                return {'id': result.id, 
                        'data': result.data, 
                        'fkServizio': result.fkServizio}
            else:
                # Restituisce un messaggio di errore se il record non è stato trovato
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            # Gestisci le eccezioni restituendo un messaggio di errore e un codice di stato 400
            return {'Error': str(e)}, 400
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def existing_Ordine(self, data, fkServizio):
        try:
            result = self.session.query(TOrdini).filter_by(data=data, fkServizio=fkServizio).first()
            if result:
                return {'id': result.id, 
                        'data': result.data, 
                        'fkServizio': result.fkServizio
                    }
            else:
                return None  # Restituisce None se l'ordine non esiste
        except Exception as e:
            return {'Error': str(e)}, 400
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()


    def get_ordini_by_data(self, data, fkServizio):
        try:
            results = self.session.query(TOrdini).filter_by(data=data, fkServizio=fkServizio).all()
            return [{'id': result.id, 'data': result.data, 'fkServizio': result.fkServizio} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 400
        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()

    def create(self, data, fkServizio):
        try:

            if self.existing_Ordine(data, fkServizio):
                # Se esiste, restituisce un messaggio di errore
                return {'Error': 'Elemento già esistente'}, 400
                
            ordine = TOrdini(

                data=data, 
                fkServizio=fkServizio

            )
            self.session.add(ordine)
            self.session.commit()
            return ordine.id
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

        finally:
                    # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                    if self.session:
                        self.session.close()


