from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from werkzeug.exceptions import Conflict, NotFound

t_utenti_controller = Blueprint('utenti', __name__)
service_t_utenti = Service_t_utenti()
httpCodes = HttpCodes()

@t_utenti_controller.route('/get_all', methods=['GET'])
def get_utenti_all():
    try:
        utenti = service_t_utenti.get_utenti_all()
        return utenti, httpCodes.OK
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_utenti_controller.route('/get_utente/<int:id>', methods=['GET'])
def get_utente_by_id(id):
    try:
        utente = service_t_utenti.get_utente_by_id(id)
        return utente, httpCodes.OK
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_utenti_controller.route('/create_utente', methods=['POST'])
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
        return service_t_utenti.create_utente(username, nome, cognome, fkTipoUtente, fkFunzCustom, reparti, email, password), httpCodes.OK
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Conflict as e:
        return {'Error': str(e)}, httpCodes.CONFLICT
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_utenti_controller.route('/update_utente', methods=['PUT'])
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
        service_t_utenti.update_utente_username(id, username)
        service_t_utenti.update_utente_nome(id, nome)
        service_t_utenti.update_utente_cognome(id, cognome)
        service_t_utenti.update_utente_fkTipoUtente(id, fkTipoUtente)
        service_t_utenti.update_utente_fkFunzCustom(id, fkFunzCustom)
        service_t_utenti.update_utente_reparti(id, reparti)
        service_t_utenti.update_utente_attivo(id, attivo)
        service_t_utenti.update_utente_email(id, email)
        service_t_utenti.update_utente_password(id, password)
        return {
            'Utente updated': f'id: {id}, username: {username}, nome: {nome}, cognome: {cognome}, '
                              f'fkTipoUtente: {fkTipoUtente}, fkFunzCustom: {fkFunzCustom}, reparti: {reparti}, '
                              f'attivo: {attivo}, email: {email}, password: {password}'
        }, httpCodes.OK
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except ValueError as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Conflict as e:
        return {'Error': str(e)}, httpCodes.CONFLICT
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

    
@t_utenti_controller.route('/delete_utente/<int:id>', methods=['DELETE'])
def delete_utente(id):
    try:
        id = UtilityGeneral.safe_int_convertion(id, 'id')
        result = service_t_utenti.delete_utente(id)
        return result, httpCodes.OK
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except ValueError as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    