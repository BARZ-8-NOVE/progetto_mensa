from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClassePiatti.Classe_t_piatti.Service_t_piatti import Service_t_Piatti
from datetime import datetime

t_piatti_controller = Blueprint('piatti', __name__)
service_piatti = Service_t_Piatti()

@t_piatti_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all():
    piatti = service_piatti.get_all()
    return jsonify(piatti)

@t_piatti_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    piatto = service_piatti.get_by_id(id)
    return jsonify(piatto)


@t_piatti_controller.route('/create', methods=['POST'])
@jwt_required()
def create():
    dati = request.json
    required_fields = ['fkTipoPiatto', 'codice', 'titolo', 'descrizione', 'inMenu', 'ordinatore', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkTipoPiatto = int(dati['fkTipoPiatto'])
        codice = dati['codice'].strip()
        titolo = dati['titolo'].strip()
        descrizione = dati['descrizione'].strip() if dati.get('descrizione') else None
        inMenu = bool(dati['inMenu'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati.get('dataInserimento', datetime.now())
        utenteInserimento = dati['utenteInserimento'].strip()

        return jsonify(service_piatti.create(fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_piatti_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    dati = request.json
    required_fields = ['fkTipoPiatto', 'codice', 'titolo', 'inMenu', 'ordinatore', 'dataInserimento', 'utenteInserimento']
    
    for field in required_fields:
        if field not in dati or dati[field] is None:
            return jsonify({'Error': f'{field} is required and cannot be None'}), 403
    
    try:
        fkTipoPiatto = int(dati['fkTipoPiatto'])
        codice = dati['codice'].strip()
        titolo = dati['titolo'].strip()
        descrizione = dati['descrizione'].strip() if dati.get('descrizione') else None
        inMenu = bool(dati['inMenu'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati.get('dataInserimento', datetime.now())
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati.get('dataCancellazione')  # Assumi che sia una stringa già nel formato corretto
        utenteCancellazione = dati.get('utenteCancellazione', '').strip() if dati.get('utenteCancellazione') else None

        return jsonify(service_piatti.update(id, fkTipoPiatto, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_piatti_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_piatti.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
