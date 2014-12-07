# coding=utf-8
from annuaire_anciens import app, user, helper, SUCCESS, FAILURE
from flask import request, abort
from flask.ext.login import current_user, login_user, login_required, logout_user
import json

@app.route('/api/v1/logged', methods=['GET'])
def logged():
    """
    Méthode legacy pour supporter l'url /login
    GET  : afficher l'annuaire si l'utilisateur est loggué, la page d'inscription sinon
    :return:
    """
    return json.dumps({ "logged" : current_user.is_authenticated()})


@helper.csrf_exempt
@app.route('/api/v1/login', methods=['POST'])
def login():
    """
    :return:    Réussite :  code 200 et { "success" : True }
                Echec :     code 401 si échec de l'authentification
    """
    form = request.form
    mail = form["mail"]
    password = form["password"]
    rememberMe = True if form.get("rememberme", None) != None else False
    utilisateur = user.find_user_by_mail_and_password(mail, password, actif_only=True)

    if utilisateur is not None:
        app.logger.info("LOGIN - success %s, with id %s", mail, utilisateur.id)
        app.logger.info("LOGIN - rememberme is %s", rememberMe)
        login_user(utilisateur, remember=rememberMe)
        return json.dumps(SUCCESS)
    else:
       app.logger.warning("LOGIN - fail %s", mail)
    abort(401)


@app.route('/api/v1/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Logout the user, duh.

    :return:    { "success": True }
    """
    app.logger.info("LOGOUT - user [%s : %s]", current_user.id, current_user.mail)
    logout_user()
    return json.dumps(SUCCESS)
