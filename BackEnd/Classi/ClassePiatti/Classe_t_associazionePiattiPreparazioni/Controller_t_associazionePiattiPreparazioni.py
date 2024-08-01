from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Service_t_associazionePiattiPreparazioni import Service_t_AssociazionePiattiPreparazionie
from datetime import datetime

t_associazione_controller = Blueprint('associazione', __name__)
service_associazione = Service_t_AssociazionePiattiPreparazionie()


@t_associazione_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all():
    piatti = service_associazione.get_all()
    return jsonify(piatti)

@t_associazione_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    piatto = service_associazione.get_by_id(id)
    return jsonify(piatto)

@t_associazione_controller.route('/create', methods=['POST'])
@jwt_required()
def create():
    dati = request.json
    required_fields = ['fkPiatto', 'fkPreparazione', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkPiatto = int(dati['fkPiatto'])
        fkPreparazione = int(dati['fkPreparazione'])
        dataInserimento = dati.get('dataInserimento', datetime.now())
        utenteInserimento = dati['utenteInserimento'].strip()

        return jsonify(service_associazione.create(fkPiatto, fkPreparazione, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_associazione_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    dati = request.json
    required_fields = ['fkPiatto', 'fkPreparazione', 'dataInserimento', 'utenteInserimento']
    
    for field in required_fields:
        if field not in dati or dati[field] is None:
            return jsonify({'Error': f'{field} is required and cannot be None'}), 403
    
    try:
        
        fkPiatto = int(dati['fkPiatto'])
        fkPreparazione = int(dati['fkPreparazione'])
        dataInserimento = dati.get('dataInserimento', datetime.now())
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati.get('dataCancellazione')  # Assumi che sia una stringa già nel formato corretto
        utenteCancellazione = dati.get('utenteCancellazione', '').strip() if dati.get('utenteCancellazione') else None

        return jsonify(service_associazione.update(id, fkPiatto, fkPreparazione,  dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_associazione_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_associazione.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
