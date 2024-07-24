from sqlalchemy.orm import relationship

from Classi.ClasseOrdini.Classe_t_ordini.Domain_t_ordini import TOrdini
from Classi.ClasseOrdini.Classe_t_ordiniPiatti.Domain_t_ordiniPiatti import TOrdiniPiatti
from Classi.ClassePiatti.Classe_t_associazionePiattiPreparazioni.Domain_t_associazionePiattiPreparazioni import TAssociazionePiattiPreparazioni
from Classi.ClasseReparti.Domain_t_reparti import TReparti
from Classi.ClasseServizi.Domani_t_servizi import TServizi
from Classi.ClasseMenu.Classe_t_menuServizi.Domain_t_menuServizi import TMenuServizi
from Classi.ClasseMenu.Classe_t_menu.Domain_t_menu import TMenu
from Classi.ClasseMenu.Classe_t_tipiMenu.Domain_t_tipiMenu import TTipiMenu
from Classi.ClasseMenu.Classe_t_menuServiziAssociazione.Domain_t_menuServiziAssociazione import TMenuServiziAssociazione

# Definire le relazioni ora che tutte le classi sono definite
TOrdini.ordini_piatti = relationship("TOrdiniPiatti", back_populates="ordini")
TOrdiniPiatti.ordini = relationship("TOrdini", back_populates="ordini_piatti")

TAssociazionePiattiPreparazioni.ordini_piatti = relationship("TOrdiniPiatti", back_populates="associazioni")
TOrdiniPiatti.associazioni = relationship("TAssociazionePiattiPreparazioni", back_populates="ordini_piatti")

TOrdini.reparti = relationship("TReparti", back_populates="ordini")
TReparti.ordini = relationship("TOrdini", back_populates="reparti")

TOrdini.servizi = relationship("TServizi", back_populates="ordini")
TServizi.ordini = relationship("TOrdini", back_populates="servizi")

TServizi.menu_servizi = relationship("TMenuServizi", back_populates="servizi")
TMenuServizi.servizi = relationship("TServizi", back_populates="menu_servizi")

TMenu.menu_servizi = relationship("TMenuServizi", back_populates="menu")
TMenuServizi.menu = relationship("TMenu", back_populates="menu_servizi")

TMenu.tipi_menu = relationship("TTipiMenu", back_populates="menu")
TTipiMenu.menu = relationship("TMenu", back_populates="tipi_menu")

TMenuServizi.menu_servizi_associazione = relationship("TMenuServiziAssociazione", back_populates="menu_servizi")
TMenuServiziAssociazione.menu_servizi = relationship("TMenuServizi", back_populates="menu_servizi_associazione")