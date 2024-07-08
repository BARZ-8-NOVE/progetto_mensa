from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Service_t_ordiniPiatti import ServiceOrdiniPiatti

t_ordini_piatti_controller = Blueprint('ordinipiatti', __name__)
service_ordini_piatti = ServiceOrdiniPiatti()

@t_ordini_piatti_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_ordini_piatti():
    return jsonify(service_ordini_piatti.get_all())

@t_ordini_piatti_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_ordine_piatto_by_id(id):
    return jsonify(service_ordini_piatti.get_by_id(id))

@t_ordini_piatti_controller.route('/create', methods=['POST'])
@jwt_required()
def create_ordine_piatto():
    dati = request.json
    required_keys = ['fkOrdineScheda', 'fkPiatto', 'quantita', 'note']
    if not all(key in dati for key in required_keys):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkOrdineScheda = int(dati['fkOrdineScheda'])
        fkPiatto = int(dati['fkPiatto'])
        quantita = int(dati['quantita'])
        note = str(dati['note'])
        return jsonify(service_ordini_piatti.create(fkOrdineScheda, fkPiatto, quantita, note))
    except Exception as e:
        return {'Error': str(e)}, 403

@t_ordini_piatti_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_ordine_piatto(id):
    dati = request.json
    required_keys = ['fkOrdineScheda', 'fkPiatto', 'quantita', 'note']
    if not all(key in dati for key in required_keys):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkOrdineScheda = int(dati['fkOrdineScheda'])
        fkPiatto = int(dati['fkPiatto'])
        quantita = int(dati['quantita'])
        note = str(dati['note'])
        return jsonify(service_ordini_piatti.update(id, fkOrdineScheda, fkPiatto, quantita, note))
    except Exception as e:
        return {'Error': str(e)}, 403

@t_ordini_piatti_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ordine_piatto(id):
    try:
        return jsonify(service_ordini_piatti.delete(id))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
