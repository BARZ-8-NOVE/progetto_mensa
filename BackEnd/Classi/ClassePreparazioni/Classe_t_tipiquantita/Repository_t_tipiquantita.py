from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Domain_t_tipiquantita import TTipoQuantita

class Repository_t_tipoquantita:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_tipoquantita(self):
        try:
            results = self.session.query(TTipoQuantita).all()
            return [{'id': result.id, 'tipo': result.tipo, 'peso_valore_in_grammi': result.peso_valore_in_grammi, 'peso_valore_in_Kg': result.peso_valore_in_Kg} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500

    def get_tipoquantita_by_id(self, id):
        try:
            result = self.session.query(TTipoQuantita).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'tipo': result.tipo, 'peso_valore_in_grammi': result.peso_valore_in_grammi, 'peso_valore_in_Kg': result.peso_valore_in_Kg}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400

    def create_tipoquantita(self, tipo, peso_valore_in_grammi=None, peso_valore_in_Kg=None):
        try:
            tipoquantita = TTipoQuantita(tipo=tipo, peso_valore_in_grammi=peso_valore_in_grammi, peso_valore_in_Kg=peso_valore_in_Kg)
            self.session.add(tipoquantita)
            self.session.commit()
            return {'tipoquantita': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete_tipoquantita(self, id):
        try:
            tipoquantita = self.session.query(TTipoQuantita).filter_by(id=id).first()
            if tipoquantita:
                self.session.delete(tipoquantita)
                self.session.commit()
                return {'tipoquantita': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
