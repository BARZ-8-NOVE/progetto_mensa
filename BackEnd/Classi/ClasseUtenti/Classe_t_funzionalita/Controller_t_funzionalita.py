from flask import Blueprint, request
from Classi.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita

t_funzionalita_controller = Blueprint('funzionalita', __name__)
service_t_funzionalita = Service_t_funzionalita()

@t_funzionalita_controller.route('/get_all', methods=['GET'])
def get_funzionalita_all():
    funzionalita = service_t_funzionalita.get_funzionalita_all()
    return funzionalita

@t_funzionalita_controller.route('/get_funzionalita/<int:id>', methods=['GET'])
def get_funzionalita_by_id(id):
    funzionalita = service_t_funzionalita.get_funzionalita_by_id(id)
    return funzionalita

@t_funzionalita_controller.route('/create_funzionalita', methods=['PUT'])
def create_funzionalita():
    dati = request.json
    if 'nome' not in dati or 'frmNome' not in dati:
        return {'Error':'wrong keys!'}, 403
    try:
        nome = str(dati['nome'])
        frmNome = str(dati['frmNome'])
        return service_t_funzionalita.create_funzionalita(nome, frmNome)
    except Exception as e:
        return {'Error': str(e)}, 403
    
@t_funzionalita_controller.route('/update_funzionalita', methods=['POST'])
def update_funzionalita():
    dati = request.json
    if 'nome' not in dati or 'frmNome' not in dati:
        return {'Error':'wrong keys'}, 403
    try:
        id = int(dati['id'])
        nome = str(dati['nome'])
        frmNome = str(dati['frmNome'])
        return service_t_funzionalita.update_funzionalita(id, nome, frmNome)
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_funzionalita_controller.route('/delete_funzionalita/<int:id>', methods=['DELETE'])
def delete_funzionalita(id):
    id = int(id)
    funzionalita = service_t_funzionalita.delete_funzionalita(id)
    return funzionalita
    