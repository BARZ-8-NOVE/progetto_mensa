from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Domain_t_preparazioni import TPreparazioni
from datetime import datetime


class Repository_t_preparazioni:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_preparazioni(self):
        try:
            results = self.session.query(TPreparazioni).filter(TPreparazioni.dataCancellazione.is_(None)).all()
            return [{
                'id': result.id,
                'fkTipoPreparazione': result.fkTipoPreparazione,
                'descrizione': result.descrizione,
                'isEstivo': result.isEstivo,
                'isInvernale': result.isInvernale,
                'allergeni': result.allergeni,
                'inizio': result.inizio,
                'fine': result.fine,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione,
                'immagine': result.immagine
            } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close
                        

    def get_all_preparazioni_base(self):
        try:
            results = self.session.query(TPreparazioni).filter(
                TPreparazioni.fkTipoPreparazione == 1,
                TPreparazioni.dataCancellazione.is_(None)
            ).all()
            return [{
                'id': result.id,
                'fkTipoPreparazione': result.fkTipoPreparazione,
                'descrizione': result.descrizione,
                'isEstivo': result.isEstivo,
                'isInvernale': result.isInvernale,
                'allergeni': result.allergeni,
                'inizio': result.inizio,
                'fine': result.fine,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione,
                'immagine': result.immagine
            } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close


    def  get_descrizione_by_id(self, id):
        try:
            result = self.session.query(TPreparazioni).filter_by(id=id).first()
            if result:
                return result.descrizione

            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            if self.session:
                self.session.close

                
    def update(self, id, fkTipoPreparazione, descrizione, isEstivo, isInvernale, inizio, fine, immagine):
        try:
            preparazione = self.session.query(TPreparazioni).filter_by(id=id).first()
            if preparazione:
                preparazione.fkTipoPreparazione = fkTipoPreparazione
                preparazione.descrizione = descrizione
                preparazione.isEstivo = isEstivo
                preparazione.isInvernale = isInvernale
                preparazione.inizio = inizio
                preparazione.fine = fine
                preparazione.immagine = immagine
                self.session.commit()
                return {'preparazione': 'updated!', 'id': id}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()



    def get_preparazione_by_id(self, id):
        try:
            result = self.session.query(TPreparazioni).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'fkTipoPreparazione': result.fkTipoPreparazione,
                    'descrizione': result.descrizione,
                    'isEstivo': result.isEstivo,
                    'isInvernale': result.isInvernale,
                    'allergeni': result.allergeni,
                    'inizio': result.inizio,
                    'fine': result.fine,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                    'immagine': result.immagine
                }
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def create_preparazione(self, fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni=None, inizio=None, fine=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None, immagine=None):
        try:
            preparazione = TPreparazioni(
                fkTipoPreparazione=fkTipoPreparazione,
                descrizione=descrizione,
                isEstivo=isEstivo,
                isInvernale=isInvernale,
                allergeni=allergeni,
                inizio=inizio,
                fine=fine,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento,
                dataCancellazione=dataCancellazione,
                utenteCancellazione=utenteCancellazione,
                immagine=immagine
            )
            self.session.add(preparazione)
            self.session.commit()
            return preparazione.id
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_last_id(self):
            try:
                # Fetch the last record by ordering by the primary key in descending order
                result = self.session.query(TPreparazioni).filter(TPreparazioni.dataCancellazione.is_(None)).order_by(TPreparazioni.id.desc()).first()
                
                if result:
                    return {'id': result.id}
                else:
                    return {'Error': 'No match found'}, 404
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 400
            finally:
                # Chiudi sempre la sessione
                self.session.close()


    def delete(self, id, utenteCancellazione):
        try:
            menu = self.session.query(TPreparazioni).filter_by(id=id).first()
            if menu:
                menu.dataCancellazione = datetime.now()
                menu.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'menu': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close() 
