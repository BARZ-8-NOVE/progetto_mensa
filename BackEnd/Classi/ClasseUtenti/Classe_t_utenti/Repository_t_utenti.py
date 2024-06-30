from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpErrors import NotFoundError

class Repository_t_utenti:
    
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.httpCodes = HttpCodes()

    def exists_utente_by_id(self, id:int):
        try:
            result = self.session.query(TUtenti).filter_by(id=id).first()
            return UtilityGeneral.checkResult(result)
        except Exception as e:
            self.session.rollback()
            raise Exception(str(e))
        
    def exists_utente_by_username(self, username:str):
        try:
            result = self.session.query(TUtenti).filter_by(username=username).first()
            return UtilityGeneral.checkResult(result)
        except Exception as e:
            self.session.rollback()
            raise Exception(str(e))
        
    def exists_utente_by_email(self, email:str):
        try:
            result = self.session.query(TUtenti).filter_by(email=email).first()
            return UtilityGeneral.checkResult(result)
        except Exception as e:
            self.session.rollback()
            raise Exception(str(e))
    
    def get_utenti_all(self):
        try:
            results = self.session.query(TUtenti).all()
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(results)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            raise Exception(str(e))

    def get_utente_by_id(self, id:int):
        try:
            result = self.session.query(TUtenti).filter_by(id=id).first()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            raise Exception(str(e))
        if result:
            self.session.close()
            return UtilityGeneral.getClassDictionaryOrList(result)
        else:
            self.session.rollback()
            self.session.close()
            raise NotFoundError('Utente', 'id', id)
        
    def create_utente(self, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo:int, inizio, email:str, password:str):
        #try:
            resultExistsEmail = self.exists_utente_by_email(email)
            if resultExistsEmail:
                self.session.rollback()
                self.session.close()
                return {'Error': UtilityMessages.existsStringError('Utente', 'email', email)}, self.httpCodes.FORBIDDEN
            resultExistsUsername = self.exists_utente_by_username(username)
            if resultExistsUsername:
                self.session.rollback()
                self.session.close()
                return {'Error':UtilityMessages.existsStringError('Utente', 'username', username)}, self.httpCodes.FORBIDDEN
            tipoUtente = Repository_t_tipiUtente()
            resultTipoUtente = tipoUtente.exists_tipoUtente_by_id(fkTipoUtente)
            if not resultTipoUtente:
                self.session.rollback()
                self.session.close()
                raise NotFoundError('TipoUtente', 'fkTipoUtente', fkTipoUtente)
                #return {'Error': UtilityMessages.existsStringError('TipoUtente', 'fkTipoUtente', fkTipoUtente)}, self.httpCodes.NOT_FOUND
            utente = TUtenti(username=username, nome=nome, cognome=cognome, fkTipoUtente=fkTipoUtente,
                            fkFunzCustom=fkFunzCustom, reparti=reparti, attivo=attivo, inizio=inizio,
                            email=email, password=password)
            self.session.add(utente)
            self.session.commit()
            return UtilityGeneral.getClassDictionaryOrList(utente), 200
        #except Exception as e:
        #    self.session.rollback()
        #    self.session.close()
        #    return {'Error': str(e)}, 400
        
    def update_utente(self, id:int, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo, email:str, password:str):
        try:
            utente:TUtenti = self.exists_utente_by_id(id)
            if utente:
                tipoUtente = Repository_t_tipiUtente()
                result = tipoUtente.exists_tipoUtente_by_id(fkTipoUtente)
                if not result:
                    self.session.rollback()
                    self.session.close()
                    return {'Error':f'cannot find tipoUtente for this id: {fkTipoUtente}'}, 404
                utente.username = username
                utente.nome = nome
                utente.cognome = cognome
                utente.fkTipoUtente = fkTipoUtente
                utente.fkFunzCustom = fkFunzCustom
                utente.reparti = reparti
                utente.attivo = attivo
                utente.email = email
                utente.password = password
                self.session.commit()
                return UtilityGeneral.getClassDictionaryOrList(utente), 200
            else:
                return {'Error':f'cannot find utente for this id: {id}'}, 404
        except Exception as e:
                self.session.rollback()
                self.session.close()
                raise Exception(str(e))

    def delete_utente(self, id:int):
        try:
            result = self.exists_utente_by_id(id)
            if result:
                self.session.delete(result)
                self.session.commit()
                self.session.close()
                return {'utente':f'deleted utente for this id: {id}'}, 200
            else:
                self.session.rollback()
                self.session.close()
                return {'Error':f'cannot find utente for this id: {id}'}, 403
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500