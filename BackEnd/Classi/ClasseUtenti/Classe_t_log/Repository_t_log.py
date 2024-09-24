from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_log.Domain_t_log import TLog
from flask import request  # Importa request per accedere ai dettagli della richiesta corrente


class Repository_t_log:  # Corretto il nome della classe
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def log_to_db(self, level, message, user_id, route, data):
        session = self.Session()  # Creare una nuova sessione per ogni log
        try:
            new_log = TLog(
                level=level,
                message=message,
                user_id=user_id,
                route=route or request.path,
                data=data
            )
            session.add(new_log)
            session.commit()
        except Exception as e:
            session.rollback()
            return {'Error': str(e)}, 500
        finally:
            session.close()  # Chiudi sempre la sessione dopo ogni operazione
