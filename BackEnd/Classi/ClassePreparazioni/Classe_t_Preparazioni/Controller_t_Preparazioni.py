from flask import Blueprint, request
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Service_t_Preparazioni import Service_t_preparazioni

t_preparazioni_controller = Blueprint('t_preparazioni', __name__)
service_t_preparazioni = Service_t_preparazioni()

@t_preparazioni_controller.route('/get_all', methods=['GET'])
def get_all_preparazioni():
    return service_t_preparazioni.get_all_preparazioni()

@t_preparazioni_controller.route('/<int:id>', methods=['GET'])
def get_preparazione_by_id(id):
    return service_t_preparazioni.get_preparazione_by_id(id)

@t_preparazioni_controller.route('/create_preparazione', methods=['POST'])
def create_preparazione():
    dati = request.json
    if 'fkTipoPreparazione' not in dati or 'descrizione' not in dati or 'isEstivo' not in dati or 'isInvernale' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        fkTipoPreparazione = int(dati['fkTipoPreparazione'])
        descrizione = dati['descrizione']
        isEstivo = bool(dati['isEstivo'])
        isInvernale = bool(dati['isInvernale'])
        allergeni = dati.get('allergeni')
        inizio = dati.get('inizio')
        fine = dati.get('fine')
        dataInserimento = dati.get('dataInserimento')
        utenteInserimento = dati.get('utenteInserimento')
        dataCancellazione = dati.get('dataCancellazione')
        utenteCancellazione = dati.get('utenteCancellazione')
        immagine = dati.get('immagine')
        
        return service_t_preparazioni.create_preparazione(
            fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni, inizio, fine,
            dataInserimento, utenteInserimento, dataCancellazione, utenteCancellazione, immagine
        )
    except Exception as e:
        return {'Error': str(e)}, 403

@t_preparazioni_controller.route('/delete_preparazione/<int:id>', methods=['PUT'])
def delete_preparazione(id):
    return service_t_preparazioni.delete_preparazione(id)
