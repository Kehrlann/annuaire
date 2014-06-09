# coding=utf-8
from datetime import datetime
import os

from werkzeug.utils import secure_filename
from flask import render_template, request, url_for, redirect, session, flash, abort
from flask.ext.login import current_user, login_required, login_user
import requests
import json
from lxml import etree

from annuaire_anciens import app, annuaire, user, PAYS
from annuaire_anciens.helper.security import generate_csrf_token


@app.route('/me', methods=['GET'])
@login_required
def compte():
    """
    Permet, entre autres, d'associer un utilisateur à un ancien :
    - Si l'utilisateur U n'a pas d'ancien associé
        - Trouver si il y a un ancien A tel que A.mail_asso == U.mail
            - Si oui, vérifier qu'il n'y a pas d'utilisateur U2
            tel que U2.id_ancien == A.id_ancien
                - Si U2 n'existe pas, alors UPDATE U tel que U.id_ancien = A.id_ancien

    """

    #TODO : refaire les commentaires
    # chopper l'ancien associé à l'utilisateur
    utilisateur = user.find_user_by_id(current_user.id)

    # Trouver si l'utilisateur a un ancien associé
    ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)

    # Si l'utilisateur n'a pas d'ancien, on va vérifier
    # Via le mail asso, s'il existe un ancien dans la base pour lui
    if ancien is None:
        ancien_temp = annuaire.find_ancien_by_mail_asso(utilisateur.mail)

        # si il y a effectivement un ancien, vérifier
        # qu'il n'est pas déjà associé à un utilisateur
        if ancien_temp is not None:
            app.logger.info(
                "USER ASSOCIATION - trying to associate user %s with ancien %s",
                current_user.id,
                ancien_temp['id_ancien']
            )
            user_temp = user.find_user_by_id_ancien(ancien_temp['id_ancien'])

            # Si ça n'existe pas, alors faire l'association
            if user_temp is None:
                # On récupère le nouvel utilisateur
                sql_res = user.update_id_ancien(utilisateur.id, ancien_temp['id_ancien'])

                # Si l'association réussit
                # réucpérer l'ancien
                if sql_res :
                    utilisateur = user.find_user_by_id(utilisateur.id)
                    app.logger.info(
                        "USER ASSOCIATION - Success, associated user %s with ancien %s",
                        utilisateur.id,
                        ancien_temp['id_ancien']
                    )
                    return redirect(url_for("ancien", id_ancien=utilisateur.id_ancien))

                else:
                    app.logger.error(
                        "USER ASSOCIATION - Oops ... update went wrong."
                    )

            else:
                app.logger.warning(
                    "USER ASSOCIATION - user %s already associated with ancien %s",
                    user_temp.id,
                    ancien_temp['id_ancien']
                )

    else:
        return redirect(url_for("ancien", id_ancien=utilisateur.id_ancien))


