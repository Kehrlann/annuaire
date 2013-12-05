# coding=utf-8
from annuaire_anciens import app, annuaire, user, helper
from uuid import uuid4
from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import LoginManager, current_user, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return user.find_user_by_id(user_id)


@app.route('/')
def home():
    return redirect(url_for('annuaire_view'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Méthode pour logguer un utilisateur (no shit) à partir de son adresse mail et son mot de pass
    GET  : afficher la page de login
    POST : valider les infos et logguer ou invalider les infos et réafficher la page de login
    @return:
    """
    form = user.login_form(request.form)

    if current_user.is_authenticated():
        return redirect(url_for('annuaire_view'))

    if request.method == 'POST' and form.validate():
        utilisateur = user.find_user_by_mail(form)
        if utilisateur is not None:
            app.logger.info("LOGIN - success %s, with id %s", form.mail.data, utilisateur.id)
            login_user(utilisateur)
            flash("Logged in successfully.")
            return redirect(url_for('annuaire_view'))
        else:
            flash("Erreur de connexion : mot de passe incorrect ou utilisateur inconnu", "error")
            app.logger.warning("LOGIN - fail %s", form.mail.data)
    return render_template('user/login.html', form=form)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """
    Vue d'enregistrement pour les nouveaux utilisateurs.

    GET :
    1/ L'utilisateur rentre une adresse mail @mines-paris.org / @mines-nancy.org / @mines-saint-etienne.org

    POST :
    1/ On vérifie que le form est valable (mots de passe corrects et égaux)
    2/ On vérifie qu'il existe bien un ancien pour cette adresse mail
        -> Si non, on ajoute une erreur dans le formulaire au niveau du mail "ancien inexistant", et on render la page
        -> Si oui -> 3
    3/ On cherche s'il existe déjà un utilisateur pour l'ancien trouvé
        -> Si oui, on redirige vers la page de login
        -> Si non -> 4
    4/ On cherche s'il existe déjà une inscription en cours pour l'ancien trouvé
        -> Si oui, on redirige vers la page de resend qui permet de renvoyer un mail d'activtation
        -> Si non -> 5
    5/ Jusqu'ici; on a trouvé un ancien, pas d'utilisateur et pas d'inscription
        a. On crée un code d'actvation
        b. On crée la préinscription
        c. On envoie le mail de confirmation
        d. On redirige vers la page de login

    @return:
    """
    form = user.registration_form(request.form)

    if current_user.is_authenticated():
        return redirect(url_for('annuaire_view'))

    if request.method == 'POST' and form.validate():
        app.logger.info("REGISTER - Trying to add user for %s", form.mail_ancien.data)
        ancien = annuaire.find_ancien_by_mail_asso(form.mail_ancien.data)
        if ancien is None:
            app.logger.warning("REGISTER - ancien not found for %s", form.mail_ancien.data)
            form.mail_ancien.errors.append("Il n'existe aucun ancien avec cette adresse mail")

        else:
            utilisateur = user.find_user_by_id_ancien(ancien['id_ancien'])
            if utilisateur is not None:
                flash("Un compte existe d&eacute;j&agrave; pour cet ancien !", "warning")
                app.logger.warning("REGISTER - double register for user with id %s", utilisateur.id)
                return redirect(url_for("login"))
            else:
                inscription = user.find_inscription_by_id_ancien(ancien['id_ancien'])
                if inscription is not None:
                    app.logger.warning("REGISTER - resend for ancien with id %s", ancien["id_ancien"])
                    return render_template("user/resend.html", id_ancien=ancien['id_ancien'])
                else:
                    code_activation = str(uuid4())
                    helper.send_activation_mail(ancien['mail_asso'], ancien['id_ancien'], code_activation)
                    user.create_preinscription(ancien['id_ancien'], form.password.data, code_activation)
                    flash("Succ&egrave;s : un mail d'activation vous sera envoy&eacute; prochainement", "success")
                    app.logger.info("REGISTER - created preinscription for ancien with id %s", ancien['id_ancien'])
                    return redirect(url_for("login"))

    return render_template('user/register.html', form=form)

@app.route('/renvoyer/<int:id_ancien>', methods=['GET'])
def resend(id_ancien):
    """
    Méthode pour renvoyer l'email de confirmation d'une inscription

    @param id_ancien: id_ancien de la préinscription à renvoyer par mail
    @return:
    """
    if id_ancien is not None:
        inscription = user.find_inscription_by_id_ancien(id_ancien)
        if inscription is not None:
            ancien = annuaire.find_ancien_by_id(id_ancien)
            code_activation = inscription['code_activation']
            helper.send_activation_mail(ancien['mail_asso'], id_ancien, code_activation)
            flash(
                "Succ&egrave;s : un mail d'activation vous sera envoy&eacute; prochainement",
                "success"
            )
            app.logger.info("RESEND - resend mail for ancien with id %s", ancien['id_ancien'])
        else:
            flash("Echec : aucune inscription trouv&eacute;e, "
            "veuillez contacter l'adminsitrateur pour plus d'information", "error")
            app.logger.error("RESEND - try resend but no preinscription found for ancien with id %s", id_ancien)
    else:
        flash("Echec : pas d'id ancien, "
            "veuillez contacter l'adminsitrateur pour plus d'information", "error")
        app.logger.error("RESEND - no id ancien")
    return redirect(url_for("login"))

@app.route('/activation/<int:id_ancien>/<code_activation>')
def activation(id_ancien, code_activation):
    """
    Valider la préinscription d'un utilisateur, puis rediriger vers la page de login

    @param id_ancien: l'id ancien associé, pour vérification (pas de collisions sur le uuid
    @param code_activation: le code d'activation
    @return:
    """
    if helper.is_valid_integer(id_ancien) and code_activation is not None and code_activation != "":
        inscription = user.find_inscription_by_id_ancien(id_ancien)
        if inscription is not None:
            if inscription['code_activation'] == code_activation:
                ancien = annuaire.find_ancien_by_id(id_ancien)
                user.validate_preinscription(inscription, ancien)
                flash(("Bienvenue %s ! Tu peux maintenant t'identifier" % ancien['prenom']), "success")
                app.logger.info("ACTIVATION - activated the account for ancien with id %s", id_ancien)
            else:
                flash("Code d'activation incorrect !", "error")
                app.logger.error(
                    "ACTIVATION - wrong code for ancien with id : %s, code : %s, should be : %s",
                    id_ancien,
                    code_activation,
                    inscription['code_activation']
                )
        else:
            flash("Pas de pr&eacute;inscription pour cet ancien ...", "error")
            app.logger.error("ACTIVATION - no inscription for ancien with id %s", id_ancien)
    else:
        flash("URL incorrecte, merci de contacter un admnistrateur si le probl&egrave;me persiste", "error")
        app.logger.error("ACTIVATION - no id or code, id : %s, code : %s", id_ancien, code_activation)

    return redirect(url_for("login"))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    app.logger.info("Logout user with id %s", current_user.id)
    logout_user()
    return redirect(url_for('login'))


@app.route("/test")
def osef():
    return redirect(url_for('login'))