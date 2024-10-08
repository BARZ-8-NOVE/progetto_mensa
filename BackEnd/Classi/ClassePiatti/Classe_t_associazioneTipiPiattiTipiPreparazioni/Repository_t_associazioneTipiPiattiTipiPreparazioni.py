from Classi.ClasseDB.db_connection import engine
from Classi.ClassePiatti.Classe_t_associazioneTipiPiattiTipiPreparazioni.Domain_t_associazioneTipiPiattiTipiPreparazioni import TAssociazioneTipiPiattiTipiPreparazioni
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class RepositoryAssociazioneTipiPiattiTipiPreparazioni:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def get_all(self):
        try:
            results = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni).filter(TAssociazioneTipiPiattiTipiPreparazioni.dataCancellazione == None).all()
            return [{'id': result.id, 
                     'fkTipoPiatto': result.fkTipoPiatto, 
                     'fkTipoPreparazione': result.fkTipoPreparazione, 
                     'dataInserimento': result.dataInserimento, 
                     'utenteInserimento': result.utenteInserimento, 
                     'dataCancellazione': result.dataCancellazione, 
                     'utenteCancellazione': result.utenteCancellazione} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_tipoPreparazione_by_TipoPiatto(self, fkTipoPiatto):
        try:
            results = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni).filter_by(fkTipoPiatto=fkTipoPiatto, dataCancellazione=None).all()
            return [{'id': result.id, 
                     'fkTipoPiatto': result.fkTipoPiatto, 
                     'fkTipoPreparazione': result.fkTipoPreparazione, 
                     'dataInserimento': result.dataInserimento, 
                     'utenteInserimento': result.utenteInserimento, 
                     'dataCancellazione': result.dataCancellazione, 
                     'utenteCancellazione': result.utenteCancellazione} for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def get_fkTipoPatto_by_fkTipoPeparazione(self, fkTipoPreparazione):
            try:
                # Query the association table for matching dish types based on preparation type
                piatti_associati = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni) \
                    .filter_by(fkTipoPreparazione=fkTipoPreparazione, dataCancellazione=None).all()
                
                # Extract and return the fkTipoPiatto values
                if piatti_associati:
                    return [associazione.fkTipoPiatto for associazione in piatti_associati]
                else:
                    return None
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 500
            finally:
                # Chiudi sempre la sessione
                self.session.close()


    def get_by_id(self, id):
        try:
            result = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni).filter_by(id=id, dataCancellazione=None).first()
            if result:
                return {'id': result.id, 'fkTipoPiatto': result.fkTipoPiatto, 'fkTipoPreparazione': result.fkTipoPreparazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def create(self, fkTipoPiatto, fkTipoPreparazione, utenteInserimento, dataInserimento = None):
        try:
            associazione = TAssociazioneTipiPiattiTipiPreparazioni (
                fkTipoPiatto=fkTipoPiatto,
                fkTipoPreparazione=fkTipoPreparazione, 
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


    def update(self, id, fkTipoPiatto, fkTipoPreparazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        try:
            associazione = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni).filter_by(id=id).first()
            if associazione:
                associazione.fkTipoPiatto = fkTipoPiatto
                associazione.fkTipoPreparazione = fkTipoPreparazione
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


    
    def delete_associazione(self, fkTipoPreparazione, utenteCancellazione):
        try:
            preparazione_contenuto = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni).filter_by(fkTipoPreparazione=fkTipoPreparazione).all()
            if preparazione_contenuto:
                for contenuto in preparazione_contenuto:
                    contenuto.dataCancellazione = datetime.now()
                    contenuto.utenteCancellazione = utenteCancellazione  
                self.session.commit()
                return {'preparazioni_contenuti': 'soft deleted!'}, 200
            else:
                return {'Error': f'No match found for this fkTipoPreparazione: {fkTipoPreparazione}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def delete(self, id, utenteCancellazione):
        try:
            associazione = self.session.query(TAssociazioneTipiPiattiTipiPreparazioni).filter_by(id=id).first()
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