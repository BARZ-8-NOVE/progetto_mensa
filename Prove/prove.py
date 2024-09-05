@app_cucina.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'authenticated' in session:
        # Ottieni i parametri dai query string
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        tipo_menu = request.args.get('tipo_menu', '1')

        # Crea un oggetto Calendar
        cal = calendar.Calendar(firstweekday=0)  # 0 per lunedì, 6 per domenica

        # Ottieni la prima e l'ultima data del mese
        first_day_of_month = datetime(year, month, 1)
        last_day_of_month = datetime(year, month, calendar.monthrange(year, month)[1])

        # Ottieni la settimana che contiene il primo giorno del mese
        first_week_start = first_day_of_month - timedelta(days=first_day_of_month.weekday())
        last_week_end = last_day_of_month + timedelta(days=(6 - last_day_of_month.weekday()))

        # Crea un intervallo di giorni che include la settimana precedente e quella successiva
        days = [first_week_start + timedelta(days=i) for i in range((last_week_end - first_week_start).days + 1)]

        # Raggruppa i giorni in settimane
        full_weeks = [days[i:i + 7] for i in range(0, len(days), 7)]

        # Mappa per i giorni della settimana
        weekdays = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
        
        # Calcola il numero della settimana per ogni giorno
        week_numbers = {}
        previous_iso_week_number = None

        for week_index, week in enumerate(full_weeks):
            for day in week:
                if day:
                    # Calcola l'anno e il mese corrente
                    actual_year = day.year
                    actual_month = day.month

                    # Ottieni il numero di settimana ISO
                    iso_week_number = day.isocalendar()[1]

                    # Se è la prima iterazione o se è cambiata la settimana ISO, calcola la settimana ciclica
                    if previous_iso_week_number is None or iso_week_number != previous_iso_week_number:
                        cycle_week_number = (iso_week_number - 1) % 4 + 1
                        previous_iso_week_number = iso_week_number

                    # Memorizza il numero di settimana ciclica
                    week_numbers[(actual_year, actual_month, day.day)] = cycle_week_number

        # Recupera i dati dal servizio
        tipologie_menu = service_t_TipiMenu.get_all()
        menu = service_t_Menu.get_by_date_range(first_week_start, last_week_end, tipo_menu)
        associazione = service_t_AssociazionePiattiPreparazionie.get_all()
        piatti = service_t_Piatti.get_all()
        preparazioni = service_t_preparazioni.get_all_preparazioni()
        servizi = service_t_Servizi.get_all_servizi()
        
        # Recupera gli ID dei menu filtrati per il mese corrente
        menu_ids = [m.get('id') for m in menu if m.get('id') is not None]

    # # Crea menu e servizi se non ci sono abbastanza menu per tutti i giorni del mese
    #     if len(menu_ids) < len(month_days):
    #         for week in month_days:
    #             for day in week:
    #                 if day != 0:  # Salta i giorni che sono parte del mese precedente o successivo
    #                         # Controlla se esiste già un menu per il giorno corrente
    #                     existing_menu = service_t_Menu.get_by_date_and_type(year, month, day, tipo_menu)
    #                     if not existing_menu:
    #                             # Crea un nuovo menu
    #                         new_menu_id = service_t_Menu.create(date(year, month, day), tipo_menu, utenteInserimento=get_username())
    #                         if new_menu_id:
    #                                 # Popola il nuovo menu con i servizi
    #                             for servizio in servizi:
    #                                 new_servizio_id = service_t_MenuServizi.create(new_menu_id, servizio['id'], utenteInserimento=get_username())
                                        
    #                                 old_menu = service_t_Menu.get_by_date_and_type_previous_year(year, month, day, tipo_menu)
    #                                 if old_menu:
    #                                     old_menu_servizi = service_t_MenuServizi.get_all_by_menu_ids(old_menu.id)
    #                                     for old_servizio in old_menu_servizi:
    #                                         if old_servizio['fkServizio'] == servizio['id']:
    #                                             old_menu_piatti = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(old_servizio ['id'])
    #                                             for old_piatto in old_menu_piatti:
    #                                                 service_t_MenuServiziAssociazione.create(new_servizio_id, old_piatto['id'], utenteInserimento=get_username())
                
    #             # Dopo aver creato i menu, servizi e piatti, fai un redirect alla stessa pagina
    #             return redirect(url_for('app_cucina.menu', year=year, month=month, tipo_menu=tipo_menu))



        # Recupera tutti i servizi associati ai menu per il mese
        menu_servizi = service_t_MenuServizi.get_all_by_menu_ids(menu_ids)
        
        # Crea una mappa per gli ID dei servizi associati ai menu
        menu_servizi_map = {}
        for ms in menu_servizi:
            if ms['fkMenu'] not in menu_servizi_map:
                menu_servizi_map[ms['fkMenu']] = {}
            menu_servizi_map[ms['fkMenu']][ms['fkServizio']] = ms['id']
        
        # Organizza i dati per giorno e servizio
        menu_per_giorno = {}
        for menu_item in menu:
            date_key = datetime.strptime(menu_item['data'], '%Y-%m-%d').strftime('%Y-%m-%d')
            if date_key not in menu_per_giorno:
                menu_per_giorno[date_key] = {'id_menu': menu_item['id']}
            # Aggiungi servizi per pranzo e cena
            for servizio in servizi:
                servizio_id = menu_servizi_map.get(menu_item['id'], {}).get(servizio['id'])
                menu_per_giorno[date_key][servizio['descrizione']] = servizio_id

        # Recupera i piatti per ogni servizio dinamicamente
        piattimenu = {}
        for servizio_id in set(id for ids in menu_servizi_map.values() for id in ids.values()):
            piattimenu[servizio_id] = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(servizio_id)
        print(piattimenu)
        # Crea una mappa dei piatti e delle preparazioni
        piatti_map = {int(piatto['id']): piatto['fkTipoPiatto'] for piatto in piatti}
        codice_map = {int(piatto['id']): piatto['codice'] for piatto in piatti}

        preparazioni_map = {int(preparazione['id']): preparazione['descrizione'] for preparazione in preparazioni}

        # Mappa per associare i piatti e le preparazioni
        associazione_map = {}
        for tipo_associa in associazione:
            piatto_nome = piatti_map.get(tipo_associa['fkPiatto'], 'Sconosciuto')
            piatto_codice = codice_map.get(tipo_associa['fkPiatto'], 'Sconosciuto')
            preparazione_descrizione = preparazioni_map.get(tipo_associa['fkPreparazione'], 'Sconosciuto')
            associazione_map[tipo_associa['id']] = {
                'piatto': piatto_nome,
                'codice': piatto_codice,
                'preparazione': preparazione_descrizione
            }



        clona_mese = CloneMenuForm() 
        

        form = CloneMenuForm()
        if request.method == 'POST':
            print('Dati del form POST:', request.form)  # Log dei dati del form
            if clona_mese.validate_on_submit() and 'clona_mese_submit' in request.form:
                try:
                    clone_date = clona_mese.clone_date.data
                    clone_year = clone_date.year
                    clone_month = clone_date.month
                    next_url = request.form.get('next_url', url_for('app_cucina.menu'))  # Usa l'URL di ritorno o un valore di default

                    # Ottieni i menu da clonare nell'intervallo corrente
                    menus_to_clone = service_t_Menu.get_by_date_range(first_week_start, last_week_end, tipo_menu)

                    for menu_to_clone in menus_to_clone:
                        # Ottieni la data originale del menu da clonare
                        original_menu_date = datetime.strptime(menu_to_clone['data'], '%Y-%m-%d').date()

                        # Calcola la nuova data nel mese e anno di destinazione
                        new_menu_date = date(clone_year, clone_month, original_menu_date.day)

                        # Verifica se il menu per la nuova data esiste già
                        existing_menu = service_t_Menu.get_by_data(new_menu_date, tipo_menu)

                        if existing_menu:
                            # Se il menu esiste, usa il suo ID
                            new_menu_id = existing_menu['id']
                        else:
                            # Se il menu non esiste, creane uno nuovo
                            new_menu_id = service_t_Menu.create(new_menu_date, tipo_menu, utenteInserimento=get_username())

                        # Clonare i servizi associati al menu originale
                        menu_servizi_to_clone = service_t_MenuServizi.get_all_by_menu_ids([menu_to_clone['id']])
                        for servizio in menu_servizi_to_clone:
                            # Verifica se il servizio associato esiste già per il nuovo menu
                            existing_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(new_menu_id, servizio['fkServizio'])

                            if existing_servizio:
                                # Se il servizio esiste, cancelliamo le associazioni piatti-preparazioni esistenti
                                service_t_MenuServiziAssociazione.delete_per_menu(existing_servizio['id'], utenteCancellazione=get_username())
                                new_servizio_id = existing_servizio['id']
                            else:
                                # Se il servizio non esiste, creane uno nuovo
                                new_servizio_id = service_t_MenuServizi.create(new_menu_id, servizio['fkServizio'], utenteInserimento=get_username())

                            # Clona le associazioni piatti-preparazioni per il nuovo servizio
                            assoc_piatti = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(servizio['id'])
                            for associazione in assoc_piatti:
                                service_t_MenuServiziAssociazione.create(new_servizio_id, associazione['fkPiatto'], associazione['fkPreparazione'], utenteInserimento=get_username())

                    flash('Mese clonato con successo!', 'success')
                    return redirect(next_url)

                except Exception as e:
                    flash(f"Errore durante la clonazione del mese: {str(e)}", 'error')

            
            
            if form.validate_on_submit():
                try:
                    menu_id = request.form['menu_id']
                    clone_date = form.clone_date.data.strftime('%Y-%m-%d')
                    next_url = request.form.get('next_url', url_for('app_cucina.menu'))  # Usa l'URL di ritorno o un valore di default
                   

                    # Funzione helper per recuperare il menu da clonare
                    def get_menu_data(menu_id):
                        assoc_piatti = service_t_MenuServiziAssociazione.get_by_fk_menu_servizio(menu_id)
                        menu = service_t_MenuServizi.get_by_id(menu_id)
                        tipo_menu = service_t_Menu.get_by_id(menu['fkMenu'])
                        return assoc_piatti, menu, tipo_menu

                    # Recupera i dati necessari per la clonazione
                    assoc_piatti, menu_da_clonare, tipo_menu_da_clonare = get_menu_data(menu_id)

                    # Recupera o crea il menu per la nuova data
                    menu_by_data = service_t_Menu.get_by_data(clone_date, tipo_menu_da_clonare['fkTipoMenu'])

                    if menu_by_data is None:
                        new_menu_id = service_t_Menu.create(clone_date, tipo_menu_da_clonare['fkTipoMenu'], utenteInserimento=get_username())
                        
                        # Recupera i dettagli del nuovo menu usando il suo ID
                        menu_by_data = service_t_Menu.get_by_id(new_menu_id)

                    # Assicurati che `menu_by_data` sia un dizionario
                    if not isinstance(menu_by_data, dict):
                        raise ValueError("Errore: menu_by_data dovrebbe essere un dizionario")

                    # Recupera o crea il servizio associato al menu
                    menu_servizio = service_t_MenuServizi.get_all_by_menu_ids_con_servizio(menu_by_data['id'], menu_da_clonare['fkServizio'])

                    if menu_servizio is None:
                        menu_servizio = service_t_MenuServizi.create(menu_by_data['id'], menu_da_clonare['fkServizio'], utenteInserimento=get_username())

                    # Verifica che `menu_servizio` sia un dizionario
                    if not isinstance(menu_servizio, dict):
                        raise ValueError("Errore: menu_servizio dovrebbe essere un dizionario")

                    # Cancella e ricrea le associazioni dei piatti per il nuovo menu
                    service_t_MenuServiziAssociazione.delete_per_menu(menu_servizio['id'], utenteCancellazione=get_username())
                    for associazione in assoc_piatti:
                        service_t_MenuServiziAssociazione.create(menu_servizio['id'], associazione['id'], utenteInserimento=get_username())

                    flash('Menu clonato con successo!', 'success')
                    return redirect(next_url)
                
                except ValueError as ve:
                    flash(f"Errore di validazione: {str(ve)}", 'error')

                except Exception as e:
                    flash(f"Errore durante la clonazione del menu: {str(e)}", 'error')

            else:
                print('Errori di validazione del form:', form.errors)  # Log per errori di validazione

        return render_template(
                    'menu.html',
                    year=year,
                    month=month,
                    month_name=calendar.month_name[month],
                    full_weeks=full_weeks,
                    weekdays=weekdays,
                    tipologie_menu=tipologie_menu,
                    menu_per_giorno=menu_per_giorno,
                    piatti_map=piatti_map,
                    preparazioni_map=preparazioni_map,
                    associazione_map=associazione_map,
                    piattimenu=piattimenu,  # Passa piattimenu al template
                    piatti=piatti,
                    preparazioni=preparazioni,
                    datetime=datetime,
                    calendar=calendar,
                    week_numbers=week_numbers,  # Passa i numeri delle settimane al template
                    form=form,
                    clona_mese=clona_mese
                )
    else:
        return redirect(url_for('app_cucina.login'))