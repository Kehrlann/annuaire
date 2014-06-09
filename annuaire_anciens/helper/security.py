# coding=utf-8
"""
Module de sécurité.
Pour l'instant, permet de contrer les cross-site request forgery (CSRF) en créant un token unique à chaque requête.

CSRF : https://en.wikipedia.org/wiki/Cross-site_request_forgery
"""
from annuaire_anciens import app
from uuid import uuid4
from itsdangerous import URLSafeSerializer
from hashlib import sha256
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
            print "token should be", token, "but is", request.form.get('_csrf_token')
            abort(403)


def generate_signed_string_from_mail(mail):
    """
    Générer une string signée par itsdangerous à partir d'un mail

    @param mail: le mail à signer
    @return une string signée à utiliser en URL
    """
    signer_kwargs = { "digest_method" : sha256 }
    signer = URLSafeSerializer(app.secret_key, signer_kwargs=signer_kwargs)
    payload = { "mail" : mail }
    signature = signer.dumps(payload)
    return signature


def get_mail_from_signed_string(signed_string):
    """
    Récupérer le mail depuis une string signée

    @param signed_string: la string signée
    @returns: le mail caché dedans
    """
    signer_kwargs = { "digest_method" : sha256 }
    signer = URLSafeSerializer(app.secret_key, signer_kwargs=signer_kwargs)
    res = signer.loads(signed_string)
    return res['mail']


def generate_csrf_token():
    """
    Stocke un token dans la session, et renvoie ce même token
    @return:__csrf_token = str(uuid4())
    """
    if '_csrf_token' not in session:
        # random uuid ... est-ce que c'est safe ??
        session['_csrf_token'] = str(uuid4())
    return session['_csrf_token']

def get_fulltext_from_session():
    """
    Récupérer la recherche fulltext, depuis n'importe quelle page
    """
    result = ""
    if 'previous_fulltext' in session:
        result = session['previous_fulltext']
    return result

app.jinja_env.globals['csrf_token'] = generate_csrf_token
app.jinja_env.globals['previous_fulltext'] = get_fulltext_from_session