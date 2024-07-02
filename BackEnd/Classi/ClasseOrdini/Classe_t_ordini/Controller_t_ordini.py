from flask import Blueprint, request, jsonify
from Classi.ClasseOrdini.Classe_t_ordini.Service_t_ordini import ServiceOrdini

t_ordini_controller = Blueprint('ordini', __name__)
service_ordini = ServiceOrdini()

@t_ordini_controller.route('/get_all', methods=['GET'])
def get_all_ordini():
    return jsonify(service_ordini.get_all())

@t_ordini_controller.route('/<int:id>', methods=['GET'])
def get_ordine_by_id(id):
    return jsonify(service_ordini.get_by_id(id))

@t_ordini_controller.route('/create', methods=['POST'])
def create_ordine():
    dati = request.json
    required_keys = ['fkReparto', 'data', 'fkServizio', 'cognome', 'nome', 'dataInserimento', 'utenteInserimento']
    if not all(key in dati for key in required_keys):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkReparto = int(dati['fkReparto'])
        data = dati['data']
        fkServizio = int(dati['fkServizio'])
        cognome = str(dati['cognome'])
        nome = str(dati['nome'])
        letto = str(dati.get('letto', None))  # Utilizzo di get() per gestire il valore opzionale
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])
        return jsonify(service_ordini.create(fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_ordini_controller.route('/update/<int:id>', methods=['PUT'])
def update_ordine(id):
    dati = request.json
    required_keys = ['fkReparto', 'data', 'fkServizio', 'cognome', 'nome', 'dataInserimento', 'utenteInserimento']
    if not all(key in dati for key in required_keys):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkReparto = int(dati['fkReparto'])
        data = dati['data']
        fkServizio = int(dati['fkServizio'])
        cognome = str(dati['cognome'])
        nome = str(dati['nome'])
        letto = str(dati.get('letto', None))  # Utilizzo di get() per gestire il valore opzionale
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])
        return jsonify(service_ordini.update(id, fkReparto, data, fkServizio, cognome, nome, letto, dataInserimento, utenteInserimento))
    except Exception as e:
        return jsonify({'Error': str(e)}), 403

@t_ordini_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_ordine(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_ordini.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