@app.route('/ancien/<int:id_ancien>')
@login_required
def ancien(id_ancien):

    #TODO : commentaires
    is_this_me = False
    adresse_form = user.update_adresse_form()
    adresse_form.set_pays(PAYS)
    experience_forms = {}
    new_experience_form = None
    linkedin_url = None
    import_linkedin_url = None
    password_form = user.change_password_form()


    # get data by id ancien
    ancien = annuaire.find_ancien_by_id(id_ancien)
    adresse = annuaire.find_adresse_by_id_ancien(id_ancien)
    experiences = annuaire.find_experience_by_id_ancien(id_ancien).fetchall()

    for exp in experiences:
        form = user.update_experience_form()
        form.set_pays(PAYS)
        form.load_experience(exp)
        experience_forms[exp['experience_id_experience']] = form

    utilisateur = user.find_user_by_id(current_user.id)

    #~~~~~~~~~#
    # ADRESSE #
    #~~~~~~~~~#
    if utilisateur is not None and utilisateur.id_ancien == id_ancien:
        is_this_me = True

        adresse = annuaire.find_adresse_by_id_ancien(utilisateur.id_ancien)
        if adresse is not None:
            adresse_form.load_adresse(adresse)

    #~~~~~~~~~~~~~#
    # INFOS PERSO #
    #~~~~~~~~~~~~~#
    ancien_form = user.update_ancien_form()
    ancien_form.load_ancien(ancien)

    #~~~~~~~~~~~~~~~~~~#
    # AJOUT EXPERIENCE #
    #~~~~~~~~~~~~~~~~~~#
    if is_this_me:
        new_experience_form = user.update_experience_form()
        new_experience_form.set_pays(PAYS)


    #~~~~~~~~~~~~~~~~~~#
    # Gestion LinkedIn #
    #~~~~~~~~~~~~~~~~~~#
    if is_this_me:

        # Connexion à LinkedIn
        if ancien['url_linkedin'] is None:
            linkedin_url = ("https://www.linkedin.com/uas/oauth2/authorization?"
                                "response_type=code&"
                                "client_id=%s&"
                                "scope=%s"
                                "&state=%s"
                                "&redirect_uri=%s" %
                                (app.config['LINKEDIN_KEY'],
                                 app.config['LINKEDIN_SCOPE'],
                                 generate_csrf_token(),
                                 url_for('linkedin_associer', _external=True)))

        # import des expériences pro linkeding
        import_linkedin_url = ("https://www.linkedin.com/uas/oauth2/authorization?"
                            "response_type=code&"
                            "client_id=%s&"
                            "scope=%s"
                            "&state=%s"
                            "&redirect_uri=%s" %
                            (app.config['LINKEDIN_KEY'],
                             app.config['LINKEDIN_SCOPE'],
                             generate_csrf_token(),
                             url_for('linkedin_importer', _external=True)))



    # load page
    return render_template(
        'annuaire/ancien.html',
        ancien=ancien,
        adresse=adresse,
        ancien_form=ancien_form,
        adresse_form=adresse_form,
        experiences=experiences,
        utilisateur=current_user,
        editable=is_this_me,
        experience_forms=experience_forms,
        new_experience_form = new_experience_form,
        linkedin_url = linkedin_url,
        import_linkedin_url= import_linkedin_url,
        password_form = password_form
    )





@app.route('/compte/password/', methods=['POST'])
@login_required
def update_password():
    """
    Mettre à jour son mot de passe.

    Lors de la mise à jour, on vérifie que l'utilisateur connait bien le mot de passe actuel,
    afin d'éviter les reset par des tierces personnes sur des sessions ouvertes.

    POST : "commit" les données
    """
    res = {}
    res["content"] = None
    res["csrf_token"] = generate_csrf_token()
    res["success"] = False


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

            res["success"] = True
            return json.dumps(res)

        else:
            app.logger.error("UPDATE PASS - error changing password  for user with id %s", current_user.id)
            flash("Probl&egrave;me &agrave; la mise &agrave; jour, contacter l'administrateur", "danger")

    res["content"] = render_template('annuaire/profile/_password.html', password_form = form)


    return json.dumps(res)


@app.route('/compte/info/', methods=['POST'])
@login_required
def update_info_perso():
    """
    Page pour mettre à jour les infos perso d'un ancien.
        -> Infos perso
        -> Adresse perso

    Deux fois (adresse+infos) trois étapes :
        1. Valider les données
        2. Le cas échéant, les sauvegarder
        3. Regénérer le template et le renvoyer avec un nouveau csrf token
    """


    res = {}
    res["content"] = None
    res["csrf_token"] = generate_csrf_token()
    res["success"] = False

    form_ancien_to_render = None

    form = user.update_ancien_form()

    info_ok = False

    utilisateur = user.find_user_by_id(current_user.id)
    if utilisateur is not None:



        #~~~~~~~~~~~~~#
        # INFOS PERSO #
        #~~~~~~~~~~~~~#
        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)

        if ancien is not None:
            form.load_ancien(ancien)

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
                        "UPDATE INFO - successfully update info for user with id %s, id ancien : %s, errors : %s",
                        current_user.id,
                        ancien['id_ancien'],
                        )
                    info_ok = True

                else:
                    app.logger.info("UPDATE INFO - failed insert for user with id %s", current_user.id)

            else:
                form_ancien_to_render = form
                app.logger.info("UPDATE INFO - failed insert for user with id %s", current_user.id)


        #~~~~~~~~~#
        # ADRESSE #
        #~~~~~~~~~#
        adresse_form = user.update_adresse_form()
        adresse_form.set_pays(PAYS)

        if utilisateur.id_ancien is not None:
            adresse = annuaire.find_adresse_by_id_ancien(utilisateur.id_ancien)
            if adresse is not None:
                adresse_form.load_adresse(adresse)

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
                if info_ok:
                    flash("Informations personnelles mises &agrave; jour", "success")


        res["content"] = _get_info_perso_template(ancien_form=form_ancien_to_render)
        res["success"] = True

    return json.dumps(res)

