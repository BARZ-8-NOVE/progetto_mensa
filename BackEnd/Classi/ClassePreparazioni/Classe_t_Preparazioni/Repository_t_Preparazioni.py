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
            return {'Error': str(e)}, 500

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
            return {'Error': str(e)}, 400

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
            return {'preparazione': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete_preparazione(self, id):
        try:
            preparazione = self.session.query(TPreparazioni).filter_by(id=id).first()
            if preparazione:
                preparazione.dataCancellazione = datetime.now()
                preparazione.utenteCancellazione = 'nome_utente'  # Sostituisci con il nome utente appropriato o la fonte dell'azione di cancellazione
                self.session.commit()
                return {'preparazione': 'soft deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
