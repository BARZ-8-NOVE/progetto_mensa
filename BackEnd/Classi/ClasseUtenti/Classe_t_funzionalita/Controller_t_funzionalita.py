from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_funzionalita.Service_t_funzionalita import Service_t_funzionalita

t_funzionalita_controller = Blueprint('funzionalita', __name__)
service_t_funzionalita = Service_t_funzionalita()

@t_funzionalita_controller.route('/get_all', methods=['GET'])
def get_funzionalita_all():
    funzionalita = service_t_funzionalita.get_funzionalita_all()
    return funzionalita

@t_funzionalita_controller.route('/<int:id>', methods=['GET'])
def get_funzionalita_by_id(id):
    funzionalita = service_t_funzionalita.get_funzionalita_by_id(id)
    return funzionalita

@t_funzionalita_controller.route('/create_funzionalita', methods=['PUT'])
def create_funzionalita():
    dati = request.json
    if 'id' not in dati or 'nome' not in dati or 'frmNome' not in dati:
        return {'Error':'wrong keys!'}, 403
    try:
        id = int(dati['id'])
        if(id == 0) or (id < 0):
            raise Exception("id cannot be equal or less than 0") 
        nome = str(dati['nome'])
        if(nome.strip() == "") or (nome is None) or (len(nome.strip()) > 50):
            raise Exception("nome cannot be None or more than 50 characters!")
        frmNome = str(dati['frmNome'])
        if(frmNome.strip() == "") or (frmNome is None) or (len(frmNome.strip()) > 50):
            raise Exception("nome cannot be None or more than 50 characters!")
        return service_t_funzionalita.create_funzionalita(id, nome, frmNome)
    except Exception as e:
        return {'Error': str(e)}, 403
    
    