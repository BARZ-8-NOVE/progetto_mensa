from sqlalchemy.orm import relationship

from Classi.ClasseOrdini.Classe_t_ordini.Domain_t_ordini import TOrdini
from Classi.ClasseOrdini.Classe_t_ordiniSchede.Domain_t_ordiniSchede import TOrdiniSchede
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Domain_t_ordiniPiatti import TOrdiniPiatti
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Domain_t_associazionePiattiPreparazioni import TAssociazionePiattiPreparazioni
from Classi.ClasseReparti.Domain_t_reparti import TReparti
from Classi.ClasseServizi.Domani_t_servizi import TServizi
from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi
from Classi.ClasseMenu.Classe_t_menu.Domain_t_menu import TMenu
from Classi.ClasseMenu.Classe_t_tipiMenu.Domain_t_tipiMenu import TTipiMenu
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Domain_t_menuServiziAssociazione import TMenuServiziAssociazione
from Classi.ClasseDiete.Classe_t_tipiAlimentazione.Domain_t_tipiAlimentazione import TTipiAlimentazione
from Classi.ClasseDiete.Classe_t_tipiDiete.Domain_t_tipiDiete import TTipiDiete
from Classi.ClasseSchede.Classe_t_schede.Domani_t_schede import TSchede
from Classi.ClasseSchede.Classe_t_schedePiatti.Domain_t_schedePiatti import TSchedePiatti


# TOrdini.servizi = relationship("TServizi", back_populates="ordine")
# TServizi.ordine = relationship("TOrdini", back_populates="servizi")



# Definire le relazioni ora che tutte le classi sono definite
TOrdiniSchede.ordini_piatti = relationship("TOrdiniPiatti", back_populates="ordiniSchede")
TOrdiniPiatti.ordiniSchede = relationship("TOrdiniSchede", back_populates="ordini_piatti")

TAssociazionePiattiPreparazioni.ordini_piatti = relationship("TOrdiniPiatti", back_populates="associazioni")
TOrdiniPiatti.associazioni = relationship("TAssociazionePiattiPreparazioni", back_populates="ordini_piatti")

TOrdiniSchede.reparti = relationship("TReparti", back_populates="ordiniSchede")
TReparti.ordiniSchede = relationship("TOrdiniSchede", back_populates="reparti")

TOrdiniSchede.servizi = relationship("TServizi", back_populates="ordiniSchede")
TServizi.ordiniSchede = relationship("TOrdiniSchede", back_populates="servizi")




TServizi.menu_servizi = relationship("TMenuServizi", back_populates="servizi")
TMenuServizi.servizi = relationship("TServizi", back_populates="menu_servizi")

TMenu.menu_servizi = relationship("TMenuServizi", back_populates="menu")
TMenuServizi.menu = relationship("TMenu", back_populates="menu_servizi")

TMenu.tipi_menu = relationship("TTipiMenu", back_populates="menu")
TTipiMenu.menu = relationship("TMenu", back_populates="tipi_menu")

TMenuServizi.menu_servizi_associazione = relationship("TMenuServiziAssociazione", back_populates="menu_servizi")
TMenuServiziAssociazione.menu_servizi = relationship("TMenuServizi", back_populates="menu_servizi_associazione")

# TTipiDiete.tipi_alimentazione = relationship('TTipiAlimentazione', backref='tipo_dieta')
# TTipiAlimentazione.tipo_dieta = relationship('TTipiDiete', backref='tipi_alimentazione')

TSchede.tipo_alimentazione = relationship('TTipiAlimentazione', back_populates='schede')
TTipiAlimentazione.schede = relationship('TSchede', back_populates= 'tipo_alimentazione')


TTipiMenu.schede = relationship("TSchede", back_populates="tipo_menu")
TSchede.tipo_menu = relationship('TTipiMenu', back_populates='schede')