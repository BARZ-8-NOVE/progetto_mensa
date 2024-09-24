from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePiatti.Classe_t_piatti.Domain_t_piatti import TPiatti
import logging
from datetime import datetime

# Configura il logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RepositoryPiatti:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def get_all(self):
        try:
            results = self.session.query(TPiatti).filter(TPiatti.dataCancellazione == None).all()
            return [{'id': result.id, 'fkTipoPiatto': result.fkTipoPiatto, 'codice': result.codice, 'titolo': result.titolo, 'descrizione': result.descrizione, 'inMenu': result.inMenu, 'ordinatore': result.ordinatore, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione} for result in results]
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error getting all piatti: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati di chiudere la sessione, se necessario
            self.session.close()

    def get_by_id(self, id):
        try:
            result = self.session.query(TPiatti).filter_by(id=id, dataCancellazione=None).first()
            if result:
                return {'id': result.id, 'fkTipoPiatto': result.fkTipoPiatto, 'codice': result.codice, 'titolo': result.titolo, 'descrizione': result.descrizione, 'inMenu': result.inMenu, 'ordinatore': result.ordinatore, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error getting piatto by ID {id}: {e}")
            return {'Error': str(e)}, 400
        finally:
            # Assicurati di chiudere la sessione, se necessario
            self.session.close()      
        
    def get_by_fkTipoPiatto(self, fkTipoPiatto):
        try:
            results = self.session.query(TPiatti).filter_by(fkTipoPiatto=fkTipoPiatto, dataCancellazione=None).all()
            return [{'id': result.id, 'titolo': result.titolo} for result in results]
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error getting piatti by fkTipoPiatto: {e}")
            return []
        finally:
            # Assicurati di chiudere la sessione, se necessario
            self.session.close()


    def create(self, fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, utenteInserimento, dataInserimento=None):
        try:
            piatto = TPiatti(
                fkTipoPiatto=fkTipoPiatto, 
                codice=codice, 
                titolo=titolo, 
                descrizione=descrizione, 
                inMenu=inMenu, 
                ordinatore=ordinatore, 
                dataInserimento=dataInserimento, 
                utenteInserimento=utenteInserimento
            )
            self.session.add(piatto)
            self.session.commit()

            return {'piatto': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Assicurati di chiudere la sessione, se necessario
            self.session.close()
        
    def update(self, id, fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, utenteInserimento):
        try:
            piatto = self.session.query(TPiatti).filter_by(id=id).first()
            if piatto:
                piatto.fkTipoPiatto = fkTipoPiatto
                piatto.codice = codice
                piatto.titolo = titolo
                piatto.descrizione = descrizione
                piatto.inMenu = inMenu
                piatto.ordinatore = ordinatore
                piatto.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'piatto': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating piatto with ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati di chiudere la sessione, se necessario
            self.session.close()


    def delete(self, id, utenteCancellazione):
        try:
            piatto = self.session.query(TPiatti).filter_by(id=id).first()
            if piatto:
                piatto.dataCancellazione = datetime.now()
                piatto.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'piatto': 'soft deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
                # Assicurati di chiudere la sessione, se necessario
                self.session.close()