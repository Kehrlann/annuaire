# coding=utf-8
from datetime import datetime
import os

from werkzeug.utils import secure_filename
from flask import render_template, request, url_for, redirect, session, flash
from flask.ext.login import current_user, login_required
import requests
from lxml import etree

from annuaire_anciens import app, annuaire, user, PAYS
from annuaire_anciens.helper.security import generate_csrf_token


@app.route('/compte/', methods=['GET'])
@login_required
def compte():
    adresse_label =  ""
    ancien_form = user.update_ancien_form()

    # chopper l'ancien associé à l'utilisateur
    utilisateur = user.find_user_by_id(current_user.id)

    # get data by id ancien
    ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)
    if ancien is not None:
        ancien_form.load_ancien(ancien)

    adresse = annuaire.find_adresse_by_id_ancien(utilisateur.id_ancien)
    if adresse is not None:
        if adresse['adresse_adresse'] is not None:
            adresse_label += adresse['adresse_adresse']+', '
        if adresse['ville_nom'] is not None:
            adresse_label += adresse['ville_nom'] + ' '

    experiences = annuaire.find_experience_by_id_ancien(utilisateur.id_ancien)

    # préparer l'url pour connecter l'utilisateur à LinkedIn si ce n'est pas déjà fait
    linkedin_url = ("https://www.linkedin.com/uas/oauth2/authorization?"
                        "response_type=code&"
                        "client_id=%s&"
                        "scope=%s"
                        "&state=%s"
                        "&redirect_uri=%s" %
                        (app.config['LINKEDIN_KEY'],
                         app.config['LINKEDIN_SCOPE'],
                         generate_csrf_token(),
                         url_for('connect_linkedin', _external=True)))

    # préparer l'url pour connecter l'utilisateur à LinkedIn si ce n'est pas déjà fait
    import_linkedin_url = ("https://www.linkedin.com/uas/oauth2/authorization?"
                        "response_type=code&"
                        "client_id=%s&"
                        "scope=%s"
                        "&state=%s"
                        "&redirect_uri=%s" %
                        (app.config['LINKEDIN_KEY'],
                         app.config['LINKEDIN_SCOPE'],
                         generate_csrf_token(),
                         url_for('import_linkedin', _external=True)))

    return render_template('user/compte.html',
                           adresse = adresse_label,
                           ancien = ancien,
                           experiences = experiences,
                           utilisateur = current_user,
                           linkedin_url = linkedin_url,
                           import_linkedin_url = import_linkedin_url)


@app.route('/compte/password/', methods=['GET', 'POST'])
@login_required
def update_password():
    form = user.change_password_form()

    if request.method == 'POST':
        # Confirmer
        form = user.change_password_form(request.form)
        form_confirmed = form.validate()

        # verifier que l'ancien mot de passe est le bon
        password_confirmed = user.confirm_password(current_user.id, form.old_password.data)
        if not password_confirmed:
            app.logger.warning("UPDATE PASS - wrong password for user with id %s", current_user.id)
            form.old_password.errors = ['Ancien mot de passe incorrect']

        # si tout va bien, mettre a jour.
        if form_confirmed and password_confirmed:
            result = user.update_password_by_id(current_user.id, form.old_password.data, form.new_password.data)
            if result:
                app.logger.info("UPDATE PASS - successfully changed password  for user with id %s", current_user.id)
                flash("Mot de passe correctement mis &agrave; jour", "success")
            else:
                app.logger.error("UPDATE PASS - error changing password  for user with id %s", current_user.id)
                flash("Probl&egrave;me &agrave; la mise &agrave; jour, contacter l'administrateur", "error")
            return redirect(url_for("compte"))

    return render_template("user/password_form.html", form=form)

