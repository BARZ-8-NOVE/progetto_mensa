import logging
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from datetime import datetime
from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi

class RepositoryMenuServizi:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TMenuServizi).all()
            return [
                {
                    'id': result.id,
                    'fkMenu': result.fkMenu,
                    'fkServizio': result.fkServizio,
                    'note': result.note,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                } for result in results
            ]
        except Exception as e:
            logging.error(f"Error getting all menu servizi: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TMenuServizi).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'fkMenu': result.fkMenu,
                    'fkServizio': result.fkServizio,
                    'note': result.note,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                }
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting menu servizi by ID {id}: {e}")
            return {'Error': str(e)}, 400

    def create(self, fkMenu, fkServizio, note, dataInserimento, utenteInserimento):
        try:
            menu_servizi = TMenuServizi(
                fkMenu=fkMenu,
                fkServizio=fkServizio,
                note=note,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento
            )
            self.session.add(menu_servizi)
            self.session.commit()
            return {'menu_servizi': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating menu servizi: {e}")
            return {'Error': str(e)}, 500

    def update(self, id, fkMenu, fkServizio, note, dataInserimento, utenteInserimento):
        try:
            menu_servizi = self.session.query(TMenuServizi).filter_by(id=id).first()
            if menu_servizi:
                menu_servizi.fkMenu = fkMenu
                menu_servizi.fkServizio = fkServizio
                menu_servizi.note = note
                menu_servizi.dataInserimento = dataInserimento
                menu_servizi.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'menu_servizi': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating menu servizi with ID {id}: {e}")
            return {'Error': str(e)}, 500

    def delete(self, id, utenteCancellazione):
        try:
            menu_servizi = self.session.query(TMenuServizi).filter_by(id=id).first()
            if menu_servizi:
                menu_servizi.dataCancellazione = datetime.now()
                menu_servizi.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'menu_servizi': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting menu servizi by ID {id}: {e}")
            return {'Error': str(e)}, 500
