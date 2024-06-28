from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseServizi.Domani_t_servizi import TServizi

class RepositoryTServizi:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_servizi(self):
        try:
            results = self.session.query(TServizi).all()
            return [{'id': result.id, 'descrizione': result.descrizione, 'ordinatore': result.ordinatore, 'inMenu': result.inMenu} for result in results]
        except Exception as e:
            return {'Error': str(e)}, 500

    def get_servizio_by_id(self, id):
        try:
            result = self.session.query(TServizi).filter_by(id=id).first()
            if result:
                return {'id': result.id, 'descrizione': result.descrizione, 'ordinatore': result.ordinatore, 'inMenu': result.inMenu}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400

    def create_servizio(self, descrizione, ordinatore, inMenu):
        try:
            new_servizio = TServizi(descrizione=descrizione, ordinatore=ordinatore, inMenu=inMenu)
            self.session.add(new_servizio)
            self.session.commit()
            return {'servizio': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def update_servizio(self, id, descrizione=None, ordinatore=None, inMenu=None):
        try:
            servizio = self.session.query(TServizi).filter_by(id=id).first()
            if servizio:
                if descrizione is not None:
                    servizio.descrizione = descrizione
                if ordinatore is not None:
                    servizio.ordinatore = ordinatore
                if inMenu is not None:
                    servizio.inMenu = inMenu
                self.session.commit()
                return {'servizio': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete_servizio(self, id):
        try:
            servizio = self.session.query(TServizi).filter_by(id=id).first()
            if servizio:
                self.session.delete(servizio)
                self.session.commit()
                return {'servizio': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
