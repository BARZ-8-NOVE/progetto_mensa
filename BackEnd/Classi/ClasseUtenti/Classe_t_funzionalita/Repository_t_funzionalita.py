from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente
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


    def get_menu_principale(self):
        """
        Recupera tutte le funzionalità che sono marcate come menu principale.

        Returns:
            List[Dict[str, Union[int, str, None]]]: Una lista di dizionari che rappresentano le voci di menu principale.
            Dict[str, str]: Un dizionario contenente un messaggio di errore in caso di eccezione.
        """
        try:
            results = self.session.query(TFunzionalita).filter_by(menuPrincipale=True).all()
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
            # Log dell'errore se necessario
            return {'Error': str(e)}
        

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
        
    def can_access(self, user_type_id, page_link):
        try:
            # Step 1: Trova la funzionalità corrispondente al link della pagina
            funzionalita = self.session.query(TFunzionalita).filter(TFunzionalita.link == page_link).first()

            if not funzionalita:
                return False, "La funzionalità richiesta non esiste."

            # Step 2: Controlla se l'utente ha il permesso di accedere alla funzionalità
            funzionalita_utente = self.session.query(TFunzionalitaUtente).filter(
                TFunzionalitaUtente.fkTipoUtente == user_type_id,
                TFunzionalitaUtente.fkFunzionalita == funzionalita.id
            ).first()

            if not funzionalita_utente:
                return False, "Accesso negato. Non hai permessi per questa funzionalità."

            # Step 3: Restituisci il permesso dell'utente
            if funzionalita_utente.permessi == 1:
                return True, "Accesso con permesso di modifica."
            else:
                return True, "Accesso in sola lettura."
        
        except Exception as e:
            return False, f"Errore durante il controllo dell'accesso: {str(e)}"

    def close_session(self):
        self.session.close()