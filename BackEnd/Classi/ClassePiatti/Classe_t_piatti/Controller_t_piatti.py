from flask import Blueprint, request, jsonify
from Classi.ClassePiatti.Classe_t_piatti.Service_t_piatti import ServicePiatti

t_piatti_controller = Blueprint('piatti', __name__)
service_piatti = ServicePiatti()

@t_piatti_controller.route('/get_all', methods=['GET'])
def get_all():
    piatti = service_piatti.get_all()
    return jsonify(piatti)

@t_piatti_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    piatto = service_piatti.get_by_id(id)
    return jsonify(piatto)

@t_piatti_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    required_fields = ['fkTipoPiatto', 'fkServizio', 'codice', 'titolo', 'descrizione', 'inMenu', 'ordinatore', 'dataInserimento', 'utenteInserimento', 'dataCancellazione', 'utenteCancellazione']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkTipoPiatto = int(dati['fkTipoPiatto'])
        fkServizio = int(dati['fkServizio'])
        codice = dati['codice'].strip()
        titolo = dati['titolo'].strip()
        descrizione = dati['descrizione'].strip()
        inMenu = bool(dati['inMenu'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati['dataInserimento']  # Assumi che sia una stringa già nel formato corretto
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati['dataCancellazione']  # Assumi che sia una stringa già nel formato corretto
        utenteCancellazione = dati['utenteCancellazione'].strip()

        return jsonify(service_piatti.create(fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_piatti_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    required_fields = ['fkTipoPiatto', 'fkServizio', 'codice', 'titolo', 'descrizione', 'inMenu', 'ordinatore', 'dataInserimento', 'utenteInserimento', 'dataCancellazione', 'utenteCancellazione']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkTipoPiatto = int(dati['fkTipoPiatto'])
        fkServizio = int(dati['fkServizio'])
        codice = dati['codice'].strip()
        titolo = dati['titolo'].strip()
        descrizione = dati['descrizione'].strip()
        inMenu = bool(dati['inMenu'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati['dataInserimento']  # Assumi che sia una stringa già nel formato corretto
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati['dataCancellazione']  # Assumi che sia una stringa già nel formato corretto
        utenteCancellazione = dati['utenteCancellazione'].strip()

        return jsonify(service_piatti.update(id, fkTipoPiatto, fkServizio, codice, titolo, descrizione, inMenu, ordinatore, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_piatti_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_piatti.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
