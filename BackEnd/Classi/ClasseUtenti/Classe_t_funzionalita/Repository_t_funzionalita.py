from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
import json

class TFunzionalitaRepository:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TFunzionalita).all()
            return [{'id': result.id,'fkPadre': result.fkPadre, 'titolo': result.titolo, 'label':result.label, 'icon': result.icon,'link': result.link, 'ordinatore': result.ordinatore,'target': result.target,'dataCancellazione': result.dataCancellazione}for result in results]
        except Exception as e:
            return json.dumps({'Error': str(e)}), 500

    def get_by_id(self, id):
        try:
            result = self.session.query(TFunzionalita).filter_by(id=id).first()
            if result: 
                return {'id': result.id, 'fkPadre': result.fkPadre, 'titolo': result.titolo, 'label':result.label, 'icon': result.icon,'link': result.link, 'ordinatore': result.ordinatore,'target': result.target,'dataCancellazione': result.dataCancellazione}
            else:
                return json.dumps({'Error': f'No match found for this ID: {id}'}), 404
        except Exception as e:
            return json.dumps({'Error': str(e)}), 400
        
    def get_by_padre(self, fkPadre):
        try:
            results = self.session.query(TFunzionalita).filter_by(fkPadre=fkPadre).all()
            if results:
                return [
                    {
                        'id': result.id,
                        'fkPadre': result.fkPadre,
                        'titolo': result.titolo,
                        'label': result.label,
                        'icon': result.icon,
                        'link': result.link,
                        'ordinatore': result.ordinatore,
                        'target': result.target,
                        'dataCancellazione': result.dataCancellazione
                    } 
                    for result in results
                ]
            else:
                return {'Error': f'No match found for this fkPadre: {fkPadre}'}, 404
        except Exception as e:
            return {'Error': str(e)}, 400