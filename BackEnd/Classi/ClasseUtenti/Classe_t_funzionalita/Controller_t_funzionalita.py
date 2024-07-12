from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from werkzeug.exceptions import NotFound

t_funzionalita_controller = Blueprint('funzionalita', __name__)
service_t_funzionalita = Service_t_funzionalita()
httpCodes = HttpCodes()

@t_funzionalita_controller.route('/get_all', methods=['GET'])
def get_funzionalita_all():
    try:
        funzionalita = service_t_funzionalita.get_all_menus()
        return funzionalita
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR

@t_funzionalita_controller.route('get_id/<int:id>', methods=['GET'])
def get_funzionalita_by_id(id):
    try:
        funzionalita = service_t_funzionalita.get_menu_by_id(id)
        return funzionalita
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR
    
@t_funzionalita_controller.route('get_padre/<int:fkPadre>', methods=['GET'])
def get_funzionalita_by_padre(fkPadre):
    try:
        funzionalita = service_t_funzionalita.get_all_children(fkPadre)
        return funzionalita
    except NotFound as e:
        return {'Error': str(e)}, httpCodes.NOT_FOUND
    except Exception as e:
        return {'Error': str(e)}, httpCodes.INTERNAL_SERVER_ERROR


