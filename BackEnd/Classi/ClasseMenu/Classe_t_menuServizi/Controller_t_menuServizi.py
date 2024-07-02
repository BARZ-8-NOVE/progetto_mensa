from flask import Blueprint, request, jsonify
from Classi.ClasseMenu.Classe_t_menuServizi.Service_t_menuServizi import ServiceMenuServizi

t_menu_servizi_controller = Blueprint('menuservizi', __name__)
service_menu_servizi = ServiceMenuServizi()

@t_menu_servizi_controller.route('/get_all', methods=['GET'])
def get_all():
    menu_servizi = service_menu_servizi.get_all()
    return jsonify(menu_servizi)

@t_menu_servizi_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    menu_servizio = service_menu_servizi.get_by_id(id)
    return jsonify(menu_servizio)

@t_menu_servizi_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    required_fields = ['fkMenu', 'fkServizio', 'note', 'dataInserimento', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkMenu = int(dati['fkMenu'])
        fkServizio = int(dati['fkServizio'])
        note = dati['note']
        dataInserimento = dati['dataInserimento']
        utenteInserimento = dati['utenteInserimento'].strip()

        return jsonify(service_menu_servizi.create(fkMenu, fkServizio, note, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_servizi_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    required_fields = [
        'fkMenu', 'fkServizio', 'note', 
        'dataInserimento', 'utenteInserimento', 
        'dataCancellazione', 'utenteCancellazione'
    ]
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkMenu = int(dati['fkMenu'])
        fkServizio = int(dati['fkServizio'])
        note = dati['note']
        dataInserimento = dati['dataInserimento']
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati['dataCancellazione']
        utenteCancellazione = dati['utenteCancellazione'].strip()

        return jsonify(service_menu_servizi.update(id, fkMenu, fkServizio, note, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_servizi_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    dati = request.json
    required_fields = ['utenteCancellazione']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_menu_servizi.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
