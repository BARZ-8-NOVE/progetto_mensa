from flask import Blueprint, request
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Service_t_preparazioniContenuti import Service_t_preparazionicontenuti

t_preparazionicontenuti_controller = Blueprint('preparazionicontenuti', __name__)
service_t_preparazionicontenuti = Service_t_preparazionicontenuti()

@t_preparazionicontenuti_controller.route('/get_all', methods=['GET'])
def get_all_preparazioni_contenuti():
    return service_t_preparazionicontenuti.get_all_preparazioni_contenuti()

@t_preparazionicontenuti_controller.route('/<int:id>', methods=['GET'])
def get_preparazioni_contenuti_by_id(id):
    return service_t_preparazionicontenuti.get_preparazioni_contenuti_by_id(id)

@t_preparazionicontenuti_controller.route('/create', methods=['POST'])
def create_preparazioni_contenuti():
    dati = request.json
    if 'fkPreparazione' not in dati or 'fkAlimento' not in dati or 'quantita' not in dati or 'fkTipoQuantita' not in dati:
        return {'Error': 'wrong keys!'}, 403
    try:
        fkPreparazione = int(dati['fkPreparazione'])
        fkAlimento = int(dati['fkAlimento'])
        quantita = float(dati['quantita'])
        fkTipoQuantita = int(dati['fkTipoQuantita'])
        note = dati.get('note')
        dataInserimento = dati.get('dataInserimento')
        utenteInserimento = dati.get('utenteInserimento')
        dataCancellazione = dati.get('dataCancellazione')
        utenteCancellazione = dati.get('utenteCancellazione')
        
        return service_t_preparazionicontenuti.create_preparazioni_contenuti(
            fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note, dataInserimento,
            utenteInserimento, dataCancellazione, utenteCancellazione
        )
    except Exception as e:
        return {'Error': str(e)}, 403
    
@t_preparazionicontenuti_controller.route('/update/<int:id>', methods=['PUT'])
def update_preparazioni_contenuti(id):
    dati = request.json
    if 'fkPreparazione' not in dati or 'fkAlimento' not in dati or 'quantita' not in dati or 'fkTipoQuantita' not in dati:
        return {'Error': 'wrong keys!'}, 403
    
    try:
        fkPreparazione = int(dati['fkPreparazione'])
        fkAlimento = int(dati['fkAlimento'])
        quantita = float(dati['quantita'])
        fkTipoQuantita = int(dati['fkTipoQuantita'])
        note = dati.get('note')
        dataInserimento = dati.get('dataInserimento')
        utenteInserimento = dati.get('utenteInserimento')
        dataCancellazione = dati.get('dataCancellazione')
        utenteCancellazione = dati.get('utenteCancellazione')
        
        # Chiamare il metodo per l'aggiornamento nel servizio
        return service_t_preparazionicontenuti.update_preparazioni_contenuti(
            id, fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note, dataInserimento,
            utenteInserimento, dataCancellazione, utenteCancellazione
        )
    except Exception as e:
        return {'Error': str(e)}, 403


@t_preparazionicontenuti_controller.route('/delete/<int:id>', methods=['PUT'])
def delete_preparazioni_contenuti(id):
    return service_t_preparazionicontenuti.delete_preparazioni_contenuti(id)
