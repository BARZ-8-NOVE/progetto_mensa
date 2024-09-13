@app_cucina.route('/ordina_pasto', methods=['GET', 'POST'])
def ordina_pasto():
    if 'authenticated' in session:
        # Imposta la data per domani
        tomorrow = datetime.now() + timedelta(days=1)
        year = request.args.get('year', tomorrow.year, type=int)
        month = request.args.get('month', tomorrow.month, type=int)
        day = request.args.get('day', tomorrow.day, type=int)
        servizio_corrente = request.args.get('servizio', '1')

        # Ottieni i reparti accessibili dall'utente
        user = service_t_utenti.get_utente_by_id(session['user_id'])
        nome = user['nome']
        cognome = user['cognome']
        data = f'{year}-{month}-{day}'

        piatti = service_t_Piatti.get_all()

        # Verifica se esiste già un ordine
        ordine_esistente = service_t_Ordini.existing_Ordine(data, servizio_corrente)
        if not ordine_esistente:
            service_t_Ordini.create(data, servizio_corrente)
            return redirect(url_for('app_cucina.ordina_pasto'))
        
        # Recupera il menu personale e altri dati
        menu_personale = service_t_Schede.get_all_personale()
        servizio = service_t_Servizi.get_all_servizi()
        tipi_menu = service_t_TipiMenu.get_all()
        tipi_menu_map = {int(tipo_menu['id']): tipo_menu['descrizione'] for tipo_menu in tipi_menu}

        # Inizializza variabili
        inf_scheda = None
        preparazioni_map = {}
        piatti_ordine_map = {}
        piatti_map = {}

        # Controlla l'ordine esistente
        controllo_ordine = service_t_OrdiniSchede.get_by_day_and_nome_cognome(data, nome, cognome, int(servizio_corrente))

        # Supponiamo che piatti_map e preparazioni_map siano già disponibili
        if controllo_ordine is not None:
            # Recupera tutti i piatti ordinati associati a quella scheda
            piatti_ordine = service_t_OrdiniPiatti.get_all_by_ordine_scheda(controllo_ordine['id'])
            print('piatti_ordine: ', piatti_ordine)
            
            # Ottieni le informazioni della scheda associata
            inf_scheda = service_t_Schede.get_by_id(controllo_ordine['fkScheda'])
            print('inf_scheda: ', inf_scheda)
            
            # Crea una mappa delle preparazioni in base al tipo di menu e al servizio
            preparazioni_map = get_preparazioni_map(data, inf_scheda['fkTipoMenu'], controllo_ordine['fkServizio'])
            print('preparazioni_map: ', preparazioni_map)
            
            # Crea una nuova mappa per i piatti ordinati
            piatti_ordine_map = {}
            
            # Itera attraverso i piatti ordinati e costruisci la mappa con codice e preparazione
            for piatto_ordine in piatti_ordine:
                piatto_id = int(piatto_ordine['fkPiatto'])
                print('Processing piatto_ordine: ', piatto_ordine)
                
                piatti_map = {int(piatto['id']): {'titolo': piatto['titolo'], 'codice': piatto['codice'], 'fkTipoPiatto': piatto['fkTipoPiatto']} for piatto in piatti}
                # Verifica se il piatto esiste in piatti_map
                if piatto_id in piatti_map:
                    print(f"Piatto trovato in piatti_map con ID {piatto_id}: ", piatti_map[piatto_id])
                    
                    # Aggiungi il piatto alla mappa dei piatti ordinati con i dettagli necessari
                    piatti_ordine_map[piatto_ordine['id']] = {
                        'id': piatto_ordine['id'],
                        'fkPiatto': piatto_ordine['fkPiatto'],
                        'quantita': piatto_ordine['quantita'],
                        'note': piatto_ordine['note'],
                        'titolo': preparazioni_map.get(piatto_id, piatti_map['titolo']),  # Usa la descrizione della preparazione
                        'codice': piatti_map[piatto_id]['codice'],  # Usa il codice del piatto
                        'fkTipoPiatto': piatti_map[piatto_id]['fkTipoPiatto']  # Tipo di piatto (es. primo, secondo, etc.)
                    }
                else:
                    print(f"Piatto con ID {piatto_id} non trovato in piatti_map.")
            
            print('Final piatti_ordine_map: ', piatti_ordine_map)


            
        else:    
            for scheda in menu_personale:
                preparazioni_map = get_preparazioni_map(data, scheda['fkTipoMenu'], int(servizio_corrente))
                
                for piatto in piatti:
                    piatto_id = int(piatto['id'])
                    
                    # Filtra solo i piatti (preparazioni) che fanno parte del menu
                    if piatto_id in preparazioni_map:
                        piatti_map[piatto_id] = {
                            'id': piatto['id'],
                            'titolo': preparazioni_map.get(piatto_id),  # Usa solo la descrizione della preparazione
                            'codice': piatto['codice'],
                            'fkTipoPiatto': piatto['fkTipoPiatto']
                        }
                
                # Assegna piatti_map alla scheda corrente
                scheda['piatti'] = piatti_map

        return render_template(
            'ordina_pasto.html',
            year=year,
            month=month,
            day=day,
            menu_personale=menu_personale,
            servizio_corrente=servizio_corrente,
            reparti=get_user_reparti(user['id']),
            servizio=servizio,
            ordine_esistente=ordine_esistente,
            tipi_menu_map=tipi_menu_map,
            preparazioni_map=preparazioni_map,
            controllo_ordine=controllo_ordine,
            inf_scheda=inf_scheda,
            piatti_map=piatti_map,
            piatti_ordine_map=piatti_ordine_map  # Passa piatti_ordine_map al template
        )
    else:
        return redirect(url_for('app_cucina.login'))