@app.route('/compte/experience/', methods=['POST'])
@app.route('/compte/experience/<int:id_experience>', methods=['POST'])
@login_required
def update_experience(id_experience = None):
    """
    Page pour mettre à jour / ajouter des expériences pro d'un ancien

    POST : "commit" les données
    """

    id = id_experience

    res = {}
    res["content"] = None
    res["csrf_token"] = generate_csrf_token()
    res["success"] = False

    experience_form_to_render = None

    experience_form = user.update_experience_form()
    experience_form.set_pays(PAYS)

    utilisateur = user.find_user_by_id(current_user.id)

    if utilisateur.id_ancien is not None:

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

            id = annuaire.update_experience(
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

            res["success"] = True

        else:
            experience_form_to_render = experience_form

        if id_experience is not None:
            res["content"] = _get_experience_template(id, form=experience_form_to_render)
        else:
            res["content"] = _get_new_experience_template(experience_form_to_render)



    return json.dumps(res)



@app.route('/compte/photo/', methods=['POST'])
@login_required
def update_photo():
    """
    Mettre à jour la photo d'un ancien.

    POST :  on récupère la photo, on la sauvegarde, on vire l'ancienne
            et on re-render les infos persos (+ csrf token)

            Le cas de suppression est géré par un flag ?suppr=true dans
            l'url de la requête (bof bof ...)
    """

    utilisateur = user.find_user_by_id(current_user.id)

    res = {}
    res["content"] = None
    res["csrf_token"] = generate_csrf_token()
    res["success"] = False

    if utilisateur.id_ancien is None:
        return res
    else:
        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)
        if ancien is None:
            return res
        else:

            # récupérer le file uploadé
            uploaded_file = None
            try:
                uploaded_file = request.files['file']
            except:
                pass

            if request.form.get("suppr"):
                 # supprimer la photo dans la fiche ancien
                app.logger.info(
                    "PHOTO - remove for : %s",
                    ancien['id_ancien'])

                annuaire.update_photo(ancien['id_ancien'], None)

                # supression de l'ancienne photo
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ancien['photo'])))
                    app.logger.info(
                        "PHOTO - ancien : %s, removed file : %s",
                        ancien['id_ancien'],
                        ancien['photo']
                    )
                except:
                    app.logger.info(
                        "PHOTO - failed to remove for : %s",
                        ancien['id_ancien'])
                flash("Photo supprim&eacute;e", "warning")

            elif uploaded_file and _allowed_file(uploaded_file.filename):

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

            elif uploaded_file and not _allowed_file(uploaded_file.filename):
                app.logger.info(
                    "PHOTO - forbidden for ancien : %s, photo : %s",
                    ancien['id_ancien'],
                    uploaded_file.filename)
                flash("Format de photo invalide", "danger")


            res["content"] = _get_info_perso_template()
            res["success"] = True
    return json.dumps(res)


@app.route('/compte/experience/remove/<int:id_experience>', methods=['POST'])
@login_required
def remove_experience(id_experience):
    """
    Supprimer une expérience par id
    @param id_experience: id_experience de l'experience à supprimer.
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
def linkedin_associer():
    """
    Fonction de callback appelée par LinkedIn.
    Associer un compte ancien à un compte LinkedIn.

    Permet de :
    - Afficher le widget linkedin dans le profil de l'Ancien
    - Se connecter avec LinkedIn.

    Worfklow :
    - Request un token
    - Faire un appel sur l'API "people" pour obtenir l'id_linkedin et l'url du profil.
    - Récupérer ces données et les insérer en base
    """
    success = False
    utilisateur = user.find_user_by_id(current_user.id)
    app.logger.info(
            "LINKEDIN - begin authorize for ancien : %s, user : %s",
            utilisateur.id_ancien,
            utilisateur.id)

    if utilisateur.id_ancien is not None:
        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)
        if ancien is not None:
            access_token = __get_linkedin_token(url_for('linkedin_associer', _external=True))
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
        flash("Oups ! Il y a eu un probl&egrave;me pendant la connexion. Merci de contacter l'administrateur.", "danger")
    return redirect(url_for("compte"))


@app.route("/compte/linkedin/disconnect/", methods=['GET'])
@login_required
def linkedin_dissocier():
    """
    Virer l'association au compte linkedin d'un ancien
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
def linkedin_importer():
    """
    Fonction de callback appelée par LinkedIn.
    Importer les expériences depuis linkedin

    Worfklow :
    - Request un token
    - Faire un appel sur l'API "people" pour obtenir les "positions"
    - Récupérer ces données et les insérer en base

    Sujet ouvert :
    - Est-ce qu'on met à jour une position déjà existante (écraser)
    - Ou alors est-ce qu'on l'importe une deuxième fois ?
        -> Pour l'instant, on importe une deuxième fois
    """
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
            access_token = __get_linkedin_token(url_for('linkedin_importer', _external=True))
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
        flash("Oups ! Il y a eu un probl&egrave;me pendant la connexion. Merci de contacter l'administrateur.", "danger")

    return redirect(url_for("compte"))


