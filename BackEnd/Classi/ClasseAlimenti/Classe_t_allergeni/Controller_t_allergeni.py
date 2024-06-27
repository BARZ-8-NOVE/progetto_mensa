from flask import Blueprint, request, jsonify
from Classi.ClasseAlimenti.Classe_t_allergeni.Service_t_allergeni import ServiceAllergeni

t_allergeni_controller = Blueprint('allergeni', __name__)
service_allergeni = ServiceAllergeni()

@t_allergeni_controller.route('/get_all', methods=['GET'])
def get_all():
    allergeni = service_allergeni.get_all()
    return jsonify(allergeni)

@t_allergeni_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    allergene = service_allergeni.get_by_id(id)
    return jsonify(allergene)

@t_allergeni_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    if 'nome' not in dati:
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        nome = dati['nome'].strip()
        if not nome or len(nome) > 50:
            raise ValueError("nome cannot be empty and must be less than 50 characters!")
        return jsonify(service_allergeni.create(nome))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_allergeni_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    if 'nome' not in dati:
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        nome = dati['nome'].strip()
        if not nome or len(nome) > 50:
            raise ValueError("nome cannot be empty and must be less than 50 characters!")
        return jsonify(service_allergeni.update(id, nome))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_allergeni_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    allergene = service_allergeni.delete(id)
    return jsonify(allergene)
