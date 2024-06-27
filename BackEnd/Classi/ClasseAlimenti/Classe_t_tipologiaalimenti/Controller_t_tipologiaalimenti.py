from flask import Blueprint, request, jsonify
from Classi.ClasseAlimenti.Classe_t_tipologiaalimenti.Service_t_tipologiaalimenti import ServiceTipologiaAlimenti

t_tipologiaalimenti_controller = Blueprint('tipologiaalimenti', __name__)
service_tipologiaalimenti = ServiceTipologiaAlimenti()

@t_tipologiaalimenti_controller.route('/get_all', methods=['GET'])
def get_all():
    alimenti = service_tipologiaalimenti.get_all()
    return jsonify(alimenti)

@t_tipologiaalimenti_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    alimento = service_tipologiaalimenti.get_by_id(id)
    return jsonify(alimento)

@t_tipologiaalimenti_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    if 'nome' not in dati or 'conservazione_id' not in dati:
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        nome = dati['nome'].strip()
        descrizione = dati.get('descrizione', '').strip()
        conservazione_id = int(dati['conservazione_id'])
        if not nome or len(nome) > 50:
            raise ValueError("nome cannot be empty and must be less than 50 characters!")
        return jsonify(service_tipologiaalimenti.create(nome, descrizione, conservazione_id))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_tipologiaalimenti_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    if 'nome' not in dati or 'conservazione_id' not in dati:
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        nome = dati['nome'].strip()
        descrizione = dati.get('descrizione', '').strip()
        conservazione_id = int(dati['conservazione_id'])
        if not nome or len(nome) > 50:
            raise ValueError("nome cannot be empty and must be less than 50 characters!")
        return jsonify(service_tipologiaalimenti.update(id, nome, descrizione, conservazione_id))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_tipologiaalimenti_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    alimento = service_tipologiaalimenti.delete(id)
    return jsonify(alimento)
