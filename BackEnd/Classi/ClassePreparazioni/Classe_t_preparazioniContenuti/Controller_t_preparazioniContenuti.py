from flask import Blueprint, request
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Service_t_preparazioniContenuti import Service_t_tipipreparazionicontenuti

t_tipipreparazionicontenuti_controller = Blueprint('t_tipipreparazionicontenuti', __name__)
service_t_tipipreparazionicontenuti = Service_t_tipipreparazionicontenuti()

@t_tipipreparazionicontenuti_controller.route('/get_all', methods=['GET'])
def get_all_tipi_preparazioni_contenuti():
    return service_t_tipipreparazionicontenuti.get_all_tipi_preparazioni_contenuti()

@t_tipipreparazionicontenuti_controller.route('/<int:id>', methods=['GET'])
def get_tipi_preparazioni_contenuti_by_id(id):
    return service_t_tipipreparazionicontenuti.get_tipi_preparazioni_contenuti_by_id(id)

@t_tipipreparazionicontenuti_controller.route('/create_tipi_preparazioni_contenuti', methods=['POST'])
def create_tipi_preparazioni_contenuti():
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
        
        return service_t_tipipreparazionicontenuti.create_tipi_preparazioni_contenuti(
            fkPreparazione, fkAlimento, quantita, fkTipoQuantita, note, dataInserimento,
            utenteInserimento, dataCancellazione, utenteCancellazione
        )
    except Exception as e:
        return {'Error': str(e)}, 403

@t_tipipreparazionicontenuti_controller.route('/delete_tipi_preparazioni_contenuti/<int:id>', methods=['PUT'])
def delete_tipi_preparazioni_contenuti(id):
    return service_t_tipipreparazionicontenuti.delete_tipi_preparazioni_contenuti(id)
