from datetime import datetime
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Domain_t_autorizzazioni import TAutorizzazioni
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityMessages import UtilityMessages
from werkzeug.exceptions import Conflict, NotFound, Forbidden, Unauthorized

class UtilityGeneral:   
    """Class for the utility general""" 
    
    # Empty Constructor
    def __init__(self) -> None:
        pass

    # Static methods
    @staticmethod
    def safe_int_convertion(value, variableName):
        """
        :description: Static method that try to convert the variable value into an integer.
        If it cannot convert the value into an integer the function will raise a ValueError
        :args: value, variableName
        :return: int(value) | raise ValueError
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Conversion error to Integer of {variableName}")
        
    @staticmethod
    def check_token_header(required_field, header):
        if required_field not in header:    
            raise Unauthorized(UtilityMessages.unauthorizedErrorToken('missing in headers'))

    @staticmethod
    def check_fields(dati, required_fields):
        """
        :description: Static method that checks if all required_fields are in dati, 
        if not the function will raise a KeyError
        :args: dati, required_fields
        :return: None | raise KeyError
        """
        if not all(field in dati for field in required_fields):
            raise KeyError(UtilityMessages.wrongKeysErrorMessage())
        
    @staticmethod
    def checkId(id:int):
        """
        :description: Static method that checks if id is None, it will raise a TypeError,
        and checks if id is less or equal of 0 if will raise a ValueError
        or will return None if not of the above conditions are true
        :args: id
        :return: None | raise TypeError | raise ValueError
        """
        if id is None:
            raise TypeError("id cannot be None!")
        if id <= 0:
            raise ValueError("id cannot be None, 0, or less than 0!")
        
    @staticmethod
    def current_date():
        """
        :description: Static method that return the current date when it's called.
        The format is (%Y-%m-%d)
        :return: current_date
        """
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        return current_date
    
    @staticmethod
    def getClassDictionaryOrList(results):
        """
        :description: Static method that checks result if isinstance of a list or of a class and return only a dictionary
        if is instance of a class or a list of dictionaries if is instance of a list
        :args: result[dict(str:any) | list(dict(str:any))]
        :return: dict(str:any) | list(dict(str:any))
        """
        if isinstance(results, (TUtenti, list)):
            if isinstance(results, TUtenti):  
                ritorno = {'id': results.id, 'username': results.username, 'nome': results.nome,
                        'cognome': results.cognome, 'fkTipoUtente': results.fkTipoUtente,
                        'fkFunzCustom': results.fkFunzCustom, 'reparti': results.reparti,
                        'attivo': results.attivo, 'inizio': results.inizio,
                        'email': results.email}
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