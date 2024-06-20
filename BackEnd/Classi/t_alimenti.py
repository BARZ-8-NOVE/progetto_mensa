from InfoDB.db_connection import Database
from flask import request

class t_alimenti:

    def __init__(self) -> None:

        self.ID = None
        self.Alimento = None
        self.Parte_Edibile_Gr = None
        self.Energia_Kcal = None
        self.Energia_KJ = None
        self.Acqua_Gr = None
        self.Prot_Tot_Gr = None
        self.Prot_Anim = None
        self.Prot_Veg = None
        self.Glucidi_Tot = None
        self.Amido = None
        self.Glucidi_Solub = None
        self.Lipidi_Tot = None
        self.Saturi_Tot = None
        self.Monoins_Tot = None
        self.Polins_Tot = None
        self.Ac_Oleico = None
        self.Ac_Linoleico = None
        self.Ac_Linolenico = None
        self.Altri_Polins = None
        self.Colesterolo = None
        self.Fibre_Alim = None
        self.Alcool = None
        self.Ferro = None
        self.Ca = None
        self.Na = None
        self.K = None
        self.P = None
        self.Zn = None
        self.Vit_B1 = None
        self.Vit_B2 = None
        self.Vit_B3 = None
        self.Vit_C = None
        self.Vit_B6 = None
        self.Folico = None
        self.Retinolo_Eq = None
        self.Beta_Carotene = None
        self.Vit_E = None
        self.Vit_D = None

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
                    (self.ID, self.Alimento, self.Parte_Edibile_Gr, self.Energia_Kcal, self.Energia_KJ, self.Acqua_Gr, self.Prot_Tot_Gr,
                    self.Prot_Anim, self.Prot_Veg, self.Glucidi_Tot, self.Amido, self.Glucidi_Solub, self.Lipidi_Tot, self.Saturi_Tot,
                    self.Monoins_Tot, self.Polins_Tot, self.Ac_Oleico, self.Ac_Linoleico, self.Ac_Linolenico, self.Altri_Polins, self.Colesterolo,
                    self.Fibre_Alim, self.Alcool, self.Ferro, self.Ca, self.Na, self.K, self.P, self.Zn, self.Vit_B1, self.Vit_B2,
                    self.Vit_B3, self.Vit_C, self.Vit_B6, self.Folico, self.Retinolo_Eq, self.Beta_Carotene, self.Vit_E, self.Vit_D) = result
                    lista = []
                    lista.append({
                        'id': self.ID,
                        'alimento': self.Alimento,
                        'parte_edibile_gr': self.Parte_Edibile_Gr,
                        'energia_kcal': self.Energia_Kcal,
                        'acqua_gr': self.Acqua_Gr,
                        'prot_tot_gr': self.Prot_Tot_Gr,
                        'prot_anim': self.Prot_Anim,
                        'prot_veg': self.Prot_Veg,
                        'glucidi_tot': self.Glucidi_Tot,
                        'lipidi_tot': self.Lipidi_Tot,
                        'saturi_tot': self.Saturi_Tot,
                        'monoins_tot': self.Monoins_Tot,
                        'polins_tot': self.Polins_Tot,
                        'ac_oleico': self.Ac_Oleico,
                        'ac_linoleico': self.Ac_Linoleico,
                        'ac_linoleico': self.Ac_Linolenico,
                        'altri_polins': self.Altri_Polins,
                        'colesterolo': self.Colesterolo,
                        'fibre_alim': self.Fibre_Alim,
                        'alcool': self.Alcool,
                        'ferro': self.Ferro,
                        'ca': self.Ca,
                        'na': self.Na,
                        'k': self.K,
                        'p': self.P,
                        'zn': self.Zn,
                        'vit_b1': self.Vit_B1,
                        'vit_b2': self.Vit_B2,
                        'vit_b3': self.Vit_B3,
                        'vit_c': self.Vit_C,
                        'vit_b6': self.Vit_B6,
                        'folico': self.Folico,
                        'retinolo_eq': self.Retinolo_Eq,
                        'beta_carotene': self.Beta_Carotene,
                        'vit_e': self.Vit_E,
                        'vit_d': self.Vit_D
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