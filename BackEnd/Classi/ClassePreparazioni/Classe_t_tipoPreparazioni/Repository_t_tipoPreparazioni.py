from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Domain_t_tipoPreparazioni import TTipiPreparazioni

class Repository_t_tipipreparazioni:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_tipipreparazioni(self):
        try:
            results = self.session.query(TTipiPreparazioni).all()
            return [{'id': result.id, 'descrizione': result.descrizione} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500

    def get_tipipreparazioni_by_id(self, id):
        try:
            result = self.session.query(TTipiPreparazioni).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'descrizione': result.descrizione}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400

    def create_tipipreparazioni(self, descrizione):
        try:
            tipipreparazioni = TTipiPreparazioni(descrizione=descrizione)
            self.session.add(tipipreparazioni)
            self.session.commit()
            return {'tipipreparazioni': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete_tipipreparazioni(self, id):
        try:
            tipipreparazioni = self.session.query(TTipiPreparazioni).filter_by(id=id).first()
            if tipipreparazioni:
                self.session.delete(tipipreparazioni)
                self.session.commit()
                return {'tipipreparazioni': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
