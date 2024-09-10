from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseMenu.Classe_t_tipiMenu.Domain_t_tipiMenu import TTipiMenu
from datetime import datetime

class RepositoryTipiMenu:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TTipiMenu).filter(TTipiMenu.dataCancellazione.is_(None)).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'descrizione': result.descrizione, 'color': result.color,
                 'backgroundColor': result.backgroundColor, 'ordinatore': result.ordinatore,
                 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento,
                 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
                for result in results]

    def get_by_id(self, id):
        try:
            result = self.session.query(TTipiMenu).filter_by(id=id).first()
        except Exception as e:
            return {'Error': str(e)}, 400
        if result:
            return {'id': result.id, 'descrizione': result.descrizione, 'color': result.color,
                    'backgroundColor': result.backgroundColor, 'ordinatore': result.ordinatore,
                    'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
        else:
            return {'Error': f'No match found for this id: {id}'}, 404

    def create(self, descrizione, color, backgroundColor, ordinatore, utenteInserimento):
        try:
            tipimenu = TTipiMenu(
                descrizione=descrizione, 
                color=color, 
                backgroundColor=backgroundColor,
                ordinatore=ordinatore, 
                utenteInserimento=utenteInserimento
                                 
            )
            self.session.add(tipimenu)
            self.session.commit()
            return {'tipimenu': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()        

    def update(self, id, descrizione, color, backgroundColor, ordinatore, utenteInserimento):
        try:
            tipimenu = self.session.query(TTipiMenu).filter_by(id=id).first()
            if tipimenu:
                tipimenu.descrizione = descrizione
                tipimenu.color = color
                tipimenu.backgroundColor = backgroundColor
                tipimenu.ordinatore = ordinatore
                tipimenu.utenteInserimento = utenteInserimento
                self.session.commit()
                return {'tipimenu': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def delete(self, id, utenteCancellazione):
        try:
            tipimenu = self.session.query(TTipiMenu).filter_by(id=id).first()
            if tipimenu:
                tipimenu.dataCancellazione = datetime.now()
                tipimenu.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'tipimenu': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()