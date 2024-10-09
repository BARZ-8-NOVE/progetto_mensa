from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseOrdini.Classe_t_orariOrdini.Domain_t_orariOrdini import TOrariOrdini
from datetime import datetime, timedelta

class RepositoryOrariOrdini:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all(self):
        try:
            results = self.session.query(TOrariOrdini).all()
            return [{'id': result.id, 
                    'nomeOrdine': result.nomeOrdine,
                    'fkServizio': result.fkServizio,
                    'tempoLimite': result.tempoLimite,
                    'ordineDipendente': result.ordineDipendente,
                    'ordinePerOggi': result.ordinePerOggi,
                    'ultimoUpdated': result.ultimoUpdated,
                    'utenteModifica': result.utenteModifica
                     
                     } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Assicurati che la sessione venga chiusa per evitare perdite di risorse
            self.session.close()


    def get_by_id(self, id):
        try:
            result = self.session.query(TOrariOrdini).filter_by(id=id).first()
            if result:
                return {'nomeOrdine': result.nomeOrdine,
                        'fkServizio': result.fkServizio,
                        'tempoLimite': result.tempoLimite,
                        'ordineDipendente': result.ordineDipendente,
                        'ordinePerOggi': result.ordinePerOggi,
                        'ultimoUpdated': result.ultimoUpdated,
                        'utenteModifica': result.utenteModifica}
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            self.session.close()


    def update(self, id, nomeOrdine, fkServizio, tempoLimite, ordineDipendente, ordinePerOggi, utenteModifica):
        try:
            orario_ordine = self.session.query(TOrariOrdini).filter_by(id=id).first()
            if orario_ordine:
                orario_ordine.nomeOrdine = nomeOrdine
                orario_ordine.fkServizio = fkServizio
                orario_ordine.tempoLimite = tempoLimite
                orario_ordine.ordineDipendente = ordineDipendente
                orario_ordine.ordinePerOggi = ordinePerOggi
                orario_ordine.utenteModifica = utenteModifica
                self.session.commit()
                return {'ordine_piatto': 'updated!'}, 200
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            self.session.close()


    def check_order_time_limit(self, servizio, tipo_commensale, order_date):
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        tomorrow = current_date + timedelta(days=1)

        try:
            time_limit_record = self.session.query(TOrariOrdini).filter(
                TOrariOrdini.fkServizio == servizio,
                TOrariOrdini.ordineDipendente == tipo_commensale
            ).first()

            if not time_limit_record:
                return {'Error': 'Limite di tempo non definito per questo servizio'}, 400

            time_limit = time_limit_record.tempoLimite
            ordine_per_oggi = time_limit_record.ordinePerOggi

            # Controllo se l'ordine è per il passato
            if order_date < current_date:
                return {'Error': 'Non è possibile effettuare ordini per date passate'}, 400

            # Controllo se l'ordine è per oggi
            if order_date == current_date:
                if ordine_per_oggi == True:
                    if current_time <= time_limit:
                        return {'status': 'Ordine consentito per oggi'}, 200
                    else:
                        return {'Error': 'Tempo per l\'ordine superato per oggi'}, 400
                else:
                    return {'Error': 'Non è permesso effettuare ordini per oggi'}, 400

            # Controllo se l'ordine è per domani
            if order_date == tomorrow:
                if ordine_per_oggi == False:
                    if current_time <= time_limit:
                        return {'status': 'Ordine consentito per domani'}, 200
                    else:
                        return {'Error': 'Tempo per l\'ordine superato per domani'}, 400
                else:
                    return {'status': 'Ordine consentito per oggi'}, 200

            # Controllo per giorni futuri
            if order_date > tomorrow:
                return {'status': 'Ordine consentito per giorni futuri'}, 200

            return {'Error': 'Data dell\'ordine non valida'}, 400

        except Exception as e:
            self.session.rollback()
            return {'Error': f'Errore nel controllo dell\'ordine: {str(e)}'}, 500
        finally:
            self.session.close()
