from sqlalchemy.orm import sessionmaker
from datetime import datetime
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Domain_t_menuServiziAssociazione import TMenuServiziAssociazione
import logging
class RepositoryMenuServiziAssociazion:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TMenuServiziAssociazione).filter(TMenuServiziAssociazione.dataCancellazione == None).all()
            return [{'id': result.id, 'fkMenuServizio': result.fkMenuServizio, 'fkAssociazione': result.fkAssociazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500
        
    def get_all_by_associazione_ids(self, fkMenuServizi):
        try:
            if not isinstance(fkMenuServizi, list) or not fkMenuServizi:
                return []  # Restituisci una lista vuota se la lista di ID è vuota o non è una lista

            results = self.session.query(TMenuServiziAssociazione).filter(
                TMenuServiziAssociazione.fkMenuServizio.in_(fkMenuServizi),
                TMenuServiziAssociazione.dataCancellazione.is_(None)
            ).all()

            return [
                {
                    'id': result.id,
                    'fkMenuServizio': result.fkMenuServizio,
                    'fkAssociazione': result.fkAssociazione,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione
                }
                for result in results
            ]
        except Exception as e:
            logging.error(f"Error getting menu associations by menu service ids: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TMenuServiziAssociazione).filter_by(id=id, dataCancellazione=None).first()
            if result:
                return {'id': result.id, 'fkMenuServizio': result.fkMenuServizio, 'fkAssociazione': result.fkAssociazione, 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento, 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400
        
    def get_by_fk_menu_servizio(self, fkMenuServizio):
        try:
            results = self.session.query(TMenuServiziAssociazione).filter_by(fkMenuServizio=fkMenuServizio, dataCancellazione=None).all()
            return [{'id': result.fkAssociazione} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500

    def create(self, fkMenuServizio, fkAssociazione, utenteInserimento, dataInserimento=None):
        try:
            associazione = TMenuServiziAssociazione(
                fkMenuServizio=fkMenuServizio,
                fkAssociazione=fkAssociazione,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento
            )
            self.session.add(associazione)
            self.session.commit()
            return {'associazione': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        
    def update(self, id, fkMenuServizio, fkAssociazione, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione):
        try:
            associazione = self.session.query(TMenuServiziAssociazione).filter_by(id=id).first()
            if associazione:
                associazione.fkMenuServizio = fkMenuServizio
                associazione.fkAssociazione = fkAssociazione
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

    def delete(self, id, utenteCancellazione):
        try:
            associazione = self.session.query(TMenuServiziAssociazione).filter_by(id=id).first()
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
