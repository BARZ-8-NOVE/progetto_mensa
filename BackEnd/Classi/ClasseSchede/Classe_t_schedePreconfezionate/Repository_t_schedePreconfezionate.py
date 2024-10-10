from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseSchede.Classe_t_schedePreconfezionate.Domani_t_schedePreconfezionate import TSchedePreconfezionate
from datetime import datetime

class RepositoryTSchedePreconfezionate:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()





    def get_by_id(self, id):
            try:
                result = self.session.query(TSchedePreconfezionate).filter_by(id=id).first()
                if result:
                    return {                
                        'id': result.id,
                        'fkScheda' : result.fkScheda,
                        'fkServizio': result.fkServizio,
                        'note' : result.note,
                        'descrizione': result.descrizione, 
                        'ordinatore': result.ordinatore,
                        'dataInserimento': result.dataInserimento, 
                        'utenteInserimento': result.utenteInserimento, 
                        'dataCancellazione': result.dataCancellazione, 
                        'utenteCancellazione': result.utenteCancellazione
                 
                    }
                else:
                    return {'Error': f'No match found for this id: {id}'}, 404
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 400
            
            finally:
                # Assicurati che la sessione venga chiusa per evitare perdite di risorse
                if self.session:
                    self.session.close()


    def get_all(self):
        try:
            # Esegui la query per ottenere tutti i risultati non cancellati
            results = self.session.query(TSchedePreconfezionate).filter(TSchedePreconfezionate.dataCancellazione.is_(None)).all()
            
            # Costruisci la lista dei risultati
            output = [{
                'id': result.id,
                'fkScheda' : result.fkScheda,
                'fkServizio': result.fkServizio,
                'note' : result.note,
                'descrizione': result.descrizione, 
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento, 
                'utenteInserimento': result.utenteInserimento, 
                'dataCancellazione': result.dataCancellazione, 
                'utenteCancellazione': result.utenteCancellazione
                    } for result in results]
            return output
        
        except Exception as e:
            self.session.rollback()
            # Log dell'errore (opzionale)
            # log.error(f"Error fetching data: {str(e)}")
            return {'Error': str(e)}, 500
        
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def get_all_by_fk_scheda(self, fkScheda):
        try:
            # Esegui la query per ottenere tutti i risultati non cancellati con fkScheda specifico
            results = self.session.query(TSchedePreconfezionate).filter(
                TSchedePreconfezionate.fkScheda == fkScheda,
                TSchedePreconfezionate.dataCancellazione.is_(None)
            ).order_by(
                TSchedePreconfezionate.fkServizio,
                TSchedePreconfezionate.ordinatore
            ).all()

            # Costruisci la lista dei risultati
            output = [{
                'id': result.id,
                'fkScheda': result.fkScheda,
                'fkServizio': result.fkServizio,
                'note': result.note,
                'descrizione': result.descrizione,
                'ordinatore': result.ordinatore,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
            
            return output

        except Exception as e:
            self.session.rollback()
            # Log dell'errore (opzionale)
            # log.error(f"Error fetching data: {str(e)}")
            return {'Error': str(e)}, 500

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def create(self, fkScheda, fkServizio, descrizione, note, ordinatore, utenteInserimento):
        try:
            scheda = TSchedePreconfezionate(
                fkScheda=fkScheda,
                fkServizio=fkServizio,
                descrizione=descrizione,
                note=note,
                ordinatore=ordinatore,
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


    def update(self, id, fkServizio, descrizione, note, ordinatore, utenteInserimento):
        try:
            scheda = self.session.query(TSchedePreconfezionate).filter_by(id=id).first()
            if scheda:
                scheda.id = id
                scheda.fkServizio=fkServizio,
                scheda.descrizione=descrizione,
                scheda.note=note,
                scheda.ordinatore=ordinatore,
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
            scheda = self.session.query(TSchedePreconfezionate).filter_by(id=id).first()
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