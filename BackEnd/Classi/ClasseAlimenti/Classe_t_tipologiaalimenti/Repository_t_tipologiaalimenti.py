from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from .Domani_t_tipologiaalimenti import TTipologiaAlimenti

class Repository_t_tipologiaalimenti:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_tipologiaalimenti(self):
        try:
            results = self.session.query(TTipologiaAlimenti).all()
            return [{'id': result.id, 'nome': result.nome, 'fktipologiaConservazione': result.fktipologiaConservazione} for result in results]
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def get_tipologiaalimenti_by_id(self, id):
        try:
            result = self.session.query(TTipologiaAlimenti).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'nome': result.nome, 'fktipologiaConservazione': result.fktipologiaConservazione}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()  # Aggiunta del rollback
            return {'Error': str(e)}, 400
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def create_tipologiaalimenti(self, nome, fktipologiaConservazione):
        try:
            tipologiaalimenti = TTipologiaAlimenti(nome=nome, fktipologiaConservazione=fktipologiaConservazione)
            self.session.add(tipologiaalimenti)
            self.session.commit()
            return {'tipologiaalimenti': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()

    def delete_tipologiaalimenti(self, id):
        try:
            tipologiaalimenti = self.session.query(TTipologiaAlimenti).filter_by(id=id).first()
            if tipologiaalimenti:
                self.session.delete(tipologiaalimenti)
                self.session.commit()
                return {'tipologiaalimenti': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            if self.session:
                self.session.close()