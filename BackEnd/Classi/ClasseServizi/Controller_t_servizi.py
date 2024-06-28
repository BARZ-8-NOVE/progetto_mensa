from flask import Blueprint, request
from Classi.ClasseServizi.Service_t_servizi import ServiceTServizi

t_servizi_controller = Blueprint('t_servizi_controller', __name__)
service_t_servizi = ServiceTServizi()

@t_servizi_controller.route('/servizi', methods=['GET'])
def get_all_servizi():
    return service_t_servizi.get_all_servizi()

@t_servizi_controller.route('/servizi/<int:id>', methods=['GET'])
def get_servizio_by_id(id):
    return service_t_servizi.get_servizio_by_id(id)

@t_servizi_controller.route('/servizi', methods=['POST'])
def create_servizio():
    dati = request.json
    if 'descrizione' not in dati or 'ordinatore' not in dati or 'inMenu' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        descrizione = str(dati['descrizione'])
        ordinatore = int(dati['ordinatore'])
        inMenu = bool(dati['inMenu'])
        return service_t_servizi.create_servizio(descrizione, ordinatore, inMenu)
    except Exception as e:
        return {'Error': str(e)}, 403

@t_servizi_controller.route('/servizi/<int:id>', methods=['PUT'])
def update_servizio(id):
    dati = request.json
    descrizione = dati.get('descrizione', None)
    ordinatore = dati.get('ordinatore', None)
    inMenu = dati.get('inMenu', None)
    return service_t_servizi.update_servizio(id, descrizione, ordinatore, inMenu)

@t_servizi_controller.route('/servizi/<int:id>', methods=['DELETE'])
def delete_servizio(id):
    return service_t_servizi.delete_servizio(id)
