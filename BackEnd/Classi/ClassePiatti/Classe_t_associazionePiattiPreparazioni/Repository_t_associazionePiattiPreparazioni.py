from Classi.ClasseDB.db_connection import engine
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Domain_t_associazionePiattiPreparazioni import TAssociazionePiattiPreparazioni
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class RepositoryAssociazionePiattiPreparazioni:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def get_all(self):
        try:
            results = self.session.query(TAssociazionePiattiPreparazioni).filter(TAssociazionePiattiPreparazioni.dataCancellazione == None).all()
            return [{'id': result.id, 'fkPiatto': result.fkPiatto, 'fkPreparazione': result.fkPreparazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_preparazione_by_piatto(self, fkPiatto):
        try:
            results = self.session.query(TAssociazionePiattiPreparazioni).filter_by(fkPiatto=fkPiatto, dataCancellazione=None).all()
            return [{'id': result.id, 'fkPiatto': result.fkPiatto, 'fkPreparazione': result.fkPreparazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def get_id_piatto_by_preparazione(self, fkPreparazione):
            try:
                result = self.session.query(TAssociazionePiattiPreparazioni).filter_by(fkPreparazione=fkPreparazione, dataCancellazione=None).first()
                return {'id': result.id, 'fkPiatto': result.fkPiatto, 'fkPreparazione': result.fkPreparazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione} 
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 500
            finally:
                # Chiudi sempre la sessione
                self.session.close()

    def get_piatti_by_preparazione(self, fkPreparazione):
            try:
                results = self.session.query(TAssociazionePiattiPreparazioni).filter_by(fkPreparazione=fkPreparazione, dataCancellazione=None).all()
                return [{'id': result.id, 'fkPiatto': result.fkPiatto, 'fkPreparazione': result.fkPreparazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione} for result in results]
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 500
            finally:
                # Chiudi sempre la sessione
                self.session.close()



    def get_id_by_preparazione_e_piatto(self, fkPiatto, fkPreparazione):
        try:
            result = self.session.query(TAssociazionePiattiPreparazioni).filter_by(
                fkPiatto=fkPiatto,
                fkPreparazione=fkPreparazione,
                dataCancellazione=None
            ).first()
            if result:
                return {
                    'id': result.id,
                    'fkPiatto': result.fkPiatto,
                    'fkPreparazione': result.fkPreparazione,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione
                }
            else:
                return {'Error': 'Associazione non trovata'}
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}
        finally:
            # Chiudi sempre la sessione
            self.session.close()



    def get_by_id_ritorno_diz(self, id):
        try:
            results = self.session.query(TAssociazionePiattiPreparazioni).filter_by(id=id, dataCancellazione=None).all()
            if results:
                return [{
                    'id': result.id,
                    'fkPiatto': result.fkPiatto,
                    'fkPreparazione': result.fkPreparazione,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione
                } for result in results]
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_by_id(self, id):
        try:
            result = self.session.query(TAssociazionePiattiPreparazioni).filter_by(id=id, dataCancellazione=None).first()
            if result:
                return {'id': result.id, 'fkPiatto': result.fkPiatto, 'fkPreparazione': result.fkPreparazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def create(self, fkPiatto, fkPreparazione, utenteInserimento, dataInserimento = None):
        try:
            associazione = TAssociazionePiattiPreparazioni (
                fkPiatto=fkPiatto,
                fkPreparazione=fkPreparazione, 
                dataInserimento=dataInserimento, 
                utenteInserimento=utenteInserimento
            )
            self.session.add(associazione)
            self.session.commit()
            return associazione.id
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def update(self, id, fkPiatto, fkPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        try:
            associazione = self.session.query(TAssociazionePiattiPreparazioni).filter_by(id=id).first()
            if associazione:
                associazione.fkPiatto = fkPiatto
                associazione.fkPreparazione = fkPreparazione
                associazione.dataInserimento = dataInserimento
                associazione.utenteInserimento = utenteInserimento
                associazione.dataCancellazione = dataCancellazione
                associazione.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'associazione': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    
    def delete_associazione(self, fkPreparazione, utenteCancellazione):
        try:
            preparazione_contenuto = self.session.query(TAssociazionePiattiPreparazioni).filter_by(fkPreparazione=fkPreparazione).all()
            if preparazione_contenuto:
                for contenuto in preparazione_contenuto:
                    contenuto.dataCancellazione = datetime.now()
                    contenuto.utenteCancellazione = utenteCancellazione  
                self.session.commit()
                return {'preparazioni_contenuti': 'soft deleted!'}, 200
            else:
                return {'Error': f'No match found for this fkPreparazione: {fkPreparazione}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def delete(self, id, utenteCancellazione):
        try:
            associazione = self.session.query(TAssociazionePiattiPreparazioni).filter_by(id=id).first()
            if associazione:
                associazione.dataCancellazione = datetime.now()
                associazione.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'associazione': 'soft deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500       
        finally:
            # Chiudi sempre la sessione
            self.session.close()