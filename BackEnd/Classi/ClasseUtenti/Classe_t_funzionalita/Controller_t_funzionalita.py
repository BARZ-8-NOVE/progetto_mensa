from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from werkzeug.exceptions import NotFound

t_funzionalita_controller = Blueprint('funzionalita', __name__)
service_t_funzionalita = Service_t_funzionalita()
httpCodes = HttpCodes()

@t_funzionalita_controller.route('/get_all', methods=['GET'])
def get_funzionalita_all():
    try:
        funzionalita = service_t_funzionalita.get_funzionalita_all()
        return funzionalita
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_funzionalita_controller.route('/get_funzionalita/<int:id>', methods=['GET'])
def get_funzionalita_by_id(id):
    try:
        funzionalita = service_t_funzionalita.get_funzionalita_by_id(id)
        return funzionalita
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_funzionalita_controller.route('/create_funzionalita', methods=['POST'])
def create_funzionalita():
    try:
        dati = request.json
        required_fields = ['nome', 'frmNome']
        UtilityGeneral.check_fields(dati, required_fields)
        nome = dati['nome']
        frmNome = dati['frmNome']
        return service_t_funzionalita.create_funzionalita(nome, frmNome)
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_funzionalita_controller.route('/update_funzionalita', methods=['PUT'])
def update_funzionalita():
    try:
        dati = request.json
        required_fields = ['id', 'nome', 'frmNome']
        UtilityGeneral.check_fields(dati, required_fields)
        id = UtilityGeneral.safe_int_convertion(dati['id'], 'id')
        nome = dati['nome']
        frmNome = dati['frmNome']
        service_t_funzionalita.update_funzionalita_nome(id, nome)
        service_t_funzionalita.update_funzionalita_frmNome(id, frmNome)
        return {'Funzionalita updated': f'id: {id}, nome: {nome}, frmNome: {frmNome}'}
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_funzionalita_controller.route('/delete_funzionalita/<int:id>', methods=['DELETE'])
def delete_funzionalita(id):
    try:
        id = UtilityGeneral.safe_int_convertion(id, 'id')
        result = service_t_funzionalita.delete_funzionalita(id)
        return result
    except ValueError as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
    