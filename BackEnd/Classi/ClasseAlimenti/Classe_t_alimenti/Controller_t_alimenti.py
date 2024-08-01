from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Classi.ClasseAlimenti.Classe_t_alimenti.Service_t_alimenti import Service_t_Alimenti
from werkzeug.exceptions import NotFound
from Classi.ClasseUtility.UtilityGeneral.UtilityHttpCodes import HttpCodes
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

t_alimenti_controller = Blueprint('alimenti', __name__)
service_alimenti = Service_t_Alimenti()
httpCodes = HttpCodes()

@t_alimenti_controller.route('/get_all', methods=['GET'])
@jwt_required()
def get_all():
    alimenti = service_alimenti.get_all()
    return jsonify(alimenti)

@t_alimenti_controller.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    alimento = service_alimenti.get_by_id(id)
    return jsonify(alimento)

@t_alimenti_controller.route('/create', methods=['POST'])
@jwt_required()
def create():
    dati = request.json
    required_fields = ['alimento', 'energia_Kcal', 'energia_KJ', 'prot_tot_gr', 'glucidi_tot', 'lipidi_tot', 'saturi_tot', 'fkAllergene', 'fkTipologiaAlimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        alimento = dati['alimento'].strip()
        energia_Kcal = float(dati['energia_Kcal'])
        energia_KJ = float(dati['energia_KJ'])
        prot_tot_gr = float(dati['prot_tot_gr'])
        glucidi_tot = float(dati['glucidi_tot'])
        lipidi_tot = float(dati['lipidi_tot'])
        saturi_tot = float(dati['saturi_tot'])
        fkAllergene = dati['fkAllergene'].strip()
        fkTipologiaAlimento = int(dati['fkTipologiaAlimento'])

        return jsonify(service_alimenti.create(alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_alimenti_controller.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    dati = request.json
    required_fields = ['alimento', 'energia_Kcal', 'energia_KJ', 'prot_tot_gr', 'glucidi_tot', 'lipidi_tot', 'saturi_tot', 'fkAllergene', 'fkTipologiaAlimento']
    if not all(field in dati for field in required_fields):
        return jsonify({'Error': 'wrong keys!'}), 403
    try:
        alimento = dati['alimento'].strip()
        energia_Kcal = float(dati['energia_Kcal'])
        energia_KJ = float(dati['energia_KJ'])
        prot_tot_gr = float(dati['prot_tot_gr'])
        glucidi_tot = float(dati['glucidi_tot'])
        lipidi_tot = float(dati['lipidi_tot'])
        saturi_tot = float(dati['saturi_tot'])
        fkAllergene = dati['fkAllergene'].strip()
        fkTipologiaAlimento = int(dati['fkTipologiaAlimento'])


        return jsonify(service_alimenti.update(id, alimento, energia_Kcal, energia_KJ, prot_tot_gr, glucidi_tot, lipidi_tot, saturi_tot, fkAllergene, fkTipologiaAlimento))

    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 403
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@t_alimenti_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    return jsonify(service_alimenti.delete(id))

@t_alimenti_controller.route('/get_alimenti_by_name/<string:name>', methods=['GET'])
@jwt_required()
def get_alimento_by_name(name):
    try:
        results = service_alimenti.get_alimento_by_name(name)
        return jsonify(UtilityGeneral.getClassDictionaryOrList(results)), httpCodes.OK
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR
    
@t_alimenti_controller.route('/get_alimenti_by_tipologia_alimento/<int:tipologia>', methods=['GET'])
@jwt_required()
def get_alimenti_by_tipologia_alimento(tipologia):
    try:
        results = service_alimenti.get_alimenti_by_tipologia_alimento(tipologia)
        return jsonify(UtilityGeneral.getClassDictionaryOrList(results)), httpCodes.OK
    except NotFound as e:
        return jsonify({'Error': str(e)}), httpCodes.NOT_FOUND
    except Exception as e:
        return jsonify({'Error': str(e)}), httpCodes.INTERNAL_SERVER_ERROR