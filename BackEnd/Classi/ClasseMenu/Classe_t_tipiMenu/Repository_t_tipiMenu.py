from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseMenu.Classe_t_tipiMenu.Domain_t_tipiMenu import TTipiMenu

class RepositoryTipiMenu:
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_tipi_menu_all(self):
        try:
            results = self.session.query(TTipiMenu).all()
        except Exception as e:
            return {'Error': str(e)}, 500
        return [{'id': result.id, 'descrizione': result.descrizione, 'color': result.color,
                 'backgroundColor': result.backgroundColor, 'ordinatore': result.ordinatore,
                 'dataInserimento': result.dataInserimento, 'utenteInserimento': result.utenteInserimento,
                 'dataCancellazione': result.dataCancellazione, 'utenteCancellazione': result.utenteCancellazione}
                for result in results]

    def get_tipi_menu_by_id(self, id):
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

    def create_tipi_menu(self, descrizione, color, backgroundColor, ordinatore, dataInserimento, utenteInserimento):
        try:
            tipimenu = TTipiMenu(descrizione=descrizione, color=color, backgroundColor=backgroundColor,
                                 ordinatore=ordinatore, dataInserimento=dataInserimento,
                                 utenteInserimento=utenteInserimento)
            self.session.add(tipimenu)
            self.session.commit()
            return {'tipimenu': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500

    def delete_tipi_menu(self, id, dataCancellazione, utenteCancellazione):
        try:
            tipimenu = self.session.query(TTipiMenu).filter_by(id=id).first()
            if tipimenu:
                tipimenu.dataCancellazione = dataCancellazione
                tipimenu.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'tipimenu': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
