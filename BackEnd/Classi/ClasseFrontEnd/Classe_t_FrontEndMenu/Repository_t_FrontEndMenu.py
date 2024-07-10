from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseFrontEnd.Classe_t_FrontEndMenu.Domani_t_FrontEndMenu import TFrontEndMenu
import json

class RepositoryTFrontEndMenu:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def get_all(self):
        try:
            results = self.session.query(TFrontEndMenu).all()
            return [{'id': result.id, 'titolo': result.titolo, 'label':result.label, 'icon': result.icon,'link': result.link, 'ordinatore': result.ordinatore,'target': result.target,'dataCancellazione': result.dataCancellazione}for result in results]
        except Exception as e:
            return json.dumps({'Error': str(e)}), 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TFrontEndMenu).filter_by(id=id).first()
            if result: 
                return {'id': result.id, 'titolo': result.titolo, 'label':result.label, 'icon': result.icon,'link': result.link, 'ordinatore': result.ordinatore,'target': result.target,'dataCancellazione': result.dataCancellazione}
            else:
                return json.dumps({'Error': f'No match found for this ID: {id}'}), 404
        except Exception as e:
            return json.dumps({'Error': str(e)}), 400
