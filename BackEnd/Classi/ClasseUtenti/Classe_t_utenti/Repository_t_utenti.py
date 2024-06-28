from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Repository_t_tipiUtenti import Repository_t_tipiUtente

class Repository_t_utenti:

    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def exists_utente_by_id(self, id:int):
        try:
            result = self.session.query(TUtenti).filter_by(id=id).first()
            if result:
                return result
            else:
                return False
        except Exception as e:
            return {'Error':str(e)}, 400
        
    def exists_utente_by_username(self, username:str):
        try:
            result = self.session.query(TUtenti).filter_by(username=username).first()
            if result:
                return result
            else:
                return False
        except Exception as e:
            return {'Error':str(e)}, 400
        
    def exists_utente_by_email(self, email:str):
        try:
            result = self.session.query(TUtenti).filter_by(email=email).first()
            if result:
                return result
            else:
                return False
        except Exception as e:
            return {'Error':str(e)}, 400
    
    def get_utenti_all(self):
        try:
            results = self.session.query(TUtenti).all()
            self.session.close()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'username': result.username, 'nome': result.nome,
                'cognome': result.cognome, 'fkTipoUtente': result.fkTipoUtente,
                'fkFunzCustom': result.fkFunzCustom, 'reparti': result.reparti,
                'attivo': result.attivo, 'inizio': result.inizio,
                'email': result.email, 'password': result.password} for result in results]

    def get_utente_by_id(self, id:int):
        try:
            result = self.session.query(TUtenti).filter_by(id=id).first()
        except Exception as e:
            return {'Error':str(e)}, 400
        if result:
            self.session.close()
            return {'id': result.id, 'username': result.username, 'nome': result.nome,
                'cognome': result.cognome, 'fkTipoUtente': result.fkTipoUtente,
                'fkFunzCustom': result.fkFunzCustom, 'reparti': result.reparti,
                'attivo': result.attivo, 'inizio': result.inizio,
                'email': result.email, 'password': result.password}, 200
        else:
            self.session.close()
            return {'Error':f'cannot find utente for this id: {id}'}, 404
        
    def create_utente(self, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo:int, inizio, email:str, password:str):
        try:
            resultExistsEmail = self.exists_utente_by_email(email)
            if resultExistsEmail:
                self.session.rollback()
                self.session.close()
                return {'Error':f'utente already exists with this email: {email}'}
            resultExistsUsername = self.exists_utente_by_username(username)
            if resultExistsUsername:
                self.session.rollback()
                self.session.close()
                return {'Error':f'utente already exists with this username: {username}'}
            tipoUtente = Repository_t_tipiUtente()
            resultTipoUtente = tipoUtente.exists_tipoUtente_by_id(fkTipoUtente)
            if not resultTipoUtente:
                self.session.rollback()
                self.session.close()
                return {'Error':f'cannot find tipoUtente for this id: {fkTipoUtente}'}, 404
            utente = TUtenti(username=username, nome=nome, cognome=cognome, fkTipoUtente=fkTipoUtente,
                            fkFunzCustom=fkFunzCustom, reparti=reparti, attivo=attivo, inizio=inizio,
                            email=email, password=password)
            self.session.add(utente)
            self.session.commit()
            return {'id': utente.id, 'username': utente.username, 'nome': utente.nome,
                'cognome': utente.cognome, 'fkTipoUtente': utente.fkTipoUtente,
                'fkFunzCustom': utente.fkFunzCustom, 'reparti': utente.reparti,
                'attivo': utente.attivo, 'inizio': utente.inizio,
                'email': utente.email, 'password': utente.password}, 200
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return {'Error': str(e)}, 400
        
    def update_utente(self, id:int, username:str, nome:str, cognome:str, fkTipoUtente:int,
                    fkFunzCustom:str, reparti:str, attivo, inizio, email:str, password:str):
        try:
            utente = self.exists_utente_by_id(id)
        except Exception as e:
                self.session.rollback()
                self.session.close()
                return {'Error': str(e)}, 400
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
            utente.inizio = inizio
            utente.email = email
            utente.password = password
            self.session.commit()
            return {'id': utente.id, 'username': utente.username, 'nome': utente.nome,
                'cognome': utente.cognome, 'fkTipoUtente': utente.fkTipoUtente,
                'fkFunzCustom': utente.fkFunzCustom, 'reparti': utente.reparti,
                'attivo': utente.attivo, 'inizio': utente.inizio,
                'email': utente.email, 'password': utente.password}, 200
        else:
            return {'Error':f'cannot find utente for this id: {id}'}, 404

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