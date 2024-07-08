from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClasseReparti.Service_t_reparti import ServiceReparti

t_reparti_controller = Blueprint('reparti', __name__)
service_reparti = ServiceReparti()

@t_reparti_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_reparti_all():
    return jsonify(service_reparti.get_all())

@t_reparti_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_reparti_by_id(id):
    return jsonify(service_reparti.get_by_id(id))

@t_reparti_controller.route('/create', methods=['POST'])
@jwt_required()
def create_reparti():
    dati = request.json
    required_fields = ['codiceAreas', 'descrizione', 'sezione', 'ordinatore', 'padiglione', 'piano', 'lato', 'inizio', 'fine', 'dataInserimento', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        return jsonify(service_reparti.create(**dati))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_reparti_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_reparti(id):
    dati = request.json
    required_fields = ['codiceAreas', 'descrizione', 'sezione', 'ordinatore', 'padiglione', 'piano', 'lato', 'inizio', 'fine', 'dataInserimento', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        return jsonify(service_reparti.update(id, **dati))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_reparti_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_reparti.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
