from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schedePreconfezionatePiatti.Domain_t_schedePreconfezionatePiatti import TSchedePreconfezionatePiatti
from datetime import datetime

class RepositoryTSchedePreconfezionatePiatti:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()



    def get_by_id(self, id):
        try:
            result = self.session.query(TSchedePreconfezionatePiatti).filter_by(id=id, dataCancellazione=None).first()
            if result:
                return {'id': result.id, 
                        'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                        'fkPiatto': result.fkPiatto,
                        'quantita': result.quantita,
                        'dataInserimento': result.dataInserimento, 
                        'utenteInserimento': result.utenteInserimento, 
                        'dataCancellazione': result.dataCancellazione, 
                        'utenteCancellazione': result.utenteCancellazione}
            else:
                return None
        except Exception as e:
            # In caso di errore, esegui il rollback della transazione
            self.session.rollback()
            return {'error': str(e)}
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()



    def get_piatti_by_scheda(self, fkSchedaPreconfezionata):
        try:
            # Esegui la query per ottenere tutti i piatti associati a una specifica scheda
            results = self.session.query(TSchedePreconfezionatePiatti).filter(
                TSchedePreconfezionatePiatti.fkSchedaPreconfezionata == fkSchedaPreconfezionata,
                TSchedePreconfezionatePiatti.dataCancellazione.is_(None)
            ).order_by().all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'fkSchedaPreconfezionata': result.fkSchedaPreconfezionata, 
                'fkPiatto': result.fkPiatto,
                'quantita': result.quantita,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
        
        except Exception as e:
            # In caso di errore, esegui il rollback della transazione
            self.session.rollback()
            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def create(self, fkSchedaPreconfezionata, fkPiatto, quantita, utenteInserimento):
        try:
            scheda = TSchedePreconfezionatePiatti(
                fkSchedaPreconfezionata=fkSchedaPreconfezionata, 
                fkPiatto=fkPiatto,
                quantita=quantita,
                utenteInserimento=utenteInserimento
            )

            # Aggiungi l'oggetto alla sessione
            self.session.add(scheda)

            # Esegui il commit
            self.session.commit()

            print("Scheda aggiunta con successo!")
            return {'Message': 'Scheda added successfully!'}, 200

        except Exception as e:
            # Rollback in caso di errore
            self.session.rollback()

            # Stampa l'errore per il debug
            print(f"Error during database commit: {str(e)}")

            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def update(self, id, fkSchedaPreconfezionata, fkPiatto, quantita, utenteInserimento):
        try:
            scheda = self.session.query(TSchedePreconfezionatePiatti).filter_by(id=id).first()
            if scheda:
                scheda.id = id
                scheda.fkSchedaPreconfezionata=fkSchedaPreconfezionata, 
                scheda.fkPiatto=fkPiatto,
                scheda.quantita=quantita,
                scheda.utenteInserimento=utenteInserimento,
                scheda.utenteInserimento = utenteInserimento

                self.session.commit()
                return {'Message': 'Scheda updated successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        
        finally:
                # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                if self.session:
                    self.session.close()


    def delete(self, id, utenteCancellazione):
        try:
            scheda = self.session.query(TSchedePreconfezionatePiatti).filter_by(id=id).first()
            if scheda:
                scheda.dataCancellazione = datetime.now()
                scheda.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'Message': 'Scheda deleted successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        
        finally:
                # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                if self.session:
                    self.session.close()