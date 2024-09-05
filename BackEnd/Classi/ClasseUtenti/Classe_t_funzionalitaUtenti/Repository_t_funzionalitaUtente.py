
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente 
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtenti.Classe_t_tipiUtenti.Domain_t_tipiUtenti import TTipiUtenti
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti# Adjust the import path as per your project structure
from Classi.ClasseDB.db_connection import engine
from sqlalchemy.orm import sessionmaker
class TFunzionalitaUtenteRepository:
    def __init__(self, ):
        Session = sessionmaker(bind=engine)
        self.session = Session()



    def get_funzionalita_utente_by_id(self, funzionalita_utente_id: int):
        return self.session.query(TFunzionalitaUtente).filter(TFunzionalitaUtente.id == funzionalita_utente_id).first()

    def get_funzionalita_utenti_by_user_type(self, tipo_utente_id: int):
        return self.session.query(TFunzionalitaUtente).filter(TFunzionalitaUtente.fkTipoUtente == tipo_utente_id).all()

    def get_funzionalita_utenti_by_funzionalita(self, funzionalita_id: int):
        return self.session.query(TFunzionalitaUtente).filter(TFunzionalitaUtente.fkFunzionalita == funzionalita_id).all()

    def get_all_funzionalita_utenti(self):
        return self.session.query(TFunzionalitaUtente).all()
    
    def get_menu_data(self, user_id: int):
        return (self.session.query(
                    TFunzionalita.id.label('funzionalita_id'),
                    TFunzionalita.fkPadre,
                    TFunzionalita.titolo,
                    TFunzionalita.label,
                    TFunzionalita.icon,
                    TFunzionalita.link,
                    TFunzionalita.ordinatore,
                    TFunzionalita.target,
                    TFunzionalita.dataCancellazione,
                    TTipiUtenti.id.label('tipo_utente_id'),
                    TTipiUtenti.nomeTipoUtente,
                    TFunzionalitaUtente.permessi
                )
                .select_from(TUtenti)  # Specify the starting point of the query
                .join(TTipiUtenti, TUtenti.fkTipoUtente == TTipiUtenti.id)
                .join(TFunzionalitaUtente, TTipiUtenti.id == TFunzionalitaUtente.fkTipoUtente)
                .join(TFunzionalita, TFunzionalitaUtente.fkFunzionalita == TFunzionalita.id)
                .filter(TUtenti.id == user_id,
                        TFunzionalita.menuPrincipale == True  # Filtro per menu principale
                        )
                .order_by(TFunzionalita.ordinatore)  
                .all())

    def get_funz_utenti_by_user_type(self, tipo_utente_id: int):
        funzionalita_utenti = self.session.query(TFunzionalitaUtente).filter(
            TFunzionalitaUtente.fkTipoUtente == tipo_utente_id
        ).all()
        
        # Convert each TFunzionalitaUtente object to a dictionary
        funzionalita_utenti_dicts = []
        for funz in funzionalita_utenti:
            funz_dict = {
                'id': funz.id,
                'fkTipoUtente': funz.fkTipoUtente,
                'fkFunzionalita': funz.fkFunzionalita,
                'permessi': funz.permessi
            }
            funzionalita_utenti_dicts.append(funz_dict)
        
        return funzionalita_utenti_dicts
    
    

    def create(self, tipo_utente_id, fkFunzionalita, permessi):
        try:
            tipoUtente = TFunzionalitaUtente(
                fkTipoUtente=tipo_utente_id,
                fkFunzionalita=fkFunzionalita,
                permessi=permessi
            )
            self.session.add(tipoUtente)
            self.session.commit()
            return {'tipo Utente': 'added!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()


    def delete_by_tipo_utente(self, tipo_utente_id):
        try:
            # Trova tutte le funzionalità associate al tipo di utente specificato
            rows_to_delete = self.session.query(TFunzionalitaUtente).filter_by(fkTipoUtente=tipo_utente_id).all()
            
            if not rows_to_delete:
                return {'Message': 'No functionalities found for this user type'}, 404

            # Elimina le righe trovate
            for row in rows_to_delete:
                self.session.delete(row)
            
            self.session.commit()
            return {'Message': f'All functionalities for user type {tipo_utente_id} deleted!'}, 200
        except Exception as e:
            self.session.rollback()
            return {'Error': str(e)}, 500
        finally:
            if self.session:
                self.session.close()
