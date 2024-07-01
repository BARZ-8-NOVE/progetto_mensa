from flask import Blueprint, request, jsonify
from Classi.ClassePiatti.Classe_t_tipiPiatti.Service_t_tipiPiatti import ServiceTipiPiatti
from datetime import datetime

t_tipi_piatti_controller = Blueprint('tipi_piatti', __name__)
service_tipi_piatti = ServiceTipiPiatti()

@t_tipi_piatti_controller.route('/get_all', methods=['GET'])
def get_all():
    tipi_piatti = service_tipi_piatti.get_all()
    return jsonify(tipi_piatti)

@t_tipi_piatti_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    tipo_piatto = service_tipi_piatti.get_by_id(id)
    return jsonify(tipo_piatto)

@t_tipi_piatti_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    required_fields = ['descrizione', 'descrizionePlurale', 'inMenu', 'ordinatore', 'color', 'backgroundColor', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        descrizione = dati['descrizione'].strip()
        descrizionePlurale = dati['descrizionePlurale'].strip()
        inMenu = bool(dati['inMenu'])
        ordinatore = int(dati['ordinatore'])
        color = dati['color'].strip()
        backgroundColor = dati['backgroundColor'].strip()
        dataInserimento = dati.get('dataInserimento', datetime.now())
        utenteInserimento = dati['utenteInserimento'].strip()

        return jsonify(service_tipi_piatti.create(descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_tipi_piatti_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    required_fields = ['descrizione', 'descrizionePlurale', 'inMenu', 'ordinatore', 'color', 'backgroundColor', 'utenteInserimento']

    # Check for missing fields
    for field in required_fields:
        if field not in dati or dati[field] is None:
            return jsonify({'Error': f'{field} is required and cannot be None'}), 403

    try:
        descrizione = dati['descrizione'].strip()
        descrizionePlurale = dati['descrizionePlurale'].strip()
        inMenu = bool(dati['inMenu'])
        ordinatore = int(dati['ordinatore'])
        color = dati['color'].strip()
        backgroundColor = dati['backgroundColor'].strip()
        dataInserimento = dati.get('dataInserimento', datetime.now())
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati.get('dataCancellazione')
        utenteCancellazione = dati.get('utenteCancellazione', '').strip() if dati.get('utenteCancellazione') else None

        return jsonify(service_tipi_piatti.update(id, descrizione, descrizionePlurale, inMenu, ordinatore, color, backgroundColor, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_tipi_piatti_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione is required and cannot be None'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_tipi_piatti.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500