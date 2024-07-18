from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, SubmitField, widgets, BooleanField, DateField, FileField, FormField, FieldList
from wtforms.validators import DataRequired, Optional
from wtforms.validators import StopValidation

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

class AlimentiForm(FlaskForm):
    alimento = StringField('Nome', validators=[DataRequired()])
    energia_Kcal = IntegerField('Energia (Kcal)', validators=[DataRequired()])
    energia_KJ = IntegerField('Energia (KJ)', validators=[DataRequired()])
    prot_tot_gr = IntegerField('Proteine (g)', validators=[DataRequired()])
    glucidi_tot = IntegerField('Carboidrati (g)', validators=[DataRequired()])
    lipidi_tot = IntegerField('Grassi (g)', validators=[DataRequired()])
    saturi_tot = IntegerField('Grassi Saturi (g)', validators=[DataRequired()])
    fkAllergene = MultiCheckboxField('Allergene', validators=[MultiCheckboxAtLeastOne()], coerce=int)
    fkTipologiaAlimento = SelectField('Tipologia', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Aggiungi')

class AlimentoForm(FlaskForm):
    fkAlimento = SelectField('Alimento', coerce=int, validators=[Optional()])
    quantita = StringField('Quantità', validators=[Optional()])
    fkTipoQuantita = SelectField('Tipo Quantità', coerce=int, validators=[Optional()])
    note = StringField('Note', validators=[Optional()])

class PreparazioniForm(FlaskForm):
    descrizione = StringField('Descrizione', validators=[DataRequired()])
    fkTipoPreparazione = SelectField('Tipo Preparazione', coerce=int, validators=[DataRequired()])
    isEstivo = BooleanField('Estivo', validators=[Optional()])
    isInvernale = BooleanField('Invernale', validators=[Optional()])
    inizio = DateField('Data Inizio', format='%Y-%m-%d', validators=[Optional()])
    fine = DateField('Data Fine', format='%Y-%m-%d', validators=[Optional()])
    immagine = FileField('Immagine', validators=[Optional()])

    alimenti = FieldList(FormField(AlimentoForm), min_entries=1)  # Initialize FieldList with a minimum of 1

    submit = SubmitField('Aggiungi')

class PiattiForm(FlaskForm):
    fkTipoPiatto = SelectField('Tipo piatto', coerce=int, validators=[DataRequired()])
    codice = StringField('Codice', validators=[DataRequired()])
    titolo = StringField('Tipo Piatto', validators=[DataRequired()])
    descrizione = StringField('Descrizione', validators=[DataRequired()])
    inMenu = BooleanField('In Menu', validators=[DataRequired()])
    ordinatore = IntegerField('Ordinatore', validators=[DataRequired()])

    submit = SubmitField('Aggiungi')

