from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClasseMenu.Classe_t_tipiMenu.Service_t_tipiMenu import ServiceTipiMenu

t_tipimenu_controller = Blueprint('tipimenu', __name__)
service_t_tipimenu = ServiceTipiMenu()

@t_tipimenu_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_tipi_menu_all():
    try:
        result = service_t_tipimenu.get_all()
        return jsonify(result)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_tipimenu_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_tipi_menu_by_id(id):
    try:
        result = service_t_tipimenu.get_by_id(id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@t_tipimenu_controller.route('/create', methods=['POST'])
@jwt_required()
def create_tipi_menu():
    dati = request.json
    required_keys = ['descrizione', 'color', 'backgroundColor', 'ordinatore', 'dataInserimento', 'utenteInserimento']
    if not all(key in dati for key in required_keys):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        descrizione = str(dati['descrizione'])
        color = str(dati['color'])
        backgroundColor = str(dati['backgroundColor'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])
        result = service_t_tipimenu.create(descrizione, color, backgroundColor, ordinatore, dataInserimento, utenteInserimento)
        return jsonify(result)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_tipimenu_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_tipi_menu(id):
    dati = request.json
    required_keys = ['descrizione', 'color', 'backgroundColor', 'ordinatore', 'dataInserimento', 'utenteInserimento']
    if not all(key in dati for key in required_keys):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        descrizione = str(dati['descrizione'])
        color = str(dati['color'])
        backgroundColor = str(dati['backgroundColor'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])
        result = service_t_tipimenu.update(id, descrizione, color, backgroundColor, ordinatore, dataInserimento, utenteInserimento)
        return jsonify(result)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_tipimenu_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    dati = request.json
    if 'utenteCancellazione' not in dati or dati['utenteCancellazione'] is None:
        return jsonify({'Error': 'utenteCancellazione key missing!'}), 403
    try:
        utenteCancellazione = dati['utenteCancellazione'].strip()
        return jsonify(service_t_tipimenu.delete(id, utenteCancellazione))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500