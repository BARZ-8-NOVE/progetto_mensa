from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Repository_t_autorizzazioni import Repository_t_autorizzazioni

class Repository_t_tipiUtente:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_tipoUtente(self, id:int):
        try:
            result = self.session.query(TTipiUtenti).filter_by(id=id).first()
            if result:
                return result
            else:
                return False
        except Exception as e:
            return {'Error':str(e)}, 400
    
    def get_tipiUtenti_all(self):
        try:
            results = self.session.query(TTipiUtenti).all()
            self.session.close()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'nomeTipoUtente': result.nomeTipoUtente, 'fkAutorizzazioni': result.fkAutorizzazioni} for result in results]

    def get_tipoUtente_by_id(self, id:int):
        try:
            result = self.session.query(TTipiUtenti).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            self.session.close()
            return {'id': result.id, 'nomeTipoUtente': result.nomeTipoUtente, 'fkAutorizzazioni': result.fkAutorizzazioni}, 200
        else:
            self.session.close()
            return {'Error':f'cannot find tipoUtente for this id: {id}'}, 404
        
    def create_tipoUtente(self, nomeTipoUtente:str, fkAutorizzazioni):
        try:
            if fkAutorizzazioni:
                autorizzazione = Repository_t_autorizzazioni()
                result = autorizzazione.exists_autorizzazione(fkAutorizzazioni)
                if not result:
                    self.session.rollback()
                    self.session.close()
                    return {'Error':f'cannot find Autorizzazione for this id: {fkAutorizzazioni}'}, 404
            tipoUtente = TTipiUtenti(nomeTipoUtente=nomeTipoUtente, fkAutorizzazioni=fkAutorizzazioni)
            self.session.add(tipoUtente)
            self.session.commit()
            return {'id':tipoUtente.id, 'nomeTipoUtente':tipoUtente.nomeTipoUtente, 'fkAutorizzazioni':tipoUtente.fkAutorizzazioni}, 200
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 400
        
    def update_tipoUtente(self, id:int, nomeTipoUtente:str, fkAutorizzazioni):
        try:
            tipoUtente = self.exists_tipoUtente(id)
        except Exception as e:
                self.session.rollback()
                self.session.close()
                return {'Error': str(e)}, 400
        if tipoUtente:
            if fkAutorizzazioni:
                autorizzazione = Repository_t_autorizzazioni()
                result = autorizzazione.exists_autorizzazione(fkAutorizzazioni)
                if not result:
                    self.session.rollback()
                    self.session.close()
                    return {'Error':f'cannot find Autorizzazione for this id: {fkAutorizzazioni}'}, 404
            tipoUtente.nomeTipoUtente = nomeTipoUtente
            tipoUtente.fkAutorizzazioni = fkAutorizzazioni
            self.session.commit()
            return {'id':tipoUtente.id, 'nomeTipoUtente':tipoUtente.nomeTipoUtente, 'fkAutorizzazioni':tipoUtente.fkAutorizzazioni}, 200
        else:
            return {'Error':f'cannot find tipoUtente for this id: {id}'}, 404

        
    def delete_tipoUtente(self, id:int):
        try:
            result = self.exists_tipoUtente(id)
            if result:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return {'TipiUtente':f'deleted tipiUtente for this id: {id}'}, 200
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'cannot find tipoUtente for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500