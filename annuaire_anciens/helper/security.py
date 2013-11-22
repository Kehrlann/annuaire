# coding=utf-8
"""
Module de sécurité.
Pour l'instant, permet de contrer les cross-site request forgery (CSRF) en créant un token unique à chaque requête.

CSRF : https://en.wikipedia.org/wiki/Cross-site_request_forgery
"""
from annuaire_anciens import app
from uuid import uuid4
from flask import request
from flask import session, abort

_exempt_views = []

def csrf_exempt(view):
    """
    Décorateur à appliquer pour se débarasser des protections CSRF
    """
    _exempt_views.append(view)
    return view

@app.before_request
def csrf_protect():
    """
    Pre-process les requêtes POST. On récupère la valeur de _csrf_token et on la compare à la valeur stockée dans
    la session.

    @raise: abort(403) unauthorized si on détecte une csrf
    @return: None if okay
    """
    destination_view = app.view_functions.get(request.endpoint)
    exempt = destination_view in _exempt_views
    if request.method == "POST" and not exempt:
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    """
    Stocke un token dans la session, et renvoie ce même token
    @return:__csrf_token = str(uuid4())
    """
    if '_csrf_token' not in session:
        # random uuid ... est-ce que c'est safe ??
        session['_csrf_token'] = str(uuid4())
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token