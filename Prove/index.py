from flask import Blueprint, render_template
import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from progetto_mensa.BackEnd.Classi.ClasseFrontEnd.Classe_t_FrontEndVociMenu.Repository_t_FrontEndVociMenu import RepositoryTFrontEndVociMenu
from progetto_mensa.BackEnd.Classi.ClasseFrontEnd.Classe_t_FrontEndVociFiglieMenu.Repository_t_FrontEndVociFiglieMenu import RepositoryTFrontEndVociFiglieMenu


def get_padri():
    try:
        response = requests.get('http://localhost:5000/fepadre/get_by_ids?id=4&id=5&id=6&id=7&id=8')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Errore nella chiamata API per padri: {e}")
        return []

app_cucina = Blueprint('app_cucina', __name__, static_folder='static', template_folder='templates')

@app_cucina.route('/login')
def login():
    return render_template('login.html')

@app_cucina.route('/alimenti')
def alimenti():
    return render_template('alimenti.html')

@app_cucina.route('/preparazioni')
def preparazioni():
    return render_template('preparazioni.html')

@app_cucina.route('/creazione_utente')
def creazione_utente():
    return render_template('creazione_utente.html')

@app_cucina.route('/index')
def index():
    return render_template('index.html')

@app_cucina.route('/indexPrincipale')
def indexPrincipale():
    try:
        padri_response = requests.get('http://localhost:5000/fepadre/get_by_ids?id=4&id=5&id=6&id=7&id=8')
        padri_response.raise_for_status()  # Controlla se la richiesta ha avuto successo
        padri = padri_response.json()
    except requests.RequestException as e:
        print(f"Errore nella chiamata API per padri: {e}")
        padri = []

    figli = []
    try:
        repository_padri = RepositoryTFrontEndVociMenu()  # Istanzia l'oggetto RepositoryTFrontEndVociMenu
        for padre in padri:
            figli += repository_padri.get_all_by_fkFrontEndMenu(padre['id'])
    except requests.RequestException as e:
        print(f"Errore nella chiamata API per figli: {e}")
        figli = []


    nipoti = []
    try:
        repository_figli = RepositoryTFrontEndVociFiglieMenu()  # Istanzia l'oggetto RepositoryTFrontEndVociFiglieMenu
        for figlio in figli:
            nipoti += repository_figli.get_all_by_fkFrontEndMenu(figlio['id'])
    except requests.RequestException as e:
        print(f"Errore nella chiamata API per nipoti: {e}")
        nipoti = []

    return render_template('indexPrincipale.html', padri=padri, figli=figli, nipoti=nipoti)