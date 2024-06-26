import logging
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePiatti.Classe_t_tipiPiatti.Domani_t_tipiPiatti import TTipiPiatti
import datetime
class RepositoryTipiPiatti:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipiPiatti).all()
            return [
                {
                    'id': result.id,
                    'descrizione': result.descrizione,
                    'descrizionePlurale': result.descrizionePlurale,
                    'inMenu': result.inMenu,
                    'ordinatore': result.ordinatore,
                    'color': result.color,
                    'backgroundColor': result.backgroundColor,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                } for result in results
            ]
        except Exception as e:
            logging.error(f"Error getting all tipi piatti: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TTipiPiatti).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'descrizione': result.descrizione,
                    'descrizionePlurale': result.descrizionePlurale,
                    'inMenu': result.inMenu,
                    'ordinatore': result.ordinatore,
                    'color': result.color,
                    'backgroundColor': result.backgroundColor,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                }
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting tipo piatto by ID {id}: {e}")
            return {'Error': str(e)}, 400

    def create(self, descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento):
        try:
            tipipiatto = TTipiPiatti(
                descrizione=descrizione,
                descrizionePlurale=descrizionePlurale,
                inMenu=inMenu,
                ordinatore=ordinatore,
                color=color,
                backgroundColor=backgroundColor,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento
            )
            self.session.add(tipipiatto)
            self.session.commit()
            return {'tipipiatto': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def update(self, id, descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        try:
            tipipiatto = self.session.query(TTipiPiatti).filter_by(id=id).first()
            if tipipiatto:
                tipipiatto.descrizione = descrizione
                tipipiatto.descrizionePlurale = descrizionePlurale
                tipipiatto.inMenu = inMenu
                tipipiatto.ordinatore = ordinatore
                tipipiatto.color = color
                tipipiatto.backgroundColor = backgroundColor
                tipipiatto.dataInserimento = dataInserimento
                tipipiatto.utenteInserimento = utenteInserimento
                tipipiatto.dataCancellazione = dataCancellazione
                tipipiatto.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'tipipiatto': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete(self, id, utenteCancellazione):
        try:
            tipo_piatto = self.session.query(TTipiPiatti).filter_by(id=id).first()
            if tipo_piatto:
                tipo_piatto.dataCancellazione = datetime.now()
                tipo_piatto.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'tipo_piatto': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting tipo piatto by ID {id}: {e}")
            return {'Error': str(e)}, 500
