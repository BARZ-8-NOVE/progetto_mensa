from flask import Blueprint, request
from Classi.ClassePreparazioni.Classe_t_tipoPreparazioni.Service_t_tipoPreparazioni import Service_t_tipipreparazioni

t_tipipreparazioni_controller = Blueprint('tipipreparazioni', __name__)
service_t_tipipreparazioni = Service_t_tipipreparazioni()

@t_tipipreparazioni_controller.route('/get_all', methods=['GET'])
def get_all_tipipreparazioni():
    return service_t_tipipreparazioni.get_all_tipipreparazioni()

@t_tipipreparazioni_controller.route('/<int:id>', methods=['GET'])
def get_tipipreparazioni_by_id(id):
    return service_t_tipipreparazioni.get_tipipreparazioni_by_id(id)

@t_tipipreparazioni_controller.route('/create', methods=['POST'])
def create_tipipreparazioni():
    dati = request.json
    if 'descrizione' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        descrizione = dati['descrizione']
        return service_t_tipipreparazioni.create_tipipreparazioni(descrizione)
    except Exception as e:
        return {'Error': str(e)}, 403

@t_tipipreparazioni_controller.route('/update/<int:id>', methods=['PUT'])
def update_tipipreparazioni(id):
    dati = request.json
    descrizione = dati.get('descrizione')
    return service_t_tipipreparazioni.update_tipipreparazioni(id, descrizione)

@t_tipipreparazioni_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_tipipreparazioni(id):
    return service_t_tipipreparazioni.delete_tipipreparazioni(id)
