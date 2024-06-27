from flask import Blueprint, request, jsonify
from Classi.ClasseAlimenti.Classe_t_tipologiaconservazione.Service_t_tipologiaconservazione import ServiceTipologiaConservazioni

t_tipologiaconservazioni_controller = Blueprint('tipologiaconservazioni', __name__)
service_tipologiaconservazioni = ServiceTipologiaConservazioni()

@t_tipologiaconservazioni_controller.route('/get_all', methods=['GET'])
def get_all():
    funzionalita = service_tipologiaconservazioni.get_all()
    return jsonify(funzionalita)

@t_tipologiaconservazioni_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    tipologiaconservazioni = service_tipologiaconservazioni.get_by_id(id)
    return jsonify(tipologiaconservazioni)

@t_tipologiaconservazioni_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    if 'id' not in dati or 'nome' not in dati:
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        id = int(dati['id'])
        if id <= 0:
            raise ValueError("id cannot be equal or less than 0")
        nome = dati['nome'].strip()
        if not nome or len(nome) > 50:
            raise ValueError("nome cannot be empty and must be less than 50 characters!")
        return jsonify(service_tipologiaconservazioni.create(id, nome))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_tipologiaconservazioni_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    tipologiaconservazioni = service_tipologiaconservazioni.delete(id)
    return jsonify(tipologiaconservazioni)
