from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente
import json

class TFunzionalitaRepository:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def get_all(self):
        session = self.Session()
        try:
            results = session.query(TFunzionalita).order_by(TFunzionalita.ordinatore).all()
            return [{'id': result.id, 'fkPadre': result.fkPadre, 'titolo': result.titolo, 'label': result.label, 'icon': result.icon, 'link': result.link, 'ordinatore': result.ordinatore, 'target': result.target, 'dataCancellazione': result.dataCancellazione} for result in results]
        except Exception as e:
            session.rollback()  # Esegui il rollback in caso di errore
            return json.dumps({'Error': str(e)}), 500
        finally:
            session.close()  # Assicurati che la sessione venga chiusa

    def get_menu_principale(self):
        session = self.Session()
        try:
            results = session.query(TFunzionalita).filter_by(menuPrincipale=True).all()
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
        except Exception as e:
            session.rollback()  # Esegui il rollback in caso di errore
            return {'Error': str(e)}, 500
        finally:
            session.close()  # Assicurati che la sessione venga chiusa

    def get_by_id(self, id):
        session = self.Session()
        try:
            result = session.query(TFunzionalita).filter_by(id=id).first()
            if result: 
                return {'id': result.id, 'fkPadre': result.fkPadre, 'titolo': result.titolo, 'label': result.label, 'icon': result.icon, 'link': result.link, 'ordinatore': result.ordinatore, 'target': result.target, 'dataCancellazione': result.dataCancellazione}
            else:
                return json.dumps({'Error': f'No match found for this ID: {id}'}), 404
        except Exception as e:
            session.rollback()  # Esegui il rollback in caso di errore
            return json.dumps({'Error': str(e)}), 400
        finally:
            session.close()  # Assicurati che la sessione venga chiusa

    def get_by_padre(self, fkPadre):
        session = self.Session()
        try:
            results = session.query(TFunzionalita).filter_by(fkPadre=fkPadre).all()
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
            session.rollback()  # Esegui il rollback in caso di errore
            return {'Error': str(e)}, 400
        finally:
            session.close()  # Assicurati che la sessione venga chiusa

    def can_access(self, user_type_id, page_link):
        session = self.Session()
        try:
            # Step 1: Trova la funzionalità corrispondente al link della pagina
            funzionalita = session.query(TFunzionalita).filter(TFunzionalita.link == page_link).first()

            if not funzionalita:
                return False, False  # La funzionalità non esiste, nessun accesso e nessun permesso

            # Step 2: Controlla se l'utente ha il permesso di accedere alla funzionalità
            funzionalita_utente = session.query(TFunzionalitaUtente).filter(
                TFunzionalitaUtente.fkTipoUtente == user_type_id,
                TFunzionalitaUtente.fkFunzionalita == funzionalita.id
            ).first()

            if not funzionalita_utente:
                return False, False  # L'utente non ha accesso a questa funzionalità

            # Step 3: Restituisci il permesso dell'utente
            if funzionalita_utente.permessi == 1:
                return True, True  # Accesso con permesso di modifica (scrittura)
            else:
                return True, False  # Accesso solo in lettura

        except Exception as e:
            session.rollback()  # Esegui il rollback in caso di errore
            return False, False  # Errore durante il controllo dell'accesso
        finally:
            session.close()  # Assicurati che la sessione venga chiusa
