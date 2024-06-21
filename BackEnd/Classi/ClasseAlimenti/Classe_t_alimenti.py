from  Classi.ClasseDB.db_connection import Database
from flask import request

class t_alimenti:

    def __init__(self) -> None:

        self.ID = None
        self.Alimento = None    
        self.Energia_Kcal = None
        self.Energia_KJ = None
        self.Prot_Tot_Gr = None        
        self.Glucidi_Tot = None        
        self.Glucidi_Solub = None
        self.Lipidi_Tot = None
        self.Saturi_Tot = None
        self.fkAllergene = None
        self.fkTipologiaAlimento = None
        

    @property
    def id(self):
        return self.__ID

    def get_t_alimenti_by_id(self):

        try:
            self.DB = Database()
            self.DB.create_connection()
            self.Cursor = self.DB.create_cursor()
            self.DB.begin_transaction()
        except:
            return {'Error': 'Cannot connect to the database'}, 400
        key = request.args
        if 'id' not in key:
            return {'Error':'Wrong Key'}, 403
        try:
            id = int(request.args.get('id'))
        except:
            return {'Error': 'id must be an integer!'}, 403
        if (isinstance(id, int)):
            try:
                self.Cursor.callproc('get_t_alimenti', [id])
                for results in self.Cursor.stored_results():
                    result = results.fetchone()
                    (self.ID, self.Alimento, self.Energia_Kcal, self.Energia_KJ,  self.Prot_Tot_Gr,
                     self.Glucidi_Tot,  self.Lipidi_Tot, self.Saturi_Tot, self.fkAllergene, self.fkTipologiaAlimento
                    ) = result
                    lista = []
                    lista.append({
                        'id': self.ID,
                        'alimento': self.Alimento,
                        'energia_kcal': self.Energia_Kcal,
                        'Energia_KJ':self.Energia_KJ,
                        'prot_tot_gr': self.Prot_Tot_Gr,
                        'glucidi_tot': self.Glucidi_Tot,
                        'lipidi_tot': self.Lipidi_Tot,
                        'saturi_tot': self.Saturi_Tot,
                        'fkAllergene': self.fkAllergene,
                        'fkTipologiaAlimento': self.fkTipologiaAlimento
                      
                    })
                    self.DB.commit_transaction()
                    self.DB.close_connection()
                    return lista
            except Exception as e:
                print(e)
                self.DB.rollback_transaction()
                self.DB.close_connection()
                return {'Error': str(e)}, 500
        else:
            return {'Error': 'id must be an integer'}, 400