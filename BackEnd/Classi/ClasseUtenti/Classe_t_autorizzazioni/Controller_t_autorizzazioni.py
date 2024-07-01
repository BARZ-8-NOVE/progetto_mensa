from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Service_t_autorizzazioni import Service_t_autorizzazioni
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from werkzeug.exceptions import NotFound

t_autorizzazioni_controller = Blueprint('autorizzazioni', __name__)
service_t_autorizzazioni = Service_t_autorizzazioni()
httpCodes = HttpCodes()

@t_autorizzazioni_controller.route('/get_all', methods=['GET'])
def get_autorizzazioni_all():
    try:
        autorizzazioni = service_t_autorizzazioni.get_autorizzazioni_all()
        return autorizzazioni, httpCodes.OK
    except Exception as e:
            return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_autorizzazioni_controller.route('/get_autorizzazione/<int:id>', methods=['GET'])
def get_autorizzazione_by_id(id):
    try:
        autorizzazione = service_t_autorizzazioni.get_autorizzazioni_by_id(id)
        return autorizzazione, httpCodes.OK
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_autorizzazioni_controller.route('/create_autorizzazione', methods=['POST'])
def create_autorizzazione():
    try:
        dati = request.json
        required_fields = ['nome', 'fkListaFunzionalita']
        UtilityGeneral.check_fields(dati, required_fields)
        nome = dati['nome']
        fkListaFunzionalita = dati['fkListaFunzionalita']
        return service_t_autorizzazioni.create_autorizzazione(nome, fkListaFunzionalita),httpCodes.OK
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_autorizzazioni_controller.route('/update_autorizzazione', methods=['PUT'])
def update_autorizzazione():
    try:
        dati = request.json
        required_fields = ['id', 'nome', 'fkListaFunzionalita']
        UtilityGeneral.check_fields(dati, required_fields)
        id = UtilityGeneral.safe_int_convertion(dati['id'], 'id')
        nome = dati['nome']
        fkListaFunzionalita = dati['fkListaFunzionalita']
        service_t_autorizzazioni.update_autorizzazione_nome(id, nome)
        service_t_autorizzazioni.update_autorizzazione_fkListaFunzionalita(id, fkListaFunzionalita)
        return {'Autorizzazione updated': f'id:{id}, nome: {nome}, fkListaFunzionalita: {fkListaFunzionalita}'}, httpCodes.OK
    except KeyError as e:
        return {'Error': str(e)}, httpCodes.BAD_REQUEST
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_autorizzazioni_controller.route('/delete_autorizzazione/<int:id>', methods=['DELETE'])
def delete_autorizzazione(id):
    try:
        id = UtilityGeneral.safe_int_convertion(id, 'id')
        service_t_autorizzazioni.delete_autorizzazione(id)
        return {'Autorizzazione deleted': f'id: {id}'}, httpCodes.OK
    except ValueError as e:
        return {'Error': str(e)}, httpCodes.UNPROCESSABLE_ENTITY
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR