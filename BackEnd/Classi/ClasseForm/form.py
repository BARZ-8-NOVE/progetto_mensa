from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,TimeField, SelectField, DecimalField, SelectMultipleField, HiddenField, SubmitField, widgets, BooleanField, DateField, FileField, FormField, FieldList,PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length,  Email, EqualTo
from wtforms.validators import StopValidation
from datetime import datetime


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)

class CustomSelectField(SelectField):
    def pre_validate(self, form):
        pass  # Bypassare la validazione delle scelte

class LogoutFormNoCSRF(FlaskForm):
    submit = SubmitField('Logout')

class LoginFormNoCSRF(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Invia Richiesta')

class CambioEmailForm(FlaskForm):
    email = StringField('Nuova Email', validators=[DataRequired(), Email()])
    email_conferma = StringField('Ripeti Nuova Email', validators=[DataRequired(), Email(), EqualTo('email', message='Le email devono corrispondere.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Reimposta e-mail')

class PasswordResetForm(FlaskForm):
    nuova_password = PasswordField('Nuova Password', validators=[
        DataRequired(), 
        EqualTo('ripeti_nuova_password', message='Le password devono corrispondere')
    ])
    ripeti_nuova_password = PasswordField('Ripeti Nuova Password', validators=[DataRequired()])
    submit = SubmitField('Reimposta Password')

class AlimentiForm(FlaskForm):
    alimento = StringField('Nome', validators=[DataRequired()])
    energia_Kcal = DecimalField('Energia (Kcal)', validators=[DataRequired()])
    energia_KJ = DecimalField('Energia (KJ)', validators=[DataRequired()])
    prot_tot_gr = DecimalField('Proteine (g)', validators=[DataRequired()])
    glucidi_tot = DecimalField('Carboidrati (g)', validators=[DataRequired()])
    lipidi_tot = DecimalField('Grassi (g)', validators=[DataRequired()])
    saturi_tot = DecimalField('Grassi Saturi (g)', validators=[DataRequired()])
    fkAllergene = MultiCheckboxField('Allergene', validators=[MultiCheckboxAtLeastOne()], coerce=int)
    fkTipologiaAlimento = SelectField('Tipologia', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Aggiungi')

class AlimentoForm(FlaskForm):
    fkAlimento = SelectField('Alimento', coerce=int, validators=[Optional()])
    quantita = StringField('Quantità', validators=[Optional()])
    fkTipoQuantita = SelectField('Tipo Quantità', coerce=int, validators=[Optional()])
    note = StringField('Note', validators=[Optional()])

class salvaForm(FlaskForm):
    submit = SubmitField('Salva modifiche')

class OrariForm(FlaskForm):
    nomeOrdine = StringField('Nome Ordine', validators=[DataRequired()])  # Definisce un campo di input di tipo String
    fkServizio = SelectField('Servizio', coerce=int, validators=[Optional()])  # Campo di selezione, le scelte verranno popolate dinamicamente
    tempoLimite = TimeField('Tempo Limite', validators=[DataRequired()])  # Campo di input per il tempo
    ordineDipendente = BooleanField('Ordine Dipendente', default=True)  # Checkbox per ordine dipendente
    ordinePerOggi = BooleanField('Ordine per Oggi', default=True)  # Checkbox per ordine per oggi
    submit = SubmitField('Invia')  # Pulsante di invio



class PreparazioniForm(FlaskForm):
    descrizione = StringField('Descrizione', validators=[Optional()])
    fkTipoPreparazione = SelectField('Tipo Preparazione', coerce=int, validators=[Optional()])
    isEstivo = BooleanField('Estivo', validators=[Optional()])
    isInvernale = BooleanField('Invernale', validators=[Optional()])
    inizio = DateField('Data Inizio', format='%Y-%m-%d', validators=[Optional()])
    fine = DateField('Data Fine', format='%Y-%m-%d', validators=[Optional()])
    immagine = FileField('Immagine', validators=[Optional()])
    submit = SubmitField('Aggiungi')

class TipologiaPiattiForm(FlaskForm):   
    descrizione = StringField('Descrizione', validators=[DataRequired()])
    descrizionePlurale = StringField('Descrizione Plurale', validators=[DataRequired()])
    inMenu = BooleanField('in menu', validators=[Optional()])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()]) 
    color = StringField('Colore', validators=[Optional(), Length(max=7)],
                                  render_kw={"type": "color"})
    backgroundColor = StringField('Colore di Sfondo', validators=[Optional(), Length(max=7)],
                                  render_kw={"type": "color"})
    submit = SubmitField('Aggiungi')

class PiattiForm(FlaskForm):
    fkTipoPiatto = SelectField('Tipo piatto', coerce=int, validators=[DataRequired()])
    codice = StringField('Codice', validators=[DataRequired()])
    titolo = StringField('Tipo Piatto', validators=[DataRequired()])
    descrizione = StringField('Descrizione', validators=[DataRequired()])
    inMenu = BooleanField('In Menu', validators=[Optional()])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()])
    submit = SubmitField('Aggiungi')


class TipologiaMenuForm(FlaskForm):   
    color = StringField('Colore', validators=[Optional(), Length(max=7)],
                                  render_kw={"type": "color"})
    backgroundColor = StringField('Colore di Sfondo', validators=[Optional(), Length(max=7)],
                                  render_kw={"type": "color"})
    descrizione = StringField('Descrizione', validators=[DataRequired()])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()]) 
    submit = SubmitField('Aggiungi')


class MenuForm(FlaskForm):
    # piatto_categoria = RadioField('Categoria', choices=[], validators=[DataRequired()], coerce=int)
    piatti = MultiCheckboxField('piatti', validators=[Optional()], coerce=int)
    preparazioni = SelectMultipleField('Preparazioni', choices=[], coerce=int)
    submit = SubmitField('Aggiungi Menu')


class schedaForm(FlaskForm):
    fkTipoAlimentazione = SelectField('Tipo alimentazione', coerce=int, validators=[DataRequired()])
    fkTipoMenu = SelectField('correlata al menu', coerce=int, validators=[DataRequired()])
    nome = StringField('Nome', validators=[Optional(), Length(max=50)])
    titolo = StringField('Titolo', validators=[Optional(), Length(max=100)])
    sottotitolo = StringField('Sottotitolo', validators=[Optional(), Length(max=100)])
    descrizione = StringField('Descrizione', validators=[Optional(), Length(max=50)])
    backgroundColor = StringField('Colore di Sfondo', validators=[Optional(), Length(max=7)],
                                  render_kw={"type": "color"})
    dipendente = BooleanField('Dipendente', default=False, validators=[Optional()])
    note = TextAreaField('Note', validators=[Optional()])
    inizio = DateField('Inizio', format='%Y-%m-%d', validators=[Optional()], default=datetime.today().date())
    fine = DateField('Fine', format='%Y-%m-%d', validators=[Optional()])
    nominativa = BooleanField('scheda nominativa', default=False, validators=[Optional()])
    submit = SubmitField('Aggiungi Scheda')


class schedaPreconfezionataForm(FlaskForm):
    fkServizio = SelectField('Servizio', coerce=int, validators=[Optional()])  # Campo di selezione, le scelte verranno popolate dinamicamente
    descrizione = StringField('Descrizione', validators=[Optional(), Length(max=50)])
    note = TextAreaField('Note', validators=[Optional()])
    ordinatore = IntegerField('Ordinatore', validators=[Optional()])
    submit = SubmitField('Aggiungi Scheda')

class schedaPiattiForm(FlaskForm):
    piatti = SelectField('Piatti', choices=[], coerce=int)
    note = TextAreaField('Note', validators=[Optional()])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()])
    submit = SubmitField('Aggiungi piatto')

class ordineSchedaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(max=50)])
    letto = StringField('Letto', validators=[DataRequired(), Length(max=5)])
    note = TextAreaField('Note', validators=[Optional()])
    submit = SubmitField('Salva e conferma')

class ordineSchedaDipendentiForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(max=50)])
    note = TextAreaField('Note', validators=[Optional()])
    submit = SubmitField('Salva e conferma')

class ordinedipendenteForm(FlaskForm):

    note = StringField('Note', validators=[Optional()])
    submit = SubmitField('Salva e conferma')

class AllergeniForm(FlaskForm):

    nome = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Salva e conferma')

class UtenteForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    fkTipoUtente = SelectField('Tipo Operatore', coerce=int, validators=[DataRequired()])
    fkFunzCustom= MultiCheckboxField('funzionalità custom', choices=[], coerce=int, validators=[Optional()])
    reparti = MultiCheckboxField('Reparti', choices=[], coerce=int, validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    inizio = DateField('Inizio', format='%Y-%m-%d', validators=[Optional()], default=datetime.today().date())
    fine = DateField('Fine', format='%Y-%m-%d', validators=[Optional()])


class TipoUtenteForm(FlaskForm):
    fkTipoUtente = StringField('Tipo Utente', validators=[DataRequired()])  
    fkFunzionalita = MultiCheckboxField('Permessi', choices=[], coerce=int, validators=[Optional()])    
    submit = SubmitField('Crea Tipo Utente')


class CloneMenuForm(FlaskForm):     
    clone_date = DateField('Data di Clonazione', format='%Y-%m-%d')
    submit = SubmitField('Conferma Clonazione')



class RepartiForm(FlaskForm): 
    codiceAreas = StringField('Codice Area', validators=[DataRequired()])  
    descrizione = StringField('Descrizione', validators=[DataRequired(), Length(max=100)])
    sezione = StringField('Sezione', validators=[DataRequired(), Length(max=50)])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()])
    padiglione = StringField('Padiglione', validators=[Optional(), Length(max=50)])
    piano = StringField('Piano', validators=[Optional(), Length(max=50)])
    lato = StringField('Lato', validators=[Optional(), Length(max=50)])
    inizio = DateField('Inizio', format='%Y-%m-%d', validators=[Optional()], default=datetime.today().date())
    fine = DateField('Fine', format='%Y-%m-%d', validators=[Optional()])


class ServiziForm(FlaskForm): 
   
    descrizione = StringField('Descrizione', validators=[DataRequired(), Length(max=100)])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()])
    inMenu = BooleanField('In Menu', validators=[Optional()])



class ContattiForm (FlaskForm): 
    oggetto = StringField('Oggetto', validators=[DataRequired(), Length(max=100)])
    messaggio = TextAreaField('Messaggio', validators=[DataRequired()])
    submit = SubmitField('Invia')


class CambioPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Vecchia Password', validators=[DataRequired()])
    nuova_password = PasswordField('Nuova Password', validators=[
        DataRequired(), 
        EqualTo('ripeti_nuova_password', message='Le password devono corrispondere')
    ])
    ripeti_nuova_password = PasswordField('Ripeti Nuova Password', validators=[DataRequired()])
    submit = SubmitField('Conferma cambio password')

class BrodoForm(FlaskForm):
    quantita = IntegerField('Quantità', validators=[DataRequired()])
    note = StringField('Note', validators=[Optional()])
    submit = SubmitField('Conferma')
