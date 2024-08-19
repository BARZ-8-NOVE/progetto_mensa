from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Domani_t_preparazionicontenuti import TPreparazioniContenuti
from datetime import datetime

class Repository_t_preparazionicontenuti:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_preparazioni_contenuti(self):
        try:
            results = self.session.query(TPreparazioniContenuti).filter(TPreparazioniContenuti.dataCancellazione.is_(None)).all()
            return [{
                'id': result.id,
                'fkPreparazione': result.fkPreparazione,
                'fkAlimento': result.fkAlimento,
                'quantita': result.quantita,
                'fkTipoQuantita': result.fkTipoQuantita,
                'note': result.note,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
            
        except Exception as e:
            return {'Error': str(e)}, 500

        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def get_preparazioni_contenuti_by_id(self, id):
        try:
            result = self.session.query(TPreparazioniContenuti).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'fkPreparazione': result.fkPreparazione,
                    'fkAlimento': result.fkAlimento,
                    'quantita': result.quantita,
                    'fkTipoQuantita': result.fkTipoQuantita,
                    'note': result.note,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione
                }
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400
        
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def get_preparazioni_contenuti_by_id_preparazione(self, fkPreparazione):
        try:
            results = self.session.query(TPreparazioniContenuti).filter_by(fkPreparazione=fkPreparazione).filter(TPreparazioniContenuti.dataCancellazione.is_(None)).all()

            if not results:
                return {'Error': f'No match found for fkPreparazione: {fkPreparazione}'}, 404

            return [{
                'id': result.id,
                'fkPreparazione': result.fkPreparazione,
                'fkAlimento': result.fkAlimento,
                'quantita': result.quantita,
                'fkTipoQuantita': result.fkTipoQuantita,
                'note': result.note,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione
            } for result in results]
        
        except Exception as e:
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def create_preparazioni_contenuti(self, fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None):
        try:
            preparazione_contenuto = TPreparazioniContenuti(
                fkPreparazione=fkPreparazione,
                fkAlimento=fkAlimento,
                quantita=quantita,
                fkTipoQuantita=fkTipoQuantita,
                note=note,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento,
                dataCancellazione=dataCancellazione,
                utenteCancellazione=utenteCancellazione
            )
            self.session.add(preparazione_contenuto)
            self.session.commit()
            return {'preparazioni_contenuti': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def update_preparazioni_contenuti(self, id: int, fkPreparazione: int, fkAlimento: int, quantita: float,
                                      fkTipoQuantita: int, note: str, dataInserimento=None,
                                      utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None):
        try:
            preparazione_contenuto = self.session.query(TPreparazioniContenuti).filter_by(id=id).first()
            if preparazione_contenuto:
                preparazione_contenuto.fkPreparazione = fkPreparazione
                preparazione_contenuto.fkAlimento = fkAlimento
                preparazione_contenuto.quantita = quantita
                preparazione_contenuto.fkTipoQuantita = fkTipoQuantita
                preparazione_contenuto.note = note
                preparazione_contenuto.dataInserimento = dataInserimento
                preparazione_contenuto.utenteInserimento = utenteInserimento
                preparazione_contenuto.dataCancellazione = dataCancellazione
                preparazione_contenuto.utenteCancellazione = utenteCancellazione

                self.session.commit()
                return {'preparazioni_contenuti': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def delete(self, fkPreparazione, utenteCancellazione):
        try:
            preparazione_contenuto = self.session.query(TPreparazioniContenuti).filter_by(fkPreparazione=fkPreparazione).all()
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
