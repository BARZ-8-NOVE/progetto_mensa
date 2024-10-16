from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAlimenti.Classe_t_allergeni.Domani_t_allergeni import TAllergeni
import logging

class RepositoryAllergeni:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TAllergeni).all()
            return [{'id': result.id, 'nome': result.nome} for result in results]
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting all allergeni: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def get_by_id(self, id):
        try:
            result = self.session.query(TAllergeni).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'nome': result.nome}
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            logging.error(f"Error getting allergene by ID {id}: {e}")
            return {'Error': str(e)}, 400
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def create(self, nome):
        try:
            allergene = TAllergeni(nome=nome)
            self.session.add(allergene)
            self.session.commit()
            return {'allergene': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error creating allergene: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def update(self, id, nome):
        try:
            allergene = self.session.query(TAllergeni).filter_by(id=id).first()
            if allergene:
                allergene.nome = nome
                self.session.commit()
                return {'allergene': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error updating allergene with ID {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def delete(self, id):
        try:
            result = self.session.query(TAllergeni).filter_by(id=id).first()
            if result:
                self.session.delete(result)
                self.session.commit()
                return {'allergene': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error deleting allergene by id {id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()