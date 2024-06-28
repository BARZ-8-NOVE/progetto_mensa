from flask import Blueprint, request, jsonify
from Classi.ClasseMenu.Classe_t_menu.Service_t_menu import ServiceMenu

t_menu_controller = Blueprint('menu', __name__)
service_menu = ServiceMenu()

@t_menu_controller.route('/get_all', methods=['GET'])
def get_all():
    menus = service_menu.get_all()
    return jsonify(menus)

@t_menu_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    menu = service_menu.get_by_id(id)
    return jsonify(menu)

@t_menu_controller.route('/create', methods=['POST'])
def create():
    dati = request.json
    required_fields = ['data', 'fkTipoMenu', 'dataInserimento', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        data = dati['data']
        fkTipoMenu = int(dati['fkTipoMenu'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = dati['utenteInserimento'].strip()

        return jsonify(service_menu.create(data, fkTipoMenu, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_controller.route('/update/<int:id>', methods=['PUT'])
def update(id):
    dati = request.json
    required_fields = ['data', 'fkTipoMenu', 'dataInserimento', 'utenteInserimento', 'dataCancellazione', 'utenteCancellazione']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        data = dati['data']
        fkTipoMenu = int(dati['fkTipoMenu'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = dati['utenteInserimento'].strip()
        dataCancellazione = dati.get('dataCancellazione')
        utenteCancellazione = dati.get('utenteCancellazione', '').strip()

        return jsonify(service_menu.update(id, data, fkTipoMenu, dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati:
        return jsonify({'Error': 'utenteCancellazione is required!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_menu.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500