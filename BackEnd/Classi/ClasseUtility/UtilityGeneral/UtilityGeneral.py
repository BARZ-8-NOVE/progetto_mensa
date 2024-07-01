from datetime import datetime
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Domain_t_autorizzazioni import TAutorizzazioni
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages

class UtilityGeneral:    
    
    @staticmethod
    def safe_int_convertion(value, variableName):
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Conversion error to Integer of {variableName}")

    @staticmethod
    def check_fields(dati, required_fields):
        if not all(field in dati for field in required_fields):
            raise KeyError(UtilityMessages.wrongKeysErrorMessage())
        
    @staticmethod
    def checkId(id):
        if id is None:
            raise TypeError("id cannot be None!")
        if (id < 0) or (id == 0):
            raise ValueError("id cannot be None, 0, or less than 0!")
        
    @staticmethod
    def current_date():
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        return current_date
    
    @staticmethod
    def getClassDictionaryOrList(results):
        if isinstance(results, (TUtenti, list)):
            if isinstance(results, TUtenti):  
                ritorno = {'id': results.id, 'username': results.username, 'nome': results.nome,
                        'cognome': results.cognome, 'fkTipoUtente': results.fkTipoUtente,
                        'fkFunzCustom': results.fkFunzCustom, 'reparti': results.reparti,
                        'attivo': results.attivo, 'inizio': results.inizio,
                        'email': results.email, 'password': results.password}
            elif all(isinstance(item, TUtenti) for item in results):
                ritorno = []
                for result in results:
                    ritorno.append({'id': result.id, 'username': result.username, 'nome': result.nome,
                        'cognome': result.cognome, 'fkTipoUtente': result.fkTipoUtente,
                        'fkFunzCustom': result.fkFunzCustom, 'reparti': result.reparti,
                        'attivo': result.attivo, 'inizio': result.inizio,
                        'email': result.email, 'password': result.password})
        if isinstance(results, (TTipiUtenti, list)):
            if isinstance(results, TTipiUtenti):
                ritorno = {'id': results.id, 'nomeTipoUtente': results.nomeTipoUtente,
                           'fkAutorizzazioni': results.fkAutorizzazioni}
            elif all(isinstance(item, TTipiUtenti) for item in results):
                ritorno = []
                for result in results:
                    ritorno.append({'id': result.id, 'nomeTipoUtente': result.nomeTipoUtente,
                           'fkAutorizzazioni': result.fkAutorizzazioni})
        if isinstance(results, (TAutorizzazioni, list)):
            if isinstance(results, TAutorizzazioni):
                ritorno = {'id': results.id, 'nome': results.nome,
                           'fkListaFunzionalita': results.fkListaFunzionalita}
            elif all(isinstance(item, TAutorizzazioni) for item in results):
                ritorno = []
                for result in results:
                    ritorno.append({'id': result.id, 'nome': result.nome,
                           'fkListaFunzionalita': result.fkListaFunzionalita})
        if isinstance(results, (TFunzionalita, list)):
            if isinstance(results, TFunzionalita):
                ritorno = {'id': results.id, 'nome': results.nome,
                           'frmNome': results.frmNome}
            elif all(isinstance(item, TFunzionalita) for item in results):
                ritorno = []
                for result in results:
                    ritorno.append({'id': result.id, 'nome': result.nome,
                           'frmNome': result.frmNome})
        return ritorno