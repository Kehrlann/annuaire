# coding=utf-8
from annuaire_anciens import app, annuaire, user, helper
from flask import abort, render_template, request, redirect, url_for, flash
from flask.ext.login import LoginManager, current_user, login_user, login_required, logout_user
from itsdangerous import BadData, BadSignature

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "inscription"

@login_manager.user_loader
def load_user(user_id):
    return user.find_user_by_id(user_id)


@app.route('/')
def home():
    return redirect(url_for('annuaire_view'))

@helper.csrf_exempt
@app.route('/login', methods=['POST'])
def login_ajax():
    """
    Méthode pour logguer un utilisateur (no shit) à partir de son adresse mail et son mot de pass
    POST : valider les infos et logguer ou invalider les infos et retourner l'url sur lequel rediriger
    @return: code 401 si échec de l'authentification, code 200 et url en cas de réussite
    """
    form = user.login_form(request.form)

    if current_user.is_authenticated():
        return url_for('annuaire_view')

    if form.validate():
        utilisateur = user.find_user_by_mail_and_password(form.mail.data, form.password.data, actif_only=True)
        app.logger.info("LOGIN - valid form")
        if utilisateur is not None:
            app.logger.info("LOGIN - success %s, with id %s", form.mail.data, utilisateur.id)
            # app.logger.info("LOGIN - rememberme is %b", form.rememberme.data)
            login_user(utilisateur, remember=form.rememberme.data)
            return url_for('annuaire_view')
        else:
            app.logger.warning("LOGIN - fail %s", form.mail.data)
    abort(401)

@app.route('/login', methods=['GET'])
def login():
    """
    Méthode legacy pour supporter l'url /login
    GET  : afficher l'annuaire si l'utilisateur est loggué, la page d'inscription sinon
    @return:
    """
    if current_user.is_authenticated():
        return redirect(url_for('annuaire_view'))
    else:
        return redirect(url_for('inscription'))


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """
    Vue d'enregistrement pour les nouveaux utilisateurs.

    GET :
    1/  Page d'accueil qui permet de se logguer ou créer un utilisateur.
        On peut se logguer via son compte ou via LinkedIn.
    2/  Si l'utilisateur veut créer un compte, il rentre une adresse
        adresse mail @mines-paris.org / @mines-nancy.org / @mines-saint-etienne.org
        ainsi qu'un mot de passe.

    POST :
    1/ On vérifie que le form est valable (mots de passe corrects et égaux)
    2/ On cherche s'il existe déjà un utilisateur pour l'ancien trouvé
        -> Si oui
        2.1/ Si il existe déjà un utilisateur ACTIF, alors annuler l'inscription
        2.2/ Si il existe déjà un utilisateur INACTIF, rediriger vers resend
        -> Si non -> 3
    3/ Création de l'inscription
        a. On crée la string signée à envoyer
        b. On crée l'utilisateur
        c. On envoie le mail de confirmation
        d. On redirige vers la page de login

    @return:
    """
    form = user.registration_form(request.form)

    if current_user.is_authenticated():
        return redirect(url_for('annuaire_view'))

    if request.method == 'POST' and form.validate():

        # Chargement des infos du form
        mail_ancien = form.mail_ancien.data+form.domaine_ancien.data
        password = form.password.data
        app.logger.info("REGISTER - Trying to add user for %s", mail_ancien)

        # Gestion des utilisateurs : si un compte existe déjà, le signaler
        utilisateur = user.find_user_by_mail(mail_ancien)
        if utilisateur is not None:

            if utilisateur.actif:
                # Un compte actif existe déjà = interdit d'en re-créer un
                flash("Un compte existe d&eacute;j&agrave; pour cet ancien !", "warning")
                app.logger.warning("REGISTER - double register for user with id %s", utilisateur.id)
                return redirect(url_for("login"))
            else:
                # un compte incatif existe déjà = renvoyer le mail de validation
                app.logger.warning("REGISTER - resend for utilisateur with id %s", utilisateur.id)
                return render_template("user/resend.html", id_utilisateur=utilisateur.id)

        else:

            # Signature du mail user
            signature = helper.generate_signed_string_from_mail(mail_ancien)

            # Création de l'utilisateur
            if user.create_user(mail_ancien, password):

                # Envoi du mail
                annuaire.helper.send_activation_mail(mail_ancien, signature)

                flash("Succ&egrave;s : un mail d'activation vous sera envoy&eacute; prochainement", "success")
                app.logger.info("REGISTER - created preinscription user with mail %s", mail_ancien)
                return redirect(url_for("login"))

            else:
                flash("&Eacute;chec lors de l'inscription. Merci de contacter l'administrateur", "error")
                app.logger.error("REGISTER - problème à la création de l'utilisateur : %s", mail_ancien)
                return redirect(url_for("login"))


    linkedin_url = ("https://www.linkedin.com/uas/oauth2/authorization?"
                        "response_type=code&"
                        "client_id=%s&"
                        "scope=%s"
                        "&state=%s"
                        "&redirect_uri=%s" %
                        (app.config['LINKEDIN_KEY'],
                         'r_basicprofile',
                         helper.generate_csrf_token(),
                         url_for('linkedin_login', _external=True)))
    return render_template('user/register.html', form=form, linkedin_url=linkedin_url)




