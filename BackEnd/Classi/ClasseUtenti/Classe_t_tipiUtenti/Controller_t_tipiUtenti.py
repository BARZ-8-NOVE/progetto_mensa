from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Service_t_tipiUtenti import Service_t_tipiUtenti

t_tipiUtenti_controller = Blueprint('tipiUtenti', __name__)
service_t_tipiUtenti = Service_t_tipiUtenti()

@t_tipiUtenti_controller.route('/get_all', methods=['GET'])
def get_tipiUtenti_all():
    tipiUtenti = service_t_tipiUtenti.get_tipiUtenti_all()
    return tipiUtenti

@t_tipiUtenti_controller.route('/get_tipoUtente/<int:id>', methods=['GET'])
def get_tipoUtente_by_id(id):
    tipoUtente = service_t_tipiUtenti.get_tipoUtente_by_id(id)
    return tipoUtente

@t_tipiUtenti_controller.route('/create_tipoUtente', methods=['PUT'])
def create_tipoUtente():
    dati = request.json
    if 'nomeTipoUtente' not in dati or 'fkAutorizzazioni' not in dati:
        return {'Error':'wrong keys!'}, 403
    try:
        nomeTipoUtente = str(dati['nomeTipoUtente'])
        fkAutorizzazioni = dati['fkAutorizzazioni']
        return service_t_tipiUtenti.create_tipoUtente(nomeTipoUtente, fkAutorizzazioni)
    except Exception as e:
        return {'Error': str(e)}, 403
    
@t_tipiUtenti_controller.route('/update_tipoUtente', methods=['POST'])
def update_tipoUtente():
    dati = request.json
    if 'id' not in dati or 'nomeTipoUtente' not in dati or 'fkAutorizzazioni' not in dati:
        return {'Error':'wrong keys'}, 403
    try:
        id = int(dati['id'])
        nomeTipoUtente = str(dati['nomeTipoUtente'])
        fkAutorizzazioni = dati['fkAutorizzazioni']
        return service_t_tipiUtenti.update_tipoUtente(id, nomeTipoUtente, fkAutorizzazioni)
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_tipiUtenti_controller.route('/delete_tipoUtente/<int:id>', methods=['DELETE'])
def delete_tipoUtente(id):
    try:
        id = int(id)
        tipoUtente = service_t_tipiUtenti.delete_tipoUtente(id)
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    return tipoUtente