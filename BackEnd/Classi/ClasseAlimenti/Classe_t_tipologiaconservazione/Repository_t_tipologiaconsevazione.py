from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAlimenti.Classe_t_tipologiaconservazione.Domani_t_tipologiaconservazione import TTipologiaConservazioni
import logging

class RepositoryTipologiaConservazioni:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipologiaConservazioni).all()
            return [{'id': result.id, 'nome': result.nome} for result in results]
        except Exception as e:
            logging.error(f"Error getting all conservazioni: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TTipologiaConservazioni).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'nome': result.nome}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting conservazione by id {id}: {e}")
            return {'Error': str(e)}, 400
        
    def create(self, nome):
        try:
            tipologia_conservazione = TTipologiaConservazioni(nome=nome)
            self.session.add(tipologia_conservazione)
            self.session.commit()
            return {'tipologia_conservazione': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating tipologia conservazione: {e}")
            return {'Error': str(e)}, 500
        
    def update(self, id, nome):
        try:
            tipologia_conservazione = self.session.query(TTipologiaConservazioni).filter_by(id=id).first()
            if tipologia_conservazione:
                tipologia_conservazione.nome = nome
                self.session.commit()
                return {'tipologia_conservazione': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating tipologia conservazione with ID {id}: {e}")
            return {'Error': str(e)}, 500

    def delete(self, id):
        try:
            result = self.session.query(TTipologiaConservazioni).filter_by(id=id).first()
            if result:
                self.session.delete(result)
                self.session.commit()
                return {'tipologiaconservazioni': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting conservazione by id {id}: {e}")
            return {'Error': str(e)}, 500
