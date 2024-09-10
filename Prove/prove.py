@app_cucina.route('/impostazioni', methods=['GET', 'POST'])
def impostazioni():
    if 'authenticated' in session:
        user = service_t_utenti.get_utente_by_id(session['user_id'])
        tipi_utenti = service_t_tipiUtenti.get_tipiUtenti_all()

        tipi_utenti_map = {int(tipo_utente['id']): tipo_utente['nomeTipoUtente'] for tipo_utente in tipi_utenti}

        form = CambioPasswordForm()

        if form.validate_on_submit():
            # Verifica la vecchia password
            password_ok = service_t_utenti.check_password(
                form.username,  # Usa l'username dell'utente loggato
                form.password.data
            )

            if password_ok:
                # Verifica se la nuova password e la conferma sono uguali
                if form.nuova_password.data == form.ripeti_nuova_password.data:
                    # Aggiorna la password dell'utente
                    service_t_utenti.update_utente_password_by_username(
                        form.username,  # Usa l'username dell'utente loggato
                        form.nuova_password.data
                    )
                    flash('Password cambiata con successo!', 'success')
                else:
                    flash('La nuova password e la conferma non corrispondono.', 'error')
            else:
                flash('La vecchia password è errata.', 'error')

        return render_template('impostazioni.html',
                               user=user,
                               tipi_utenti_map=tipi_utenti_map,
                               form=form
                               )
    else:
        return redirect(url_for('app_cucina.login'))
