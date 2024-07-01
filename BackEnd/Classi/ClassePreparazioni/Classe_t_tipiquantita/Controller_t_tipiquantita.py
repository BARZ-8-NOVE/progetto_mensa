from flask import Blueprint, request
from Classi.ClassePreparazioni.Classe_t_tipiquantita.Service_t_tipiquantita import Service_t_tipoquantita

t_tipoquantita_controller = Blueprint('tipoquantita', __name__)
service_t_tipoquantita = Service_t_tipoquantita()

@t_tipoquantita_controller.route('/get_all', methods=['GET'])
def get_all_tipoquantita():
    return service_t_tipoquantita.get_all_tipoquantita()

@t_tipoquantita_controller.route('/<int:id>', methods=['GET'])
def get_tipoquantita_by_id(id):
    return service_t_tipoquantita.get_tipoquantita_by_id(id)

@t_tipoquantita_controller.route('/create', methods=['POST'])
def create_tipoquantita():
    dati = request.json
    if 'tipo' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        tipo = dati['tipo']
        peso_valore_in_grammi = dati.get('peso_valore_in_grammi')
        peso_valore_in_Kg = dati.get('peso_valore_in_Kg')
        return service_t_tipoquantita.create_tipoquantita(tipo, peso_valore_in_grammi, peso_valore_in_Kg)
    except Exception as e:
        return {'Error': str(e)}, 403

@t_tipoquantita_controller.route('/update/<int:id>', methods=['PUT'])
def update_tipoquantita(id):
    dati = request.json
    tipo = dati.get('tipo')
    peso_valore_in_grammi = dati.get('peso_valore_in_grammi')
    peso_valore_in_Kg = dati.get('peso_valore_in_Kg')
    return service_t_tipoquantita.update_tipoquantita(id, tipo, peso_valore_in_grammi, peso_valore_in_Kg)

@t_tipoquantita_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_tipoquantita(id):
    return service_t_tipoquantita.delete_tipoquantita(id)
