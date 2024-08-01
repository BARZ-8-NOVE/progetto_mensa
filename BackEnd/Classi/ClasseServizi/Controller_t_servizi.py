from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from Classi.ClasseServizi.Service_t_servizi import Service_t_Servizi

t_servizi_controller = Blueprint('servizi', __name__)
service_t_servizi = Service_t_Servizi()

@t_servizi_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_servizi():
    return service_t_servizi.get_all_servizi()

@t_servizi_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_servizio_by_id(id):
    return service_t_servizi.get_servizio_by_id(id)

@t_servizi_controller.route('/create', methods=['POST'])
@jwt_required()
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

@t_servizi_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_servizio(id):
    dati = request.json
    descrizione = dati.get('descrizione', None)
    ordinatore = dati.get('ordinatore', None)
    inMenu = dati.get('inMenu', None)
    return service_t_servizi.update_servizio(id, descrizione, ordinatore, inMenu)

@t_servizi_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_servizio(id):
    return service_t_servizi.delete_servizio(id)