@app.route('/compte/info/', methods=['GET', 'POST'])
@login_required
def update_info_perso():
    form = user.update_ancien_form()

    utilisateur = user.find_user_by_id(current_user.id)
    ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)

    if ancien is not None:
        form.load_ancien(ancien)

        if request.method == 'POST':
            # Confirmer
            form = user.update_ancien_form(request.form)
            form_confirmed = form.validate()


            # si tout va bien, mettre a jour.
            if form_confirmed:
                success = annuaire.update_fiche_ancien(
                    ancien['id_ancien'],
                    form.telephone.data,
                    form.mobile.data,
                    form.site.data,
                    form.mail_perso.data
                )
                if success:
                    app.logger.info(
                        "UPDATE INFO - successfully info for user with id %s, id ancien : %s, errors : %s",
                        current_user.id,
                        ancien['id_ancien'],
                        )
                    flash("Informations personnelles correctement mises &agrave; jour", "success")
                    return redirect(url_for("compte"))

                app.logger.info("UPDATE INFO - failed insert for user with id %s", current_user.id)
            app.logger.info("UPDATE INFO - failed insert for user with id %s", current_user.id)

    return render_template("user/info_perso_form.html", ancien_form=form)


@app.route('/compte/adresse/', methods=['GET', 'POST'])
@login_required
def update_adresse():
    adresse_form = user.update_adresse_form()
    adresse_form.set_pays(PAYS)

    utilisateur = user.find_user_by_id(current_user.id)

    if utilisateur.id_ancien is not None:
        adresse = annuaire.find_adresse_by_id_ancien(utilisateur.id_ancien)
        if adresse is not None:
            adresse_form.load_adresse(adresse)

        if request.method == 'POST':
            # Confirmer
            adresse_form = user.update_adresse_form(request.form)
            adresse_form.set_pays(PAYS)
            form_confirmed = adresse_form.validate()

            # si tout va bien, mettre a jour.
            if form_confirmed:
                annuaire.update_adresse_perso(
                    utilisateur.id_ancien,
                    adresse_form.ville.data,
                    adresse_form.pays.data,
                    adresse_form.adresse.data,
                    adresse_form.code.data
                )
                flash("Adresse personnelle mise &agrave; jour", "success")
                return redirect(url_for("compte"))

        return render_template("user/adresse_form.html", adresse_form=adresse_form)
    else:
        return redirect(url_for("compte"))

