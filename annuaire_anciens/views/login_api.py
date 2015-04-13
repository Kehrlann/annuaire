# coding=utf-8
from annuaire_anciens import app, user, helper, SUCCESS, FAILURE
from flask import request, abort
from flask.ext.login import current_user, login_user, login_required, logout_user, LoginManager
import json


login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = "inscription"

@login_manager.user_loader
def load_user(user_id):
    return user.find_user_by_id(user_id)

@app.route('/api/v1/logged', methods=['GET'])
def logged():
    """
    Méthode legacy pour supporter l'url /login
    GET  : afficher l'annuaire si l'utilisateur est loggué, la page d'inscription sinon
    :return:
    """
    return json.dumps({ "logged" : current_user.is_authenticated()})


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


@login_manager.unauthorized_handler
def unauthorized():
    abort(401, "Vous n'etes pas authentifie et n'avez pas acces a cette page ...")