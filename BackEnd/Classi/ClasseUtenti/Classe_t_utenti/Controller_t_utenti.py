from flask import Blueprint, request
from Classi.ClasseUtenti.Classe_t_utenti.Service_t_utenti import Service_t_utenti

t_utenti_controller = Blueprint('utenti', __name__)
service_t_utenti = Service_t_utenti()

@t_utenti_controller.route('/get_all', methods=['GET'])
def get_tipiUtenti_all():
    utenti = service_t_utenti.get_utenti_all()
    return utenti

@t_utenti_controller.route('/get_utente/<int:id>', methods=['GET'])
def get_tipoUtente_by_id(id):
    utente = service_t_utenti.get_utente_by_id(id)
    return utente

@t_utenti_controller.route('/create_utente', methods=['PUT'])
def create_utente():
    dati = request.json
    required_fields = ['username', 'nome', 'cognome', 'fkTipoUtente', 'fkFunzCustom', 'reparti', 'email', 'password']
    if not all(field in dati for field in required_fields):
        return {'Error':'wrong keys!'}, 403
    try:
        username = str(dati['username'])
        nome = str(dati['nome'])
        cognome = str(dati['cognome'])
        fkTipoUtente = int(dati['fkTipoUtente'])
        fkFunzCustom = str(dati['fkFunzCustom'])
        reparti = str(dati['reparti'])
        email = str(dati['email'])
        password = str(dati['password'])
        return service_t_utenti.create_utente(username, nome, cognome, fkTipoUtente, fkFunzCustom, reparti, email, password)
    except Exception as e:
        return {'Error': str(e)}, 403
    
@t_utenti_controller.route('/update_utente', methods=['POST'])
def update_utente():
    dati = request.json
    required_fields = ['id', 'username', 'nome', 'cognome', 'fkTipoUtente', 'fkFunzCustom', 'reparti', 'attivo', 'email', 'password']
    if not all(field in dati for field in required_fields):
        return {'Error':'wrong keys!'}, 403
    try:
        id = int(dati['id'])
        username = str(dati['username'])
        nome = str(dati['nome'])
        cognome = str(dati['cognome'])
        fkTipoUtente = int(dati['fkTipoUtente'])
        fkFunzCustom = str(dati['fkFunzCustom'])
        reparti = str(dati['reparti'])
        attivo = int(dati['attivo'])
        email = str(dati['email'])
        password = str(dati['password'])
        return service_t_utenti.update_utente(id, username, nome, cognome, fkTipoUtente, fkFunzCustom, reparti, attivo, email, password)
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    
@t_utenti_controller.route('/delete_utente/<int:id>', methods=['DELETE'])
def delete_utente(id):
    try:
        id = int(id)
        result = service_t_utenti.delete_utente(id)
    except ValueError as ve:
        return {'Error': str(ve)}, 403
    except Exception as e:
        return {'Error': str(e)}, 400
    return result