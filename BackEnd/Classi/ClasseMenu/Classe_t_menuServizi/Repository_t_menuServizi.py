import logging
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from datetime import datetime
from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi
from sqlalchemy import and_

class RepositoryMenuServizi:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TMenuServizi).filter(TMenuServizi.dataCancellazione.is_(None)).all()
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
        finally:
            # Chiudi sempre la sessione
            self.session.close()

        
    def get_all_by_menu_id(self, menu_id):
         return self.session.query(TMenuServizi).filter(TMenuServizi.fkMenu.in_(menu_id)).all()

    def get_all_by_menu_ids(self, menu_ids):
        try:
            # Assicurati che menu_ids sia una lista
            if not isinstance(menu_ids, list):
                menu_ids = [menu_ids]

            # Filtra i record con fkMenu in menu_ids
            results = self.session.query(TMenuServizi).filter(
                TMenuServizi.fkMenu.in_(menu_ids),
                TMenuServizi.dataCancellazione.is_(None)
            ).all()

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
            logging.error(f"Error getting menu services by menu ids: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

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
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def create(self, fkMenu, fkServizio, utenteInserimento, note = None):
        try:
            menu_servizi = TMenuServizi(
                fkMenu=fkMenu,
                fkServizio=fkServizio,
                utenteInserimento=utenteInserimento,
                note=note

            )
            self.session.add(menu_servizi)
            self.session.commit()
            return menu_servizi.id
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating menu servizi: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

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
        finally:
            # Chiudi sempre la sessione
            self.session.close()

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
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_all_by_menu_ids_con_servizio(self, menu_id, fkServizio):
        try:
        # Filtra i record con fkMenu e fkServizio
            result = self.session.query(TMenuServizi).filter(
                TMenuServizi.fkMenu == menu_id,
                TMenuServizi.fkServizio == fkServizio,
                TMenuServizi.dataCancellazione.is_(None)
            ).first()
            
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
                return {'id': 'N/A'}
            
        except Exception as e:
            logging.error(f"Error getting menu services by menu id and service type: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()