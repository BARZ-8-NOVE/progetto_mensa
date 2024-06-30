from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Service_t_tipiUtenti import Service_t_tipiUtenti
from Classi.ClasseUtility.UtilityGeneral.UtilityGeneral import UtilityGeneral

t_tipiUtenti_controller = Blueprint('tipiUtenti', __name__)
service_t_tipiUtenti = Service_t_tipiUtenti()

@t_tipiUtenti_controller.route('/get_all', methods=['GET'])
def get_tipiUtenti_all():
    try:
        tipiUtenti = service_t_tipiUtenti.get_tipiUtenti_all()
        return tipiUtenti
    except Exception as e:
        return {'Error': str(e)}, 400

@t_tipiUtenti_controller.route('/get_tipoUtente/<int:id>', methods=['GET'])
def get_tipoUtente_by_id(id):
    tipoUtente = service_t_tipiUtenti.get_tipoUtente_by_id(id)
    return tipoUtente

@t_tipiUtenti_controller.route('/create_tipoUtente', methods=['PUT'])
def create_tipoUtente():
    try:
        dati = request.json
        required_fields = ['nomeTipoUtente', 'fkAutorizzazioni']
        UtilityGeneral.check_fields(dati, required_fields)
        nomeTipoUtente = dati['nomeTipoUtente']
        fkAutorizzazioni = dati['fkAutorizzazioni']
        return service_t_tipiUtenti.create_tipoUtente(nomeTipoUtente, fkAutorizzazioni)
    except KeyError as e:
        return {'Error': str(e)}, 405
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, 422
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_tipiUtenti_controller.route('/update_tipoUtente', methods=['POST'])
def update_tipoUtente():
    try:
        dati = request.json
        required_fields = ['id', 'nomeTipoUtente', 'fkAutorizzazioni']
        UtilityGeneral.check_fields(dati, required_fields)
        id = UtilityGeneral.safe_int_convertion(dati['id'], 'id')
        nomeTipoUtente = dati['nomeTipoUtente']
        fkAutorizzazioni = dati['fkAutorizzazioni']
        return service_t_tipiUtenti.update_tipoUtente(id, nomeTipoUtente, fkAutorizzazioni)
    except KeyError as e:
        return {'Error': str(e)}, 405
    except (ValueError, TypeError) as e:
        return {'Error': str(e)}, 422
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_tipiUtenti_controller.route('/delete_tipoUtente/<int:id>', methods=['DELETE'])
def delete_tipoUtente(id):
    try:
        id = UtilityGeneral.safe_int_convertion(id, 'id')
        tipoUtente = service_t_tipiUtenti.delete_tipoUtente(id)
        return tipoUtente
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    