@app.route('/compte/experience/', methods=['GET', 'POST'])
@app.route('/compte/experience/<int:id_experience>', methods=['GET', 'POST'])
@login_required
def update_experience(id_experience = None):
    experience_form = user.update_experience_form()
    experience_form.set_pays(PAYS)

    utilisateur = user.find_user_by_id(current_user.id)

    if utilisateur.id_ancien is not None:

        if request.method == 'POST':
            experience_form = user.update_experience_form(request.form)
            experience_form.set_pays(PAYS)
            form_confirmed = experience_form.validate()

            if form_confirmed:
                try:
                    date_debut = datetime.strptime(experience_form.date_debut.data, '%m/%Y')
                except ValueError:
                    date_debut = None
                try:
                    date_fin = datetime.strptime(experience_form.date_fin.data, '%m/%Y')
                except ValueError:
                    date_fin = None

                annuaire.update_experience(
                    utilisateur.id_ancien,
                    id_experience,
                    experience_form.ville.data,
                    experience_form.pays.data,
                    experience_form.adresse.data,
                    experience_form.code.data,
                    experience_form.entreprise.data,
                    experience_form.poste.data,
                    experience_form.description.data,
                    experience_form.mail.data,
                    experience_form.site.data,
                    experience_form.telephone.data,
                    experience_form.mobile.data,
                    date_debut,
                    date_fin
                )
                if id_experience is not None:
                    flash("Exp&eacute;rience professionnelle modifi&eacute;e", "success")
                else:
                    flash("Exp&eacute;rience professionnelle ajout&eacute;e", "success")

                return redirect(url_for('compte'))

        else:
            experience = annuaire.find_experience_by_id_ancien_id_experience(utilisateur.id_ancien, id_experience)
            if experience is not None:
                experience = experience.first()
            if experience is not None:
                experience_form.load_experience(experience)

        return render_template("user/experience_form.html", form=experience_form, id_experience=id_experience)

    else:
        return redirect(url_for('compte'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/compte/photo/', methods=['GET', 'POST'])
@login_required
def update_photo():
    """
    Mettre à jour la photo d'un ancien.
    Si GET : la page de mise à jour
    Si POST : on récupère la photo, on la sauvegarde, on vire l'ancienne et on redirige vers compte
    @return:
    """
    utilisateur = user.find_user_by_id(current_user.id)
    if utilisateur.id_ancien is not None:
        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)
        if ancien is not None:
            photo = ancien['photo']
        else:
            photo = None

        # Si c'est une requete post (envoi) alors c'est une nouvelle photo  à traiter
        if request.method == 'POST' and ancien is not None:
            uploaded_file = request.files['file']
            if uploaded_file and allowed_file(uploaded_file.filename):

                # upload de l'ancienne photo
                id_photo = user.get_next_photo_id()
                extension = uploaded_file.filename.rsplit('.', 1)[1]
                filename = secure_filename(str(id_photo)+"."+extension)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # mise à jour de la fiche ancien avec la nouvelle photo
                annuaire.update_photo(ancien['id_ancien'], filename)
                app.logger.info(
                    "PHOTO - succes for user with %s, ancien : %s, photo name : %s, number : %s",
                    current_user.id,
                    ancien['id_ancien'],
                    uploaded_file.filename,
                    id_photo)

                # supression de l'ancienne photo
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ancien['photo'])))
                    app.logger.info(
                        "PHOTO - ancien : %s, removed file : %s",
                        ancien['id_ancien'],
                        ancien['photo'])
                except:
                    app.logger.info(
                        "PHOTO - failed to remove for : %s",
                        ancien['id_ancien'])

                flash('Photo mise &agrave; jour', 'success')

            elif uploaded_file and not allowed_file(uploaded_file.filename):
                app.logger.info(
                    "PHOTO - forbidden for ancien : %s, photo : %s",
                    ancien['id_ancien'],
                    uploaded_file.filename)
                flash("Format de photo invalide", "error")

            elif not uploaded_file:
                 # supprimer la photo dans la fiche ancien
                app.logger.info(
                    "PHOTO - remove for : %s",
                    ancien['id_ancien'])

                annuaire.update_photo(ancien['id_ancien'], None)

                # supression de l'ancienne photo
                # supression de l'ancienne photo
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ancien['photo'])))
                    app.logger.info(
                        "PHOTO - ancien : %s, removed file : %s",
                        ancien['id_ancien'],
                        ancien['photo'])
                except:
                    app.logger.info(
                        "PHOTO - failed to remove for : %s",
                        ancien['id_ancien'])
                flash("Photo supprim&eacute;e", "warning")


        elif ancien is not None:
            return render_template('user/picture_form.html', photo=photo)

    return redirect(url_for('compte'))


@app.route('/compte/experience/remove/<int:id_experience>', methods=['POST'])
@login_required
def remove_experience(id_experience):
    """
    Supprimer une expérience par id
    @param id_experience:
    @return: redirect @compte
    """
    utilisateur = user.find_user_by_id(current_user.id)
    if utilisateur.id_ancien is not None:
        annuaire.remove_experience(utilisateur.id_ancien, id_experience)
        app.logger.info(
            "EXPERIENCE - successfully removed experience :%s, for ancien : %s, user : %s",
            id_experience,
            utilisateur.id_ancien,
            utilisateur.id)
        flash("Exp&eacute;rience supprim&eacute;e", "success")

    return redirect(url_for('compte'))

@app.route("/compte/linkedin/authorize/", methods=['GET'])
@login_required
def connect_linkedin():
    success = False
    utilisateur = user.find_user_by_id(current_user.id)
    app.logger.info(
            "LINKEDIN - begin authorize for ancien : %s, user : %s",
            utilisateur.id_ancien,
            utilisateur.id)

    if utilisateur.id_ancien is not None:
        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)
        if ancien is not None:
            access_token = __get_linkedin_token(url_for('connect_linkedin', _external=True))
            api_url = "https://api.linkedin.com/v1/people/~:(id,public-profile-url)?oauth2_access_token=%s" % access_token
            api_req =  requests.get(api_url)
            if api_req is not None and api_req.status_code == requests.codes.ok:
                parsed = etree.fromstring(api_req.text.encode("utf-8"))
                if parsed is not None:
                    id_linkedin = None
                    url_linkedin = None
                    for e in parsed:
                        if e.tag == "id":
                            id_linkedin = e.text
                        elif e.tag == "public-profile-url":
                            url_linkedin = e.text
                    if url_linkedin is not None and id_linkedin is not None:
                        success = annuaire.update_linkedin_ancien(ancien['id_ancien'], id_linkedin, url_linkedin)
                        app.logger.info(
                            "LINKEDIN - successful update for user : %s, ancien : %s, id_linkedin : %s, url public profile : %s",
                            utilisateur.id, ancien['id_ancien'], id_linkedin, url_linkedin)

            if not success:
                app.logger.error(
                    "LINKEDIN - bad people API request for user : %s, code : %s, request response : %s",
                    utilisateur.id, api_req.status_code, api_req.text)

    if success:
        flash("Profil linkedin correctement connect&eacute; !", "success")
    else:
        flash("Oups ! Il y a eu un probl&egrave;me pendant la connexion. Merci de contacter l'administrateur.", "error")
    return redirect(url_for("compte"))


