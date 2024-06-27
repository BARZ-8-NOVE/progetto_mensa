from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Domani_t_tipologiaalimenti import TTipologiaAlimenti
import logging

class RepositoryTipologiaAlimenti:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipologiaAlimenti).all()
            return [{'id': result.id, 'nome': result.nome, 'descrizione': result.descrizione, 'conservazione_id': result.conservazione_id} for result in results]
        except Exception as e:
            logging.error(f"Error getting all alimenti: {e}")
            return {'Error': str(e)}, 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TTipologiaAlimenti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'nome': result.nome, 'descrizione': result.descrizione, 'conservazione_id': result.conservazione_id}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            logging.error(f"Error getting alimento by id {id}: {e}")
            return {'Error': str(e)}, 400
        
    def create(self, nome, descrizione, conservazione_id):
        try:
            alimento = TTipologiaAlimenti(nome=nome, descrizione=descrizione, conservazione_id=conservazione_id)
            self.session.add(alimento)
            self.session.commit()
            return {'alimento': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating alimento: {e}")
            return {'Error': str(e)}, 500

    def update(self, id, nome, descrizione, conservazione_id):
        try:
            alimento = self.session.query(TTipologiaAlimenti).filter_by(id=id).first()
            if alimento:
                alimento.nome = nome
                alimento.descrizione = descrizione
                alimento.conservazione_id = conservazione_id
                self.session.commit()
                return {'alimento': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating alimento with id {id}: {e}")
            return {'Error': str(e)}, 500

    def delete(self, id):
        try:
            result = self.session.query(TTipologiaAlimenti).filter_by(id=id).first()
            if result:
                self.session.delete(result)
                self.session.commit()
                return {'alimento': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting alimento by id {id}: {e}")
            return {'Error': str(e)}, 500
