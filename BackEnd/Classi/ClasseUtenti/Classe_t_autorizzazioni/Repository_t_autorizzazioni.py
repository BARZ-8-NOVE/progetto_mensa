from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Domain_t_autorizzazioni import TAutorizzazioni
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

class Repository_t_autorizzazioni:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_autorizzazione(self, id):
        try:
            result = self.session.query(TAutorizzazioni).filter_by(id=id).first()
            return UtilityGeneral.checkResult(result)
        except Exception as e:
            return {'Error':str(e)}, 400

    def get_autorizzazioni_all(self):
        try:
            results = self.session.query(TAutorizzazioni).all()
            self.session.close()
            return UtilityGeneral.getClassDictionary(results)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500

    def get_autorizzazione_by_id(self, id:int):
        try:
            result = self.session.query(TAutorizzazioni).filter_by(id=id).first()
            if result:
                self.session.close()
                return UtilityGeneral.getClassDictionary(result)
            else:
                self.session.close()
                return {'Error':f'cannot find autorizzazione for this id: {id}'}, 404
        except Exception as e:
            return {'Error':str(e)}, 400
        
    def create_autorizzazione(self, nome:str, fkListaFunzionalita:str):
        try:
            result = TAutorizzazioni(nome=nome, fkListaFunzionalita=fkListaFunzionalita)
            self.session.add(result)
            self.session.commit()
            return UtilityGeneral.getClassDictionary(result)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}
        
    def update_autorizzazione(self, id:int, nome:str, fkListaFunzionalita:str):
        try:
            result:TAutorizzazioni = self.exists_autorizzazione(id)
            if result:
                result.nome = nome
                result.fkListaFunzionalita = fkListaFunzionalita
                self.session.commit()
                return UtilityGeneral.getClassDictionary(result)
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'cannot find autorizzazione for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        
    def delete_autorizzazione(self, id:int):
        try:
            result = self.exists_autorizzazione(id)
            if result:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return {'Autorizzazione':f'deleted autorizzazione for this id: {id}'}
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'cannot find autorizzazione for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500