from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from werkzeug.exceptions import Conflict, NotFound, Forbidden, Unauthorized
from server import jwt
from datetime import datetime, timezone

t_utenti_controller = Blueprint('utenti', __name__)
service_t_utenti = Service_t_utenti()
httpCodes = HttpCodes()

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    try:
        current_utente_public_id = jwt_payload['sub']
        service_t_utenti.do_logout(current_utente_public_id)
        response = jsonify({"Utente": "Logged out because the token has expired!"})
        unset_jwt_cookies(response)
        return response
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except KeyError as e:
        return jsonify({'Error': str(e)}), httpCodes.BAD_REQUEST
    except Unauthorized as e:
            return jsonify({'Error': str(e)}), httpCodes.UNAUTHORIZED
    except ValueError as e:
        return jsonify({'Error': str(e)}), httpCodes.UNPROCESSABLE_ENTITY
    except Forbidden as e:
        return jsonify({'Error': str(e)}), httpCodes.FORBIDDEN
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR
    
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    token_expiry = datetime.fromtimestamp(jwt_payload['exp'], timezone.utc)
    if token_expiry < datetime.now(timezone.utc):
        current_utente_public_id = jwt_payload['sub']
        service_t_utenti.do_logout(current_utente_public_id)
        return True
    return False
    
@t_utenti_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_utenti_all():
    try:
        utenti = service_t_utenti.get_utenti_all()
        return jsonify(utenti), httpCodes.OK
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR

@t_utenti_controller.route('/get_utente', methods=['GET'])
@jwt_required()
def get_utente_by_id():
    try:
        id = UtilityGeneral.safe_int_convertion(request.args.get('id'), 'id')
        utente = service_t_utenti.get_utente_by_id(id)
        return jsonify(utente), httpCodes.OK
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR

@t_utenti_controller.route('/create_utente', methods=['POST'])
def create_utente():
    try:
        dati = request.json
        required_fields = ['username', 'nome', 'cognome', 'fkTipoUtente', 'fkFunzCustom', 'reparti', 'email', 'password']
        UtilityGeneral.check_fields(dati, required_fields)
        username = dati['username']
        nome = dati['nome']
        cognome = dati['cognome']
        nomeTipoUtente = dati['fkTipoUtente'] #UtilityGeneral.safe_int_convertion(dati['fkTipoUtente'], 'fkTipoUtente')
        fkFunzCustom = dati['fkFunzCustom']
        reparti = dati['reparti']
        email = dati['email']
        password = dati['password']
        return jsonify(service_t_utenti.create_utente(username, nome, cognome, nomeTipoUtente, fkFunzCustom, reparti, email, password)), httpCodes.OK
    except KeyError as e:
        return jsonify({'Error': str(e)}), httpCodes.BAD_REQUEST
    except (ValueError, TypeError) as e:
        return jsonify({'Error': str(e)}), httpCodes.UNPROCESSABLE_ENTITY
    except Conflict as e:
        return jsonify({'Error': str(e)}), httpCodes.CONFLICT
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR
    
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
        return jsonify({
            'Utente updated': f'id: {id}, username: {username}, nome: {nome}, cognome: {cognome}, '
                              f'fkTipoUtente: {fkTipoUtente}, fkFunzCustom: {fkFunzCustom}, reparti: {reparti}, '
                              f'attivo: {attivo}, email: {email}'
        }), httpCodes.OK
    except KeyError as e:
        return jsonify({'Error': str(e)}), httpCodes.BAD_REQUEST
    except ValueError as e:
        return jsonify({'Error': str(e)}), httpCodes.UNPROCESSABLE_ENTITY
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except Conflict as e:
        return jsonify({'Error': str(e)}), httpCodes.CONFLICT
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR

@t_utenti_controller.route('/delete_utente/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_utente():
    try:
        id = UtilityGeneral.safe_int_convertion(request.args.get('id'), 'id')
        result = service_t_utenti.delete_utente(id)
        return jsonify(result), httpCodes.OK
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except ValueError as e:
        return jsonify({'Error': str(e)}), httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR
    
@t_utenti_controller.route('/do_login', methods=['POST'])
def do_login():
    try:
        dati = request.json
        required_fields = ['username', 'password']
        UtilityGeneral.check_fields(dati, required_fields)
        username = dati['username']
        password = dati['password']
        return jsonify(service_t_utenti.do_login(username, password)), httpCodes.OK
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except KeyError as e:
        return jsonify({'Error': str(e)}), httpCodes.BAD_REQUEST
    except ValueError as e:
        return jsonify({'Error': str(e)}), httpCodes.UNPROCESSABLE_ENTITY
    except Forbidden as e:
        return jsonify({'Error': str(e)}), httpCodes.FORBIDDEN
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR
    
@t_utenti_controller.route('/do_logout', methods=['POST'])
@jwt_required()
def do_logout():
    try:
        current_utente_public_id = get_jwt_identity()
        return jsonify(service_t_utenti.do_logout(current_utente_public_id)), httpCodes.OK
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except KeyError as e:
        return jsonify({'Error': str(e)}), httpCodes.BAD_REQUEST
    except ValueError as e:
        return jsonify({'Error': str(e)}), httpCodes.UNPROCESSABLE_ENTITY
    except Forbidden as e:
        return jsonify({'Error': str(e)}), httpCodes.FORBIDDEN
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR
    
