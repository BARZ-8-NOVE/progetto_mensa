from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_autorizzazioni.Service_t_autorizzazioni import Service_t_autorizzazioni

t_autorizzazioni_controller = Blueprint('autorizzazioni', __name__)
service_t_autorizzazioni = Service_t_autorizzazioni()

@t_autorizzazioni_controller.route('/get_all', methods=['GET'])
def get_autorizzazioni_all():
    autorizzazioni = service_t_autorizzazioni.get_autorizzazioni_all()
    return autorizzazioni

@t_autorizzazioni_controller.route('/get_autorizzazione/<int:id>', methods=['GET'])
def get_autorizzazione_by_id(id):
    autorizzazioni = service_t_autorizzazioni.get_autorizzazioni_by_id(id)
    return autorizzazioni

@t_autorizzazioni_controller.route('/create_autorizzazione', methods=['PUT'])
def create_autorizzazione():
    dati = request.json
    if 'nome' not in dati or 'fkListaFunzionalita' not in dati:
        return {'Error':'wrong keys!'}, 403
    try:
        nome = str(dati['nome'])
        fkListaFunzionalita = str(dati['fkListaFunzionalita'])
        return service_t_autorizzazioni.create_autorizzazione(nome, fkListaFunzionalita)
    except ValueError as ve:
        return {'Error': str(ve)}
    except Exception as e:
        return {'Error': str(e)}, 403
    
@t_autorizzazioni_controller.route('/update_autorizzazione', methods=['POST'])
def update_autorizzazione():
    dati = request.json
    if 'nome' not in dati or 'fkListaFunzionalita' not in dati:
        return {'Error':'wrong keys'}, 403
    try:
        id = int(dati['id'])
        nome = str(dati['nome'])
        fkListaFunzionalita = str(dati['fkListaFunzionalita'])
        return service_t_autorizzazioni.update_autorizzazione(id, nome, fkListaFunzionalita)
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_autorizzazioni_controller.route('/delete_autorizzazione/<int:id>', methods=['DELETE'])
def delete_autorizzazione(id):
    try:
        id = int(id)
        autorizzazione = service_t_autorizzazioni.delete_autorizzazione(id)
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    return autorizzazione
    