@app.route("/compte/linkedin/disconnect/", methods=['POST'])
@login_required
def disconnect_linkedin():
    """
    Virer l'experience linkedin d'un ancien
    @return:
    """
    utilisateur = user.find_user_by_id(current_user.id)
    if utilisateur.id_ancien is not None:
        app.logger.info(
            "LINKEDIN - successful unlink for user : %s, ancien : %s",
            utilisateur.id, utilisateur.id_ancien)
        annuaire.update_linkedin_ancien(utilisateur.id_ancien)
        flash("Compte LinkedIn dissoci&eacute; de l'annuaire", "success")
    return redirect(url_for('compte'))


@app.route("/compte/linkedin/import/", methods=['GET'])
@login_required
def import_linkedin():
    import_success = False
    saved_positions = 0
    utilisateur = user.find_user_by_id(current_user.id)
    app.logger.info(
            "LINKEDIN - begin import for ancien : %s, user : %s",
            utilisateur.id_ancien,
            utilisateur.id)

    if utilisateur.id_ancien is not None:
        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)
        if ancien is not None:
            access_token = __get_linkedin_token(url_for('import_linkedin', _external=True))
            api_url = "https://api.linkedin.com/v1/people/~:(id,positions)?oauth2_access_token=%s" % access_token
            api_req =  requests.get(api_url)
            if api_req is not None and api_req.status_code == requests.codes.ok:
                parsed = etree.fromstring(api_req.text.encode("utf-8"))
                if parsed is not None:
                    positions = []
                    for e in parsed:
                        if e.tag == "positions":
                            positions = __get_positions(e)

                    if len(positions) > 0:

                        # récupérer les positions existantes pour update. A voir.
                        # sql_experiences = annuaire.find_experience_by_id_ancien(utilisateur.id_ancien)
                        # experiences = sql_experiences.fetchall()
                        # sql_experiences.close()

                        import_success = True

                        for position in positions:
                            app.logger.info(
                                "LINKEDIN - saving experience for user %s, enreprise : %s, position : %s, id_xp : %s",
                                utilisateur.id,
                                position['entreprise'],
                                position['position'],
                                position['id_experience_linkedin']
                            )
                            success = annuaire.update_experience(
                                utilisateur.id_ancien,
                                None,
                                None,
                                None,
                                None,
                                None,
                                position['entreprise'],
                                position['position'],
                                position['description'],
                                None,
                                None,
                                None,
                                None,
                                position['date_debut'],
                                position['date_fin'],
                                position['id_experience_linkedin']
                            )

                            if not success:
                                app.logger.error("LINKEDIN - error saving experience for user %s, id experience : %s")
                                app.logger.warning(position)
                                import_success=False
                            else:
                                saved_positions += 1
                    else:
                        app.logger.warning("LINKEDIN - no positions found for user : %s", utilisateur.id)

                else:
                    app.logger.error("LINKEDIN - blank API response file for user : %s", utilisateur.id)

            elif api_req is None:
                app.logger.error("LINKEDIN - bad people API request for user : %s, null response", utilisateur.id)
            else:
                app.logger.error(
                    "LINKEDIN - bad people API request for user : %s, code : %s, request response : %s",
                    utilisateur.id,
                    api_req.status_code,
                    api_req.text
                )

    if import_success:
        flash("%s exp&eacute;riences import&eacute;es avec succ&egrave;s !" % saved_positions, "success")
    else:
        flash("Oups ! Il y a eu un probl&egrave;me pendant la connexion. Merci de contacter l'administrateur.", "error")

    return redirect(url_for("compte"))


