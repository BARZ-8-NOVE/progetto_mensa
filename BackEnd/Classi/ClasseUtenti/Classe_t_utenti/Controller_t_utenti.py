from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

t_utenti_controller = Blueprint('utenti', __name__)
service_t_utenti = Service_t_utenti()

@t_utenti_controller.route('/get_all', methods=['GET'])
def get_utenti_all():
    try:
        utenti = service_t_utenti.get_utenti_all()
        return utenti
    except Exception as e:
        return {'Error': str(e)}, 400

@t_utenti_controller.route('/get_utente/<int:id>', methods=['GET'])
def get_utente_by_id(id):
    try:
        utente = service_t_utenti.get_utente_by_id(id)
        return utente
    except Exception as e:
        return {'Error': str(e)}, 400

@t_utenti_controller.route('/create_utente', methods=['PUT'])
def create_utente():
    try:
        dati = request.json
        required_fields = ['username', 'nome', 'cognome', 'fkTipoUtente', 'fkFunzCustom', 'reparti', 'email', 'password']
        UtilityGeneral.check_fields(dati, required_fields)
        username = dati['username']
        nome = dati['nome']
        cognome = dati['cognome']
        fkTipoUtente = UtilityGeneral.safe_int_convertion(dati['fkTipoUtente'], 'fkTipoUtente')
        fkFunzCustom = dati['fkFunzCustom']
        reparti = dati['reparti']
        email = dati['email']
        password = dati['password']
        return service_t_utenti.create_utente(username, nome, cognome, fkTipoUtente, fkFunzCustom, reparti, email, password)
    except KeyError as e:
        return {'Error': str(e)}, 405
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, 422
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_utenti_controller.route('/update_utente', methods=['POST'])
def update_utente():
    try:
        dati = request.json
        required_fields = ['id', 'username', 'nome', 'cognome', 'fkTipoUtente', 'fkFunzCustom', 'reparti', 'attivo', 'email', 'password']
        UtilityGeneral.check_fields(dati, required_fields)
        id = UtilityGeneral.safe_int_convertion(dati['id'], 'id')
        username = dati['username']
        nome = dati['nome']
        cognome = dati['cognome']
        fkTipoUtente = UtilityGeneral.safe_int_convertion(dati['fkTipoUtente'], 'fkTipoUtente')
        fkFunzCustom = dati['fkFunzCustom']
        reparti = dati['reparti']
        attivo = UtilityGeneral.safe_int_convertion(dati['attivo'], 'attivo')
        email = dati['email']
        password = dati['password']
        return service_t_utenti.update_utente(id, username, nome, cognome, fkTipoUtente,
                                            fkFunzCustom, reparti, attivo, email, password)
    except KeyError as e:
        return {'Error': str(e)}, 405
    except ValueError as e:
        return {'Error': str(e)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_utenti_controller.route('/delete_utente/<int:id>', methods=['DELETE'])
def delete_utente(id):
    try:
        id = UtilityGeneral.safe_int_convertion(id, 'id')
        result = service_t_utenti.delete_utente(id)
        return result
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    