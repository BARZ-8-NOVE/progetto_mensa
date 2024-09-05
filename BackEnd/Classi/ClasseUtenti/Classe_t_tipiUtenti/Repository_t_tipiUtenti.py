from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import NotFound
import logging

class Repository_t_tipiUtente:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_tipoUtente_by_id(self, id:int):
        result = self.session.query(TTipiUtenti).filter_by(id=id).first()
        return result
    
    def exists_tipoUtente_by_nomeTipoUtente(self, nomeTipoUtente):
        result = self.session.query(TTipiUtenti).filter_by(nomeTipoUtente=nomeTipoUtente).first()
        return result.id
    
    def set_null_fkAutorizzazioni(self, fkAutorizzazioni):
        results = self.session.query(TTipiUtenti).filter_by(fkAutorizzazioni=fkAutorizzazioni).all()
        for result in results:
            result.fkAutorizzazioni = None
            self.session.commit()
        return
    


    def get_by_id(self, id):
        try:
            result = self.session.query(TTipiUtenti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'nomeTipoUtente': result.nomeTipoUtente}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting alimento by ID {id}: {e}")
            return {'Error': str(e)}, 400
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

        
    def get_tipiUtenti_all(self):
        try:
            results = self.session.query(TTipiUtenti).all()
            return [{'id': result.id, 'nomeTipoUtente': result.nomeTipoUtente} for result in results]

        except Exception as e:
            # Se si verifica un'eccezione, esegui il rollback della sessione
            self.session.rollback()
            return {'Error': str(e)}, 500

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            self.session.close()


    def create(self, nomeTipoUtente, fkAutorizzazioni=None):
        try:
            # Crea l'oggetto TSchede
            tipo_utente = TTipiUtenti(
                nomeTipoUtente=nomeTipoUtente,
                fkAutorizzazioni=fkAutorizzazioni,
            )

            # Aggiungi l'oggetto alla sessione
            self.session.add(tipo_utente)

            # Esegui il commit
            self.session.commit()

            # Ottieni l'ID del nuovo tipo utente
            new_id = tipo_utente.id

            print(f"Tipo utente aggiunto con successo! ID: {new_id}")
            return new_id

        except Exception as e:
            # Rollback in caso di errore
            self.session.rollback()

            # Stampa l'errore per il debug
            print(f"Errore durante il commit al database: {str(e)}")

            return {'Error': str(e)}, 500

        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()


    def update(self, id, nomeTipoUtente, fkAutorizzazioni=None):
        try:
            tipoUtente = self.session.query(TTipiUtenti).filter_by(id=id).first()
            if tipoUtente:
                tipoUtente.nomeTipoUtente = nomeTipoUtente
                tipoUtente.fkAutorizzazioni = fkAutorizzazioni
            
                self.session.commit()
                return {'alimento': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating tipo utente with ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()


   
    
    def update_tipoUtente_nomeTipoUtente(self, id:int, nomeTipoUtente:str):
        tipoUtente:TTipiUtenti = self.exists_tipoUtente_by_id(id)
        if tipoUtente:
            tipoUtente.nomeTipoUtente = nomeTipoUtente
            self.session.commit()
        else:
            raise NotFound('TipoUtente', 'id', id)
        
   
        
    def delete_tipoUtente(self, id:int):
        result = self.exists_tipoUtente_by_id(id)
        if result:
            from Classi.ClasseUtenti.Classe_t_utenti.Repository_t_utenti import Repository_t_utenti
            utenti = Repository_t_utenti()
            results = utenti.exist_utenti_by_tipoUtente(result.id)
            if not results:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return
            else:
                return results
        else:
            self.session.close()
            raise NotFound('TipoUtente', 'id', id)
        