def __get_linkedin_token(url):
    """
    Récupérer un token d'accès pour un utilisateur LinkedIn, et rediriger vers `url`

    Workflow de l'API LinkedIn :
    - User clique sur un lien vers LinkedIn, avec en paramètre une url de redirection (et un csrf token)
    - User s'authentifie et donne accès à cette application
    - LinkedIn redirige vers l'url de redirection fournie = l'authentification est réussie
        - Note : Flask conserve les paramètres de requêtes que LinkedIn a fournis, ils sont passés implicitement ici
    - Ensuite, on réclame un token d'accès, avec l'url de redirection en paramètre, en POSTant une requête
    - Dans la réponse, on obtient le token

    @note: pas sûr que redirection = authentification réussie ; il faudrait vérifier les codes ...
    @param url: l'url pour laquelle va être utilisé le token
    @return:
    """
    access_token = None
    if request.args.get('error') is None:
        state = request.args.get('state')
        code = request.args.get('code')
        if code is not None and state == session['_csrf_token']:
            linkedin_url = ("https://www.linkedin.com/uas/oauth2/accessToken?"
                            "grant_type=authorization_code"
                            "&code=%s"
                            "&redirect_uri=%s"
                            "&client_id=%s"
                            "&client_secret=%s" %
                            (code,
                             url,
                             app.config['LINKEDIN_KEY'],
                             app.config['LINKEDIN_SECRET']
                             ))
            req = requests.post(linkedin_url)
            app.logger.info(
                "LINKEDIN - Request for user : %s, request : %s",
                current_user.id, linkedin_url)
            if req.status_code == requests.codes.ok:
                access_token = req.json()['access_token']
            else:
                app.logger.error(
                    "LINKEDIN - bad access request for user : %s, code : %s, request response : %s",
                    current_user.id, req.status_code, req.json())
        else:
            app.logger.error(
                "LINKEDIN - CSRF or no code for user : %s, code : %s, token (LinkedIn state) : %s, should be : %s",
                current_user.id, code, state, session['_csrf_token'])
    else:
        app.logger.error(
            "LINKEDIN - error authorizing LinkedIn access for user : %s, errors : %s",
            current_user.id, request.args.get('error'))

    return access_token

def __get_positions(element):
    """
    Prend un etree.element et le parse pour en récupérer un  tableau de positions
    xsd :

    <positions total="">
        <position>
            <id>
            <title>
            <summary>
            <start-date>
                <year>
                <month>
            </start-date>
            <end-date>
                <year>
                <month>
            </end-date>
            <is-current>
            <company>
                <name>
            </coompany>
        </position>
    </positions>

    @param element: etree.element
    @return:
    """
    positions = []
    for e in element:
        position = dict()

        id_exp = e.find("id")
        position['id_experience_linkedin'] = __getNodeText(id_exp)

        title = e.find("title")
        position['position'] = __getNodeText(title)

        summary = e.find("summary")
        position['description'] = __getNodeText(summary)

        start_date = e.find("start-date")
        date_debut = None
        if start_date is not None:
            year =  start_date.find("year")
            month = start_date.find("month")
            if year is not None:
                mois = 1
                if month is not None:
                    mois = month.text
                date_debut = datetime(int(year.text), int(mois), 1)
        position['date_debut'] = date_debut

        end_date = e.find("end-date")
        date_fin = None
        if end_date is not None:
            year =  end_date.find("year")
            month = end_date.find("month")
            if year is not None:
                mois = 12
                if month is not None:
                    mois = month.text
                date_fin = datetime(int(year.text), int(mois), 1)
        position['date_fin'] = date_fin

        company = e.find("company")
        entreprise = None
        if company is not None:
            entreprise = company.find("name")
        position['entreprise'] = __getNodeText(entreprise)
        positions.append(position)
    return positions


def __getNodeText(nodeElement):
    """
    Helper pour récupérer le texte d'un etree s'il n'est pas nul
    @param nodeElement: etree.node
    @return: node.text
    """
    if nodeElement is not None:
        return nodeElement.text