from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClasseMenu.Classe_t_menuServizi.Service_t_menuServizi import Service_t_MenuServizi

t_menu_servizi_controller = Blueprint('menuservizi', __name__)
service_menu_servizi = Service_t_MenuServizi()

@t_menu_servizi_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all():
    menu_servizi = service_menu_servizi.get_all()
    return jsonify(menu_servizi)

@t_menu_servizi_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    menu_servizio = service_menu_servizi.get_by_id(id)
    return jsonify(menu_servizio)

@t_menu_servizi_controller.route('/create', methods=['POST'])
@jwt_required()
def create():
    dati = request.json
    required_fields = ['fkMenu', 'fkServizio', 'note', 'utenteInserimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkMenu = int(dati['fkMenu'])
        fkServizio = int(dati['fkServizio'])
        note = dati['note']
        utenteInserimento = str(dati['utenteInserimento'])

        return jsonify(service_menu_servizi.create(fkMenu, fkServizio, note,  utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_servizi_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    dati = request.json
    required_fields = [
        'fkMenu', 'fkServizio', 'note', 
        'dataInserimento', 'utenteInserimento'
    ]
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        fkMenu = int(dati['fkMenu'])
        fkServizio = int(dati['fkServizio'])
        note = dati['note']
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])
        return jsonify(service_menu_servizi.update(id, fkMenu, fkServizio, note, dataInserimento, utenteInserimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_menu_servizi_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_menu_servizi.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500