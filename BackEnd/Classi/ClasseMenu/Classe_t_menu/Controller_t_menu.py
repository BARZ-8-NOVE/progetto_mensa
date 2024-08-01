from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClasseMenu.Classe_t_menu.Service_t_menu import Service_t_Menu

t_menu_controller = Blueprint('menu', __name__)
service_menu = Service_t_Menu()

@t_menu_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all():
    menus = service_menu.get_all()
    return jsonify(menus)

@t_menu_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    menu = service_menu.get_by_id(id)
    return jsonify(menu)

@t_menu_controller.route('/create', methods=['POST'])
@jwt_required()
def create():
    dati = request.json
    required_fields = ['data', 'fkTipoMenu', 'dataInserimento', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        data = dati['data']
        fkTipoMenu = int(dati['fkTipoMenu'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])

        return jsonify(service_menu.create(data, fkTipoMenu, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    dati = request.json
    required_fields = ['data', 'fkTipoMenu', 'dataInserimento', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        data = dati['data']
        fkTipoMenu = int(dati['fkTipoMenu'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])

        return jsonify(service_menu.update(id, data, fkTipoMenu, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_menu .delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500