@app.route("/linkedin/login", methods=['GET'])
def linkedin_login():
    """
    Fonction de callback appelée par LinkedIn.

    Log-in un membre à partir de LinkedIn.

    Worfklow :
    - Request un token
    - Faire un appel sur l'API "people" pour obtenir l'id_linkedin
    - Regarder si il existe un ancien avec cet id_linkedin
    - Regarder si il existe un utilisateur pour cet id_ancien
    - Logguer cet utilisateur !

    Notes :
    - On pourrait stocker les tokens pour ne pas avoir la demande systématique, mais ça veut dire modifier le workflow
    - Il faut penser à garder le "remember me", si on décide d'en faire une variable.
    """
    app.logger.info("LINKEDIN - begin login")

    access_token = __get_linkedin_token(url_for('linkedin_login', _external=True))
    api_url = "https://api.linkedin.com/v1/people/~:(id)?oauth2_access_token=%s" % access_token
    api_req =  requests.get(api_url)
    if api_req is not None and api_req.status_code == requests.codes.ok:
        parsed = etree.fromstring(api_req.text.encode("utf-8"))
        if parsed is not None:
            id_linkedin = None
            for e in parsed:
                if e.tag == "id":
                    id_linkedin = e.text
            if id_linkedin is not None:
                app.logger.info("LINKEDIN - search ancien for id id_linkedin : %s", id_linkedin)
                ancien = annuaire.find_ancien_by_id_linkedin(id_linkedin)
                if ancien is not None:
                    app.logger.info("LINKEDIN - found ancien with ID : %s", ancien['id_ancien'])
                    utilisateur = user.find_user_by_id_ancien(ancien['id_ancien'], actif_only=True)
                    if utilisateur is not None :
                        app.logger.info("LOGIN - linkedin login successful, with id %s",  utilisateur.id)
                        login_user(utilisateur, remember=True)
                        flash("Logged in successfully.")
                        return redirect(url_for('annuaire_view'))
                    else:
                        flash("Erreur de connexion : mot de passe incorrect ou utilisateur inconnu", "danger")
                        app.logger.warning("LOGIN - linkedin login failed for id_linkedin %s", id_linkedin)

                else:
                    app.logger.warning("LINKEDIN - no ancien for id_linkedin : %s", id_linkedin)

        else:
            app.logger.error("LINKEDIN - blank API response file")

    elif api_req is None:
        app.logger.error("LINKEDIN - bad people API request, null response")
    else:
        app.logger.error(
            "LINKEDIN - bad people API request ... code : %s, request response : %s",
            api_req.status_code,
            api_req.text
        )

    return redirect(url_for("login"))



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
    user_id = "Anonymous"
    if current_user.is_authenticated():
        user_id = current_user.id
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
                user_id, linkedin_url)
            if req.status_code == requests.codes.ok:
                access_token = req.json()['access_token']
            else:
                app.logger.error(
                    "LINKEDIN - bad access request for user : %s, code : %s, request response : %s",
                    user_id, req.status_code, req.json())
        else:
            app.logger.error(
                "LINKEDIN - CSRF or no code for user : %s, code : %s, token (LinkedIn state) : %s, should be : %s",
                user_id, code, state, session['_csrf_token'])
    else:
        app.logger.error(
            "LINKEDIN - error authorizing LinkedIn access for user : %s, errors : %s",
            user_id, request.args.get('error'))

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
        position['id_experience_linkedin'] = _getNodeText(id_exp)

        title = e.find("title")
        position['position'] = _getNodeText(title)

        summary = e.find("summary")
        position['description'] = _getNodeText(summary)

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
        position['entreprise'] = _getNodeText(entreprise)
        positions.append(position)
    return positions


