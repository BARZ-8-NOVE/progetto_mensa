import logging
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseMenu.Classe_t_menu.Domain_t_menu import TMenu
from datetime import datetime 

class RepositoryMenu:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TMenu).all()
            return [
                {
                    'id': result.id,
                    'data': result.data,
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                } for result in results
            ]
        except Exception as e:
            logging.error(f"Error getting all menu: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TMenu).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'data': result.data,
                    'fkTipoMenu': result.fkTipoMenu,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                }
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting menu by ID {id}: {e}")
            return {'Error': str(e)}, 400

    def create(self, data, fkTipoMenu, dataInserimento, utenteInserimento):
        try:
            menu = TMenu(
                data=data,
                fkTipoMenu=fkTipoMenu,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento
            )
            self.session.add(menu)
            self.session.commit()
            return {'menu': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating menu: {e}")
            return {'Error': str(e)}, 500

    def update(self, id, data, fkTipoMenu, dataInserimento, utenteInserimento):
        try:
            menu = self.session.query(TMenu).filter_by(id=id).first()
            if menu:
                menu.data = data
                menu.fkTipoMenu = fkTipoMenu
                menu.dataInserimento = dataInserimento
                menu.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'menu': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating menu with ID {id}: {e}")
            return {'Error': str(e)}, 500

    def delete(self, id, utenteCancellazione):
        try:
            menu = self.session.query(TMenu).filter_by(id=id).first()
            if menu:
                menu.dataCancellazione = datetime.now()
                menu.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'menu': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting menu by ID {id}: {e}")
            return {'Error': str(e)}, 500