@app.route('/renvoyer/<int:id_user>', methods=['GET'])
def resend(id_user):
    """
    Méthode pour renvoyer l'email de confirmation d'une inscription

    @param id_user: id_user de la préinscription à renvoyer par mail
    """
    if helper.is_valid_integer(id_user) is not None:
        utilisateur = user.find_user_by_id(id_user)
        if utilisateur is not None and not utilisateur.actif:
            signature = helper.generate_signed_string_from_mail(utilisateur.mail)
            helper.send_activation_mail(utilisateur.mail, signature)
            flash(
                "Succ&egrave;s : un mail d'activation vous sera envoy&eacute; prochainement",
                "success"
            )
            app.logger.info("RESEND - resend mail for user with id %s", utilisateur.id)
        else:
            flash("Echec : aucune inscription trouv&eacute;e, "
            "veuillez contacter l'adminsitrateur pour plus d'information", "error")
            app.logger.error("RESEND - try resend but no utilisateur found for id %s", id_user)
    else:
        flash("Echec : pas d'id utilisateur, "
            "veuillez contacter l'adminsitrateur pour plus d'information", "error")
        app.logger.error("RESEND - no id user")
    return redirect(url_for("login"))

@app.route('/activation/<code_activation>')
def activation(code_activation):
    """
    Valider la préinscription d'un utilisateur, puis rediriger vers la page de login

    @param code_activation: le code d'activation
    @return:
    """
    if code_activation is not None and code_activation != "":
        try:
            mail = helper.get_mail_from_signed_string(code_activation)
            utilisateur = user.find_user_by_mail(mail, actif_only=False)
            if utilisateur is not None and not utilisateur.actif:
                if user.activate_user(utilisateur.id):
                    flash(("Bienvenue %s ! Tu peux maintenant t'identifier" % utilisateur.mail), "success")
                    app.logger.info("ACTIVATION - activated the account for utilisateur with id %s", utilisateur.id)
                else:
                    flash(("Oups ... Erreur d'activation. Merci de contacter l'adminsitrateur."), "success")
                    app.logger.info("ACTIVATION - error activating  the account for user with id %s", utilisateur.id)

        except Exception, e:
            flash("URL incorrecte, merci de relancer la proc&eacute;dure d'inscription ou de "
                  "contacter un admnistrateur si le probl&egrave;me persiste", "error")
            app.logger.error(
                "ACTIVATION - critical error decoding activation_code. Exception : %s",
                e.__class__.__name__
            )


    return redirect(url_for("login"))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Logout the user, duh.
    """
    app.logger.info("Logout user with id %s", current_user.id)
    logout_user()
    return redirect(url_for('login'))


@app.context_processor
def inject_auth():
    """
    Ajoute automatiquement une variable `user_is_auth` au contexte Jinja
    """
    return dict(user_is_auth=current_user.is_authenticated())