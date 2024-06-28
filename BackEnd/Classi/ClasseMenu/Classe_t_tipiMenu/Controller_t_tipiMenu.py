from flask import Blueprint, request
from Classi.ClasseMenu.Classe_t_tipiMenu.Service_t_tipiMenu import ServiceTipiMenu

t_tipimenu_controller = Blueprint('tipimenu', __name__)
service_t_tipimenu = ServiceTipiMenu()

@t_tipimenu_controller.route('/get_all', methods=['GET'])
def get_tipi_menu_all():
    return service_t_tipimenu.get_tipi_menu_all()

@t_tipimenu_controller.route('/<int:id>', methods=['GET'])
def get_tipi_menu_by_id(id):
    return service_t_tipimenu.get_tipi_menu_by_id(id)

@t_tipimenu_controller.route('/create_tipi_menu', methods=['POST'])
def create_tipi_menu():
    dati = request.json
    if 'descrizione' not in dati or 'color' not in dati or 'backgroundColor' not in dati or 'ordinatore' not in dati or 'dataInserimento' not in dati or 'utenteInserimento' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        descrizione = str(dati['descrizione'])
        color = str(dati['color'])
        backgroundColor = str(dati['backgroundColor'])
        ordinatore = int(dati['ordinatore'])
        dataInserimento = dati['dataInserimento']
        utenteInserimento = str(dati['utenteInserimento'])
        return service_t_tipimenu.create_tipi_menu(descrizione, color, backgroundColor, ordinatore, dataInserimento, utenteInserimento)
    except Exception as e:
        return {'Error': str(e)}, 403

@t_tipimenu_controller.route('/delete_tipi_menu/<int:id>', methods=['PATCH'])
def delete_tipi_menu(id):
    dati = request.json
    if 'dataCancellazione' not in dati or 'utenteCancellazione' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        dataCancellazione = dati['dataCancellazione']
        utenteCancellazione = str(dati['utenteCancellazione'])
        return service_t_tipimenu.delete_tipi_menu(id, dataCancellazione, utenteCancellazione)
    except Exception as e:
        return {'Error': str(e)}, 403
