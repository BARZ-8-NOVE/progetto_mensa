from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.ClassePreparazioni.Classe_t_Preparazioni.Domain_t_preparazioni import TPreparazioni
from Classi.ClassePreparazioni.Classe_t_preparazioniContenuti.Repository_t_preparazioniContenuti import TPreparazioniContenuti
from Classi.ClasseAlimenti.Classe_t_alimenti.Repository_t_alimenti import TAlimenti
from datetime import datetime
from sqlalchemy import func, case
from collections import defaultdict

class Repository_t_preparazioni:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_preparazioni(self):
        try:
            results = self.session.query(TPreparazioni).filter(TPreparazioni.dataCancellazione.is_(None)).all()
            return [{
                'id': result.id,
                'fkTipoPreparazione': result.fkTipoPreparazione,
                'descrizione': result.descrizione,
                'isEstivo': result.isEstivo,
                'isInvernale': result.isInvernale,
                'allergeni': result.allergeni,
                'inizio': result.inizio,
                'fine': result.fine,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione,
                'immagine': result.immagine
            } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close
                        

    def get_all_preparazioni_base(self):
        try:
            results = self.session.query(TPreparazioni).filter(
                TPreparazioni.fkTipoPreparazione == 1,
                TPreparazioni.dataCancellazione.is_(None)
            ).all()
            return [{
                'id': result.id,
                'fkTipoPreparazione': result.fkTipoPreparazione,
                'descrizione': result.descrizione,
                'isEstivo': result.isEstivo,
                'isInvernale': result.isInvernale,
                'allergeni': result.allergeni,
                'inizio': result.inizio,
                'fine': result.fine,
                'dataInserimento': result.dataInserimento,
                'utenteInserimento': result.utenteInserimento,
                'dataCancellazione': result.dataCancellazione,
                'utenteCancellazione': result.utenteCancellazione,
                'immagine': result.immagine
            } for result in results]
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close


    def  get_descrizione_by_id(self, id):
        try:
            result = self.session.query(TPreparazioni).filter_by(id=id).first()
            if result:
                return result.descrizione

            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            if self.session:
                self.session.close

                
    def update(self, id, fkTipoPreparazione, descrizione, isEstivo, isInvernale, inizio, fine, immagine):
        try:
            preparazione = self.session.query(TPreparazioni).filter_by(id=id).first()
            if preparazione:
                preparazione.fkTipoPreparazione = fkTipoPreparazione
                preparazione.descrizione = descrizione
                preparazione.isEstivo = isEstivo
                preparazione.isInvernale = isInvernale
                preparazione.inizio = inizio
                preparazione.fine = fine
                preparazione.immagine = immagine
                self.session.commit()
                return {'preparazione': 'updated!', 'id': id}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()



    def get_preparazione_by_id(self, id):
        try:
            result = self.session.query(TPreparazioni).filter_by(id=id).first()
            if result:
                return {
                    'id': result.id,
                    'fkTipoPreparazione': result.fkTipoPreparazione,
                    'descrizione': result.descrizione,
                    'isEstivo': result.isEstivo,
                    'isInvernale': result.isInvernale,
                    'allergeni': result.allergeni,
                    'inizio': result.inizio,
                    'fine': result.fine,
                    'dataInserimento': result.dataInserimento,
                    'utenteInserimento': result.utenteInserimento,
                    'dataCancellazione': result.dataCancellazione,
                    'utenteCancellazione': result.utenteCancellazione,
                    'immagine': result.immagine
                }
            else:
                return {'Error': f'No match found for this id: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 400
        finally:
            # Chiudi sempre la sessione
            self.session.close()

    def create_preparazione(self, fkTipoPreparazione, descrizione, isEstivo, isInvernale, allergeni=None, inizio=None, fine=None, dataInserimento=None, utenteInserimento=None, dataCancellazione=None, utenteCancellazione=None, immagine=None):
        try:
            preparazione = TPreparazioni(
                fkTipoPreparazione=fkTipoPreparazione,
                descrizione=descrizione,
                isEstivo=isEstivo,
                isInvernale=isInvernale,
                allergeni=allergeni,
                inizio=inizio,
                fine=fine,
                dataInserimento=dataInserimento,
                utenteInserimento=utenteInserimento,
                dataCancellazione=dataCancellazione,
                utenteCancellazione=utenteCancellazione,
                immagine=immagine
            )
            self.session.add(preparazione)
            self.session.commit()
            return preparazione.id
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close()


    def get_last_id(self):
            try:
                # Fetch the last record by ordering by the primary key in descending order
                result = self.session.query(TPreparazioni).filter(TPreparazioni.dataCancellazione.is_(None)).order_by(TPreparazioni.id.desc()).first()
                
                if result:
                    return {'id': result.id}
                else:
                    return {'Error': 'No match found'}, 404
            except Exception as e:
                self.session.rollback()
                return {'Error': str(e)}, 400
            finally:
                # Chiudi sempre la sessione
                self.session.close()


    def recupera_ingredienti_base(self, id, quantita_richesta):
        try:
            base_id = id - 100000  # Rimuoviamo l'offset per ottenere l'ID della preparazione base
            # Recupera gli ingredienti della preparazione base
            preparazione_base_ingredienti = (
                self.session.query(
                    TPreparazioniContenuti.fkAlimento,
                    TPreparazioniContenuti.quantita
                )
                .filter(
                    TPreparazioniContenuti.dataCancellazione == None,
                    TPreparazioniContenuti.fkPreparazione == base_id,
                )
                .all()
            )

            ingredienti = {}  # Dizionario per contenere id alimento come chiave e (quantità, allergeni) come valore

            # Calcola la quantità totale della preparazione base
            quantita_totale_preparazione_base = sum(ingredient.quantita for ingredient in preparazione_base_ingredienti)

            for ingredient in preparazione_base_ingredienti:
                # Calcola la quantità in base alla quantità richiesta
                quantita_calcolata = (ingredient.quantita / quantita_totale_preparazione_base) * quantita_richesta
                
                # Aggiungi l'ingrediente al dizionario
                ingredienti[ingredient.fkAlimento] = {'quantita': quantita_calcolata, 'allergeni': []}

            return ingredienti  # Restituisci il dizionario degli ingredienti

        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            return {}  # In caso di errore, restituisci un dizionario vuoto

        finally:
            self.session.close()

    def processa_ingredienti(self, fk_alimento, quantita_richesta, risultati):
        """Processa ingredienti composti e semplici."""
        # Creiamo una lista per gestire ingredienti composti da elaborare
        stack = [(fk_alimento, quantita_richesta)]

        while stack:
            current_fk_alimento, current_quantita = stack.pop()

            # Controlla se current_fk_alimento è None
            if current_fk_alimento is None:
                print(f"Attenzione: fk_alimento è None per quantità richiesta: {current_quantita}")
                continue

            if current_fk_alimento > 100000:  # Ingredienti composti
                sottoingredienti = self.recupera_ingredienti_base(current_fk_alimento, current_quantita)
                for key, value in sottoingredienti.items():
                    # Aggiungi alla lista di ingredienti da processare
                    stack.append((key, value['quantita']))
            else:  # Ingredienti semplici
                risultati[current_fk_alimento]['quantita'] += current_quantita


    def recupero_totale_peso_ingredienti(self, descrizione):
        try:
            # Recupera la preparazione in base alla descrizione fornita
            preparazione = self.session.query(TPreparazioni).filter_by(descrizione=descrizione).first()
            if not preparazione:
                return {'Error': 'Nessuna preparazione trovata con questa descrizione.'}, 404

            # Recupera gli ingredienti di base associati alla preparazione
            ingredienti_base = self.session.query(TPreparazioniContenuti).filter_by(
                fkPreparazione=preparazione.id, 
                dataCancellazione=None).all()
            
            # Inizializza il dizionario per i risultati
            risultati = defaultdict(lambda: {'quantita': 0})

            # Itera su ogni ingrediente di base
            for ingrediente in ingredienti_base:
                self.processa_ingredienti(ingrediente.fkAlimento, ingrediente.quantita, risultati)

            # Restituisce i risultati con i pesi totali per ogni ingrediente
            return {fk_alimento: data['quantita'] for fk_alimento, data in risultati.items()}

        except Exception as e:
            return {'Error': str(e)}, 500


    def peso_ingredienti_qunatita_totale(self, descrizione, quantita_totale):
        try:
            # Recupera la preparazione in base alla descrizione fornita
            preparazione = self.session.query(TPreparazioni).filter_by(descrizione=descrizione).first()
            if not preparazione:
                return {'Error': 'Nessuna preparazione trovata con questa descrizione.'}, 404

            # Recupera gli ingredienti associati alla preparazione
            ingredienti_base = self.session.query(TPreparazioniContenuti).filter_by(
                fkPreparazione=preparazione.id, 
                dataCancellazione=None).all()
            
            # Inizializza una lista per i risultati
            risultati = []

            # Calcola il peso totale degli ingredienti
            peso_totale_ingredienti = 0

            # Itera su ogni ingrediente di base
            for ingrediente in ingredienti_base:
                # Aggiungi un dizionario per ogni ingrediente
                risultati.append({
                    'fkAlimento': ingrediente.fkAlimento,
                    'quantita': ingrediente.quantita,
                    'fkTipoQuantita': ingrediente.fkTipoQuantita  # Supponendo che questo campo rappresenti il tipo di peso
                })
                peso_totale_ingredienti += ingrediente.quantita  # Somma per il peso totale

            # Calcola le proporzioni basate sulla quantità totale desiderata
            proporzioni = []
            if peso_totale_ingredienti > 0:
                for item in risultati:
                    proporzioni.append({
                        'fkAlimento': item['fkAlimento'],
                        'quantita': round((item['quantita'] / peso_totale_ingredienti) * quantita_totale),
                        'fkTipoQuantita': item['fkTipoQuantita']
                    })

            # Restituisce i risultati con le proporzioni per ogni ingrediente
            return proporzioni

        except Exception as e:
            return {'Error': str(e)}, 500




    def recupero_totale_ingredienti_base(self, descrizione):
        try:
            # Recupera la preparazione in base alla descrizione fornita
            preparazione = self.session.query(TPreparazioni).filter_by(descrizione=descrizione).first()
            if not preparazione:
                return {'Error': 'Nessuna preparazione trovata con questa descrizione.'}, 404

            # Recupera gli ingredienti di base associati alla preparazione
            ingredienti_base = self.session.query(TPreparazioniContenuti).filter_by(
                fkPreparazione=preparazione.id, 
                dataCancellazione=None).all()
            
            # Inizializza il dizionario per i risultati
            risultati = defaultdict(lambda: {'quantita': 0})
            peso_totale = 0  # Aggiungi una variabile per tenere traccia del peso totale degli ingredienti

            # Itera su ogni ingrediente di base
            for ingrediente in ingredienti_base:
                self.processa_ingredienti(ingrediente.fkAlimento, ingrediente.quantita, risultati)
                peso_totale += ingrediente.quantita  # Somma il peso totale degli ingredienti

            # Inizializza un dizionario per i risultati finali
            ingredienti_finali = {}
            calorie_totali = 0
            allergeni_set = set()

            # Somma gli ingredienti con le stesse chiavi
            for key, value in risultati.items():
                ingredienti_finali[key] = value  # Aggiungi ingredienti semplici e composti già processati

            # Calcola le calorie totali e gli allergeni
            for key in ingredienti_finali.keys():
                result = (
                    self.session.query(
                        TAlimenti.energia_Kcal,
                        TAlimenti.fkAllergene
                    )
                    .filter(TAlimenti.id == key)  # Filtra per l'id dell'alimento
                    .first()
                )

                if result:
                    energia_kcal, fk_allergene = result
                    quantita = ingredienti_finali[key]['quantita']
                    calorie_totali += energia_kcal * quantita / 100  # Calcola calorie in base alla quantità

                    if fk_allergene:
                        # Dividi fk_allergene in una lista
                        allergeni_list = [allergene.strip() for allergene in fk_allergene.split(',')]
                        
                        # Aggiungi allergeni al set se non sono '15'
                        for allergene in allergeni_list:
                            if allergene != '15':
                                allergeni_set.add(allergene)

            # Verifica se ci sono allergeni
            if not allergeni_set:
                # Se non ci sono allergeni, assegna '15'
                allergeni_set.add('15')

            # Calcola le calorie per 100 grammi
            if peso_totale > 0:
                calorie_per_100g = (calorie_totali * 100) / peso_totale
            else:
                calorie_per_100g = 0

            # Crea e restituisci un dizionario con i risultati
            return {
                'descrizione': descrizione,
                'calorie_totali': round(calorie_totali) if calorie_totali else 0,
                'calorie_per_100g': round(calorie_per_100g) if calorie_per_100g else 0,  # Calorie per 100g
                'allergeni': ','.join(sorted(allergeni_set)) if allergeni_set else None  # Ordina e unisci in stringa
            }
        except Exception as e:
            print(f"Errore nel recupero degli ingredienti e calorie: {e}")
            return {'Error': str(e)}, 400

        finally:
            self.session.close()



    # def calcola_calorie_per_nome(self, titolo_piatto):
    #     try:
    #         results = (
    #             self.session.query(
    #                 TPreparazioni.descrizione,
    #                 func.sum(TAlimenti.energia_Kcal * TPreparazioniContenuti.quantita / 100).label('calorie_totali'),
    #                 func.count(TPreparazioniContenuti.fkAlimento.distinct()).label('numero_ingredienti'),
    #                 func.group_concat(
    #                     func.distinct(case(
    #                         (TAlimenti.fkAllergene != 15, TAlimenti.fkAllergene)
    #                     ))
    #                 ).label('allergeni')  # Usa DISTINCT per evitare duplicati
    #             )
    #             .join(TPreparazioniContenuti, 
    #                 (TPreparazioniContenuti.fkPreparazione == TPreparazioni.id) & 
    #                 (TPreparazioniContenuti.dataCancellazione == None))  # Aggiungi il filtro per data_cancellazione
    #             .join(TAlimenti, TPreparazioniContenuti.fkAlimento == TAlimenti.id)
    #             .filter(TPreparazioni.descrizione == titolo_piatto)  # Filtra per nome del piatto
    #             .group_by(TPreparazioniContenuti.fkPreparazione)
    #             .first()  # Prendi il primo risultato
    #         )

    #         if results:
    #             calorie_totali = results.calorie_totali if results.calorie_totali is not None else 0  # Imposta a 0 se None
    #             # Crea e restituisci un dizionario con i risultati
    #             return {
    #                 'descrizione': results.descrizione,
    #                 'calorie_totali': calorie_totali,
    #                 'allergeni': results.allergeni
    #             }

    #         # Se non ci sono risultati, ritorna 0 calorie
    #         return {
    #             'descrizione': titolo_piatto,
    #             'calorie_totali': 0,
    #             'allergeni': None
    #         }

    #     except Exception as e:
    #         print(f"Si è verificato un errore: {e}")
    #         return None

    #     finally:
    #         self.session.close()



    def delete(self, id, utenteCancellazione):
        try:
            menu = self.session.query(TPreparazioni).filter_by(id=id).first()
            if menu:
                menu.dataCancellazione = datetime.now()
                menu.utenteCancellazione = utenteCancellazione
                self.session.commit()
                return {'menu': 'deleted!'}, 200
            else:
                return {'Error': f'No match found for this ID: {id}'}, 404
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            # Chiudi sempre la sessione
            self.session.close() 
