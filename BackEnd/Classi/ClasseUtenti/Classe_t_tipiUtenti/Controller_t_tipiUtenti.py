from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Service_t_tipiUtenti import Service_t_tipiUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from werkzeug.exceptions import NotFound

t_tipiUtenti_controller = Blueprint('tipiUtenti', __name__)
service_t_tipiUtenti = Service_t_tipiUtenti()
httpCodes = HttpCodes()

@t_tipiUtenti_controller.route('/get_all', methods=['GET'])
def get_tipiUtenti_all():
    try:
        tipiUtenti = service_t_tipiUtenti.get_tipiUtenti_all()
        return tipiUtenti, httpCodes.OK
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_tipiUtenti_controller.route('/get_tipoUtente/<int:id>', methods=['GET'])
def get_tipoUtente_by_id(id):
    try:
        tipoUtente = service_t_tipiUtenti.get_tipoUtente_by_id(id)
        return tipoUtente, httpCodes.OK
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_tipiUtenti_controller.route('/create_tipoUtente', methods=['POST'])
def create_tipoUtente():
    try:
        dati = request.json
        required_fields = ['nomeTipoUtente', 'fkAutorizzazioni']
        UtilityGeneral.check_fields(dati, required_fields)
        nomeTipoUtente = dati['nomeTipoUtente']
        fkAutorizzazioni = dati['fkAutorizzazioni']
        return service_t_tipiUtenti.create_tipoUtente(nomeTipoUtente, fkAutorizzazioni), httpCodes.OK
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_tipiUtenti_controller.route('/update_tipoUtente', methods=['PUT'])
def update_tipoUtente():
    try:
        dati = request.json
        required_fields = ['id', 'nomeTipoUtente', 'fkAutorizzazioni']
        UtilityGeneral.check_fields(dati, required_fields)
        id = UtilityGeneral.safe_int_convertion(dati['id'], 'id')
        nomeTipoUtente = dati['nomeTipoUtente']
        fkAutorizzazioni = dati['fkAutorizzazioni']
        service_t_tipiUtenti.update_tipoUtente_nomeTipoUtente(id, nomeTipoUtente)
        service_t_tipiUtenti.update_tipoUtente_fkAutorizzazioni(id, fkAutorizzazioni)
        return {'TipoUtente updated': f'id: {id}, nomeTipoUtente: {nomeTipoUtente}, fkAutorizzazioni: {fkAutorizzazioni}'}, httpCodes.OK
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_tipiUtenti_controller.route('/delete_tipoUtente/<int:id>', methods=['DELETE'])
def delete_tipoUtente(id):
    try:
        id = UtilityGeneral.safe_int_convertion(id, 'id')
        result = service_t_tipiUtenti.delete_tipoUtente(id)
        if not result:
            return {'TipoUtente deleted': f'id: {id}'}
        else:
            return {'You cannot delete this tipoUtente because associated at some utenti':
                UtilityGeneral.getClassDictionaryOrList(result)}, httpCodes.FORBIDDEN
    except ValueError as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    