def _getNodeText(nodeElement):
    """
    Helper pour récupérer le texte d'un etree s'il n'est pas nul
    @param nodeElement: etree.node
    @return: node.text
    """
    if nodeElement is not None:
        return nodeElement.text


def _allowed_file(filename):
    """
    Vérifier qu'un fichier est bien dans la liste des extensions autorisées.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



def _get_info_perso_template(ancien_form=None, adresse_form=None):
    """
    Permet de render le template _info_perso pour l'ancien en cours.

    @param adresse_form:    le formulaire d'adresse à inclure
    @param ancien_form:     le formulaire d'infos persos à inclure

    On prend des formulaires en entrée pour gérer les erreurs.


    NB: la modificaiton in-line des infos perso (sans page reload) ne
        permet plus de render des templates complets côté serveur. Plutôt
        que de réécrire l'intégralité de l'appli côté client, on render des
        templates partiels qu'on injecte dans la page sur des appels POST.

        Ce n'est pas super propre, mais c'est la vie :3
    """
    utilisateur = user.find_user_by_id(current_user.id)

    ancien = None
    adresse = None
    is_this_me = False

    if utilisateur is not None and utilisateur.id_ancien is not None:
        is_this_me = True

        ancien = annuaire.find_ancien_by_id(utilisateur.id_ancien)

        #~~~~~~~~~~~~~#
        # INFOS PERSO #
        #~~~~~~~~~~~~~#
        if ancien_form is None:
            ancien_form = user.update_ancien_form()
            ancien_form.load_ancien(ancien)

        #~~~~~~~~~#
        # ADRESSE #
        #~~~~~~~~~#
        if adresse_form is None:
            adresse_form = user.update_adresse_form()
            adresse_form.set_pays(PAYS)
            adresse = annuaire.find_adresse_by_id_ancien(utilisateur.id_ancien)
            if adresse is not None:
                adresse_form.load_adresse(adresse)

    else:
        if ancien_form is None:
            ancien_form = user.update_ancien_form()

        if adresse_form is None:
            adresse_form = user.update_adresse_form()
            adresse_form.set_pays(PAYS)


    return render_template(
        'annuaire/profile/_infos_perso.html',
        ancien=ancien,
        adresse=adresse,
        ancien_form=ancien_form,
        adresse_form=adresse_form,
        utilisateur=current_user,
        editable=is_this_me
    )


def _get_experience_template(id_experience, form = None):
    """
    Permet de render le template _experience_pro pour l'ancien en cours.

    :param id_experience:   l'id de l'expérience considérée
    :param form:            le formulaire d'expérience pro à inclure

    On prend des formulaires en entrée pour gérer les erreurs.


    NB: la modificaiton in-line des expériences pro (sans page reload) ne
        permet plus de render des templates complets côté serveur. Plutôt
        que de réécrire l'intégralité de l'appli côté client, on render des
        templates partiels qu'on injecte dans la page sur des appels POST.

        Ce n'est pas super propre, mais c'est la vie :3

        cf : _get_info_perso_template
    """
    utilisateur = user.find_user_by_id(current_user.id)

    experience = None
    is_this_me = False

    if utilisateur is not None and utilisateur.id_ancien is not None:
        is_this_me = True

        experience = annuaire.find_experience_by_id_ancien_id_experience(utilisateur.id_ancien, id_experience).first()

        if form is None:
            form = user.update_experience_form()
            form.load_experience(experience)

    else:
        # attention, on ne devrait jamais arriver ici
        if form is None:
            form = user.update_experience_form()

    form.set_pays(PAYS)

    return render_template(
        'annuaire/profile/_experience.html',
        exp=experience,
        form=form,
        utilisateur=current_user,
        editable=is_this_me
    )


def _get_new_experience_template(form):
    """
    Permet de render le template _new_experience_pro avec un formulaire donné

    :param form:
    :return:
    """
    if form is not None:
        return render_template(
            'annuaire/profile/_new_experience.html',
            new_experience_form = form,
            editable = True
        )
    else:
        return ""