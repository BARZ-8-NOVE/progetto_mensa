from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from .Service_t_tipologiaalimenti import Service_t_tipologiaalimenti

t_tipologiaalimenti_controller = Blueprint('tipologiaalimenti', __name__)
service_t_tipologiaalimenti = Service_t_tipologiaalimenti()

@t_tipologiaalimenti_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_tipologiaalimenti():
    return service_t_tipologiaalimenti.get_all_tipologiaalimenti()

@t_tipologiaalimenti_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_tipologiaalimenti_by_id(id):
    return service_t_tipologiaalimenti.get_tipologiaalimenti_by_id(id)

@t_tipologiaalimenti_controller.route('/create', methods=['POST'])
@jwt_required()
def create_tipologiaalimenti():
    dati = request.json
    if 'nome' not in dati or 'fktipologiaConservazione' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        nome = dati['nome']
        fktipologiaConservazione = dati['fktipologiaConservazione']
        return service_t_tipologiaalimenti.create_tipologiaalimenti(nome, fktipologiaConservazione)
    except Exception as e:
        return {'Error': str(e)}, 403

@t_tipologiaalimenti_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tipologiaalimenti(id):
    return service_t_tipologiaalimenti.delete_tipologiaalimenti(id)
