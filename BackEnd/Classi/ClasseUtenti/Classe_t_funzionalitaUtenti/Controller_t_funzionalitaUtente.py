from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Service_t_funzionalitaUtente import TFunzionalitaUtenteService

t_funzionalitaUtenti_controller = Blueprint('funzionalita_utenti', __name__)
service_t_funz_utenti = TFunzionalitaUtenteService()

@t_funzionalitaUtenti_controller.route("/<int:funzionalita_utente_id>", methods=['GET'])
def get_funzionalita_utente(funzionalita_utente_id):  
    funzionalita_utente = service_t_funz_utenti.get_funzionalita_utente_by_id(funzionalita_utente_id)
    if funzionalita_utente:
        return {'id': funzionalita_utente.id, 'fkTipoUtente': funzionalita_utente.fkTipoUtente, 'fkFunzionalita': funzionalita_utente.fkFunzionalita, 'permessi': funzionalita_utente.permessi}
    else:
        return {'error': 'FunzionalitaUtente not found'}, 404

@t_funzionalitaUtenti_controller.route("/tipo_utente/<int:tipo_utente_id>", methods=['GET'])
def get_funzionalita_utenti_by_user_type(tipo_utente_id):
    funzionalita_utenti = service_t_funz_utenti.get_funzionalita_utenti_by_user_type(tipo_utente_id)
    return [{'id': fu.id, 'fkTipoUtente': fu.fkTipoUtente, 'fkFunzionalita': fu.fkFunzionalita, 'permessi': fu.permessi} for fu in funzionalita_utenti]

@t_funzionalitaUtenti_controller.route("/funzionalita/<int:funzionalita_id>", methods=['GET'])
def get_funzionalita_utenti_by_funzionalita(funzionalita_id):
    funzionalita_utenti = service_t_funz_utenti.get_funzionalita_utenti_by_funzionalita(funzionalita_id)
    return [{'id': fu.id, 'fkTipoUtente': fu.fkTipoUtente, 'fkFunzionalita': fu.fkFunzionalita, 'permessi': fu.permessi} for fu in funzionalita_utenti]