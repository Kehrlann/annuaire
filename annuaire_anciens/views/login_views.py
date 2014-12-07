# coding=utf-8
from annuaire_anciens import app, annuaire, user, helper
from flask import abort, render_template, request, redirect, url_for, flash
from flask.ext.login import LoginManager, current_user, login_user, login_required, logout_user
import datetime as dt
from annuaire_anciens.helper.security import generate_signed_string_from_mail_and_date
import json

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "inscription"
DATETIME_FORMAT = "%Y%m%d%H%M"

@login_manager.user_loader
def load_user(user_id):
    return user.find_user_by_id(user_id)


# API READY
@app.route('/')
def root():
    return render_template('index.html')

# API READY
@app.route('/register', methods=['POST'])
def register():
    """
    Méthode pour enregistrer un nouvel utilisateur via ajax
    POST

    """

# LEGACY - TO BE REMOVED
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

    :return:
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
        utilisateur = user.find_user_by_mail(mail_ancien, actif_only=False)
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
                flash("&Eacute;chec lors de l'inscription. Merci de contacter l'administrateur", "danger")
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

    :param id_user: id_user de la préinscription à renvoyer par mail
    """
    if helper.is_valid_integer(id_user) is not None:
        utilisateur = user.find_user_by_id(id_user)
        if utilisateur is not None and not utilisateur.actif:
            signature = helper.generate_signed_string_from_mail(utilisateur.mail)
            helper.send_activation_mail(utilisateur.mail, signature)
            flash(
                "Succ&egrave;s : un mail d'activation te sera envoy&eacute; prochainement",
                "success"
            )
            app.logger.info("RESEND - resend mail for user with id %s", utilisateur.id)
        else:
            flash("Echec : aucune inscription trouv&eacute;e, "
            "merci de contacter l'adminsitrateur pour plus d'information", "danger")
            app.logger.error("RESEND - try resend but no utilisateur found for id %s", id_user)
    else:
        flash("Echec : pas d'id utilisateur, "
            "merci de contacter l'adminsitrateur pour plus d'information", "danger")
        app.logger.error("RESEND - no id user")
    return redirect(url_for("login"))

@app.route('/activation/<code_activation>')
def activation(code_activation):
    """
    Valider la préinscription d'un utilisateur, puis rediriger vers la page de login

    :param code_activation: le code d'activation
    :return:
    """
    if code_activation is not None and code_activation != "":
        try:
            mail = helper.unsing_string(code_activation)["mail"]
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
                  "contacter un admnistrateur si le probl&egrave;me persiste", "danger")
            app.logger.error(
                "ACTIVATION - critical error decoding activation_code. Exception : %s",
                e.__class__.__name__
            )
    return redirect(url_for("login"))


@app.route("/reset", methods=["GET", "POST"])
def reset_password():
    """
    Pour qu'un utilisateur met à jour son mot de passe oublié.
    L'ancien tape son adresse. Si un utilisateur existe, on génère
    une signature avec `itsdangerous`
    (voir :func:`helper.security.generate_signed_string_from_mail_and_date`)

    Cette signature contient :
    - Le mail de l'utilisateur
    - La date max d'utilisation de la signature
        - Heure UTC
        - Par défaut : utcnow() + 12h

    Cette signature "activation" est ensuite envoyée par mail,
    dans le lien https://truc.com/rest/<activation>

    Méthodes :
    - GET   :   afficher le formulaire
    - POST  :   submit le formulaire

    ATTENTION : le reset de mot de passe est donc stateless, et l'utilisateur
    peut utiliser le lien autant de fois qu'il le souhaite pendant ses 12h d'activité.
    """

    form = user.request_new_password_form()

    # Si c'est un POST, on traite le formulaire
    if request.method == "POST":

        form = user.request_new_password_form(request.form)

        # Validation du formulaire
        if form.validate():
            app.logger.info("REQUEST PASS RESET - START - updating pass for user with mail : %s", form.mail_ancien.data)

            mail_ancien = form.mail_ancien.data+form.domaine_ancien.data
            utilisateur_confirmed = user.find_user_by_mail(mail_ancien) is not None

            # Si l'utilisateur n'existe pas dans la base, on redirige vers
            # la page de création d'un compte, avec un message
            if not utilisateur_confirmed:
                flash(
                    "Il semblerait que cet utilisateur n'existe pas dans notre base de donn&eacute;es."
                    "<br>As-tu pens&eacute; &agrave; cr&eacute;er un compte ?",
                    "warning"
                )
                app.logger.error("REQUEST PASS RESET - FAIL - Not exist user with mail : %s", form.mail_ancien.data)
                return redirect(url_for("inscription"))

            # Si l'utilisateur existe, on lui envoie un mail
            # Et on redirige vers "login"
            else:


                # TODO : que se passe-t-il si l'envoi de mail fail ?
                date_max = dt.datetime.utcnow() + dt.timedelta(hours=12)
                signature = generate_signed_string_from_mail_and_date(mail_ancien, date_max.strftime(DATETIME_FORMAT))
                annuaire.helper.send_reset_password_mail(mail_ancien, signature)

                flash(
                    "Tu vas bient&ocirc;t recevoir un mail avec les instructions pour mettre"
                    " &agrave; jour ton mont de passe.",
                    "success"
                )
                app.logger.info("REQUEST PASS RESET - SUCCESS - updating pass for user with mail : %s", form.mail_ancien.data)

                return redirect(url_for("login"))


    return render_template(
        "user/password/request_new_password.html",
        form = form
    )


@app.route("/reset/<activation>", methods=["GET", "POST"])
def reset_password_activate(activation):
    """
    Vue qui correspond au lien envoyé dans l'e-mail de reset du password.

    Méthodes :
    - GET   :   Afficher le formulaire
    - POST  :   Submit et traitement du formulaire

    Dans tous les cas, on vérifie la validité de la signature :
    - On arrive à la lire
    - On arrive à extraire mail et date
    - Le mail existe dans notre user base
    - La date est inférieure à datetime.utcnow()

    Une fois la signature validée, on affiche ou on submit le formulaire.

    Si pas de code d'activation, le routing de Flask devrait rediriger vers
    :func:`reset_password()`, mais au cas où, on pète

    :param str activation:  Le code d'activation. Est créé + signé avec itsdangerous.
                            Contient les données de la forme suivante :
                            { "mail" : "user@provider.com", "date" : "yyyyMMddhhmm" }
    """

    form = user.create_new_password_form()
    if activation is not None and activation != "":
        app.logger.info("RESET PASS - Start")

        try:
            mail = helper.unsing_string(activation)["mail"]
            date = dt.datetime.strptime(helper.unsing_string(activation)["date"], DATETIME_FORMAT)
            utilisateur = user.find_user_by_mail(mail, actif_only=True)

            app.logger.info("RESET PASS - Trying reset for user : %s, with date (utc) : %s", mail, date)

            if utilisateur is not None and date > dt.datetime.utcnow():

                if request.method == "POST":
                    form = user.create_new_password_form(request.form)
                    if form.validate():
                        success = user.reset_password_by_id(utilisateur.id, form.new_password.data)

                        if not success:
                            flash("Oops ! Une erreur a eu lieu lors de la mise &agrave; jour de ton mot de passe... <br>"
                                  "Merci de relancer la proc&eacute;dure, ou de contacter un administrateur "
                                  "si le probl&egrave;me persiste", "danger")
                            app.logger.error("RESET PASS - FAIL - update fail fur user with id : %s", utilisateur.id)

                        else:
                            flash("Succ&egrave;s ! Ton mot de passe a &eacute;t&eacute; modifi&eacute;.",
                                  "success")
                            app.logger.warning("RESET PASS - FAIL - update fail fur user with id : %s", utilisateur.id)

                            return redirect(url_for('login'))



                return render_template(
                    "user/password/create_new_password.html",
                    activation=activation,
                    form=form
                )

            elif utilisateur is None:
                flash("Oops ! Ce code ne correspond à aucun utilisateur... <br>"
                      "Merci de relancer la proc&eacute;dure, ou de contacter un administrateur "
                      "si le probl&egrave;me persiste", "danger")
                app.logger.error("RESET PASS - FAIL - user does not exist, mail : %s", mail)

            elif date > dt.datetime.utcnow():
                flash("Oops ! Ce code est p&eacute;rim&eacute;... "
                      "Pour rappel, les codes ne sont valables que 12h. <br>"
                      "Merci de renvoyer une demande de mot de passe !", "warning")
                app.logger.error(
                    "RESET PASS - FAIL - The token is too old, for user %s ; "
                    "mail is %s ; max date (utc) is %s",
                    utilisateur.id,
                    mail,
                    date
                )


            else:
                raise Exception("Strange exception, you shouldn't be here ....")

        except Exception, e:
            flash("URL incorrecte, merci de relancer la proc&eacute;dure de changement de mot de passe, "
                  "ou de contacter un admnistrateur si le probl&egrave;me persiste", "danger")
            app.logger.error(
                "RESET PASS - critical error decoding activation_code. Exception : %s",
                e.__class__.__name__
            )

        return redirect(url_for("reset_password"))

    else:
        abort(405, "Page uniquement accessible avec un code d'activation")



@app.context_processor
def inject_auth():
    """
    Ajoute automatiquement une variable `user_is_auth` au contexte Jinja
    """
    admin = False
    auth = False
    if current_user.is_authenticated():
        auth = True
        admin = current_user.admin
    return dict(user_is_auth=auth, user_is_admin=admin)
