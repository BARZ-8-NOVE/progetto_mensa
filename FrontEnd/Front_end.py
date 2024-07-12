from flask import Blueprint, render_template, url_for
import requests


app_cucina = Blueprint('app_cucina', __name__, static_folder='static', template_folder='templates')


def get_menu_data():
    response = requests.get('http://localhost:5000/funzionalita/get_all')
    if response.status_code == 200:
        data = response.json()  # Converti la risposta in JSON
        return data
    else:
        return []  # Gestione del caso in cui la richiesta non sia andata a buon fine

def build_menu_structure(data):
    menu_structure = []
    
    # Prima passata: aggiungi i padri senza figli e nipoti
    for item in data:
        if item['fkPadre'] is None:
            item['figli'] = []
            item['nipoti'] = []  # Inizializza la lista dei nipoti
            menu_structure.append(item)
    
    # Seconda passata: aggiungi figli e inizializza lista nipoti vuota per i figli
    for item in data:
        if item['fkPadre'] is not None:
            for padre in menu_structure:
                if padre['id'] == item['fkPadre']:
                    # Verifica se l'elemento è già stato aggiunto come figlio
                    if item not in padre['figli']:
                        item['nipoti'] = []  # Inizializza la lista dei nipoti per l'item
                        padre['figli'].append(item)
                    break
    
    # Terza passata: aggiungi nipoti ai figli
    for padre in menu_structure:
        for figlio in padre['figli']:
            figlio['nipoti'] = []  # Inizializza la lista dei nipoti per ogni figlio
            for item in data:
                if item['fkPadre'] == figlio['id']:
                    # Verifica se l'elemento è già stato aggiunto come nipote
                    if item not in figlio['nipoti']:
                        figlio['nipoti'].append(item)
    
    return menu_structure




@app_cucina.route('/index')
def indexPrincipale():    
    data = get_menu_data()
    menu_structure = build_menu_structure(data)
    return render_template('index.html', menu_structure=menu_structure)

@app_cucina.route('/login')
def login():
    return render_template('login.html')

@app_cucina.route('/alimenti')
def alimenti():
    data = get_menu_data()
    menu_structure = build_menu_structure(data)

    return render_template('alimenti.html', menu_structure=menu_structure)

@app_cucina.route('/preparazioni')
def preparazioni():
    return render_template('preparazioni.html')

@app_cucina.route('/creazione_utente')
def creazione_utente():
    return render_template('creazione_utente.html')

@app_cucina.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

