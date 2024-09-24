from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schedePiatti.Domain_t_schedePiatti import TSchedePiatti
from datetime import datetime

class RepositoryTSchedePiatti:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()




    def get_by_id(self, id):
        try:
            result = self.session.query(TSchedePiatti).filter_by(id=id, dataCancellazione=None).first()
            if result:
                return {'id': result.id, 
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



    def get_piatti_by_scheda(self, fkScheda):
        try:
            # Esegui la query per ottenere tutti i piatti associati a una specifica scheda
            results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'ordinatore': result.ordinatore,
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


    def get_piatti_non_dolci_by_scheda(self, fkScheda, fkServizio):
        try:
            # Esegui la query per ottenere tutti i piatti non dolci per una specifica scheda e servizio
            results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.colonna != 2,
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.fkServizio == fkServizio,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'ordinatore': result.ordinatore,
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


    def get_dolci_pane_by_scheda(self, fkScheda, fkServizio):
        try:
            # Esegui la query per ottenere i dolci e il pane associati a una specifica scheda e servizio
            results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.colonna == 2,
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.fkServizio == fkServizio,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'ordinatore': result.ordinatore,
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


    def get_piatti_by_scheda_and_servizio(self, fkScheda, fkServizio):
        try:
            # Esegui la query per ottenere i piatti associati a una specifica scheda e servizio
            results = self.session.query(TSchedePiatti).filter(
                TSchedePiatti.fkScheda == fkScheda,
                TSchedePiatti.fkServizio == fkServizio,
                TSchedePiatti.dataCancellazione.is_(None)
            ).order_by(TSchedePiatti.ordinatore).all()
            
            # Costruisci la lista dei risultati
            return [{
                'id': result.id, 
                'note': result.note,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'fkPiatto': result.fkPiatto,
                'colonna': result.colonna,
                'riga': result.riga,
                'ordinatore': result.ordinatore,
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


    def create(self, fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, utenteInserimento):
        try:
            scheda = TSchedePiatti(
                fkScheda=fkScheda,
                fkServizio=fkServizio,
                fkPiatto=fkPiatto, 
                colonna=colonna,
                riga=riga,
                note=note,
                ordinatore=ordinatore,
                utenteInserimento=utenteInserimento, 

            )
            self.session.add(scheda)
            self.session.commit()
            return 
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()
            

    def update(self, id , fkScheda, fkServizio, fkPiatto, colonna, riga, note, ordinatore, utenteInserimento):
        try:
            scheda = self.session.query(TSchedePiatti).filter_by(id=id).first()
            if scheda:
                scheda.id = id
                scheda.fkScheda = fkScheda
                scheda.fkServizio = fkServizio
                scheda.fkPiatto = fkPiatto
                scheda.colonna = colonna
                scheda.riga = riga
                scheda.note = note
                scheda.ordinatore = ordinatore
                scheda.utenteInserimento = utenteInserimento

                
                self.session.commit()
                return {'Message': 'Scheda updated successfully!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def delete_piatti_Scheda(self, fkScheda, utenteCancellazione):
        try:
            # Ottieni tutte le associazioni corrispondenti a fkMenuServizio
            piattiScheda = self.session.query(TSchedePiatti).filter_by(fkScheda=fkScheda).all()
            
            # Se non ci sono associazioni, restituisci un errore
            if not piattiScheda:
                return {'Error': f'No match found for fkMenuServizio: {fkScheda}'}, 404
            
            # Esegui la soft delete per ciascuna associazione
            for associazione in piattiScheda:
                associazione.dataCancellazione = datetime.now()
                associazione.utenteCancellazione = utenteCancellazione
            
            # Commit le modifiche
            self.session.commit()
            return {'associazione': 'soft deleted!'}, 200
            
        except Exception as e:
            # Esegui il rollback in caso di errore
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def crea_piatto_vuoto(self, id):
        try:
            # Ottieni tutte le associazioni corrispondenti a fkMenuServizio
            piattiScheda = self.session.query(TSchedePiatti).filter_by(id=id).first()
            
            # Se non ci sono associazioni, restituisci un errore
            if not piattiScheda:
                return {'Error': f'No match found for id: {id}'}, 404
            
            # Esegui la "soft delete" impostando il campo fkPiatto a None
            piattiScheda.fkPiatto = None
            
            # Commit le modifiche
            self.session.commit()
            return {'message': 'Soft delete successful!'}, 200
            
        except Exception as e:
            # Esegui il rollback in caso di errore
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def delete_piatto_singolo(self, id, utenteCancellazione):
        try:
            # Ottieni l'associazione corrispondente a fkMenuServizio
            piattiScheda = self.session.query(TSchedePiatti).filter_by(id=id).first()
            
            # Se non ci sono associazioni, restituisci un errore
            if not piattiScheda:
                return {'Error': f'No match found for id: {id}'}, 404
            
            # Esegui la "soft delete" impostando il campo dataCancellazione e utenteCancellazione
            piattiScheda.dataCancellazione = datetime.now()
            piattiScheda.utenteCancellazione = utenteCancellazione
            
            # Commit le modifiche
            self.session.commit()
            return {'message': 'Soft delete successful!'}, 200
        
        except Exception as e:
            # Esegui il rollback in caso di errore
            self.session.rollback()
            # Log dell'errore (opzionale)
            # log.error(f"Error during soft delete: {str(e)}")
            return {'Error': str(e)}, 500
        
        finally:
            # Chiudi sempre la sessione
            self.session.close()