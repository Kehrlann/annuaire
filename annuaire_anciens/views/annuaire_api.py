# coding=utf-8
"""
    Toutes les API relatives à l'utilisation de l'annuaire.
"""

from annuaire_anciens import app, helper
from search import search_fulltext, search_anciens
from flask import request, session
from flask.ext.login import login_required, current_user
import json
from urllib2 import unquote

@app.route('/api/v1/ancien', methods=['GET'])
@login_required
def fulltext_api():
    """
    API pour obtenir la liste des anciens sur une recherche fulltext

    Les paramètres sont dans la query string, et sont les suivants :
    - q : le texte à recherche (default : None)
    - p : la page (default : 1)

    :return:    Un objet contenant :
                    - max_pages : le nombre de pages maximum
                    - data : la liste des résultats sous forme d'objets JSON html-encodé de la forme
                        {
                            'id':           23154,
                            'prenom':       'J&eacute;r&ocirc;me',
                            'nom':          'Toto',
                            'ecole':        'P',
                            'promo':        2008,
                            'ville':        'COLOMBES',
                            'pays':         'FRANCE',
                            'code_postal':  '92700',
                            'entreprise':   'SNCF'
                        }
    """
    # 1. Obtenir les paramètres
    fulltext = request.args.get('q', None)
    if fulltext is not None:
        fulltext = unquote(fulltext)
    page = request.args.get('p', 1)


    # 2. Stocker la recherche pour l'afficher dans d'autres pages.
    if 'previous_search' in session:
        session.pop('previous_search')

    session['previous_fulltext'] = fulltext

    # 3. Effectuer la recherche
    s = search_fulltext(fulltext, int(page), current_user.admin)

    # 4. Mettre en forme les résultats
    results = []
    for ancien in s[1]:
        results.append(helper.row_to_json(ancien))

    to_send = { "current_page" : s[0].current, "max_pages" : s[0].last , "data" : results }

    # 5. Return
    return json.dumps(to_send)



@app.route('/api/v1/ancien/avance', methods=['GET'])
@login_required
def search_api():
    """
    API pour obtenir la liste des anciens sur une recherche avancée

    Les paramètres sont dans la query string, et sont les suivants :
    - prenom
    - nom
    - ecole
    - promo
    - ville
    - pays
    - entreprise
    - adresse
    - p : la page (default : 1)

    :return:    Un objet contenant :
                    - max_pages : le nombre de pages maximum
                    - data : la liste des résultats sous forme d'objets JSON html-encodé de la forme
                        {
                            'id':           23154,
                            'prenom':       'J&eacute;r&ocirc;me',
                            'nom':          'Toto',
                            'ecole':        'P',
                            'promo':        2008,
                            'ville':        'COLOMBES',
                            'pays':         'FRANCE',
                            'code_postal':  '92700',
                            'entreprise':   'SNCF'
                        }
    """

    # 1. Obtenir les paramètres
    page = request.args.get('p', 1)

    # 2. Stocker la recherche pour l'afficher dans d'autres pages.
    if 'previous_fulltext' in session:
        session.pop('previous_fulltext')

    session['previous_search'] = request.args

    # 3. Effectuer la recherche
    s = search_anciens(request.args, int(page), current_user.admin)

    # 4. Mettre en forme les résultats
    results = []
    for ancien in s[1]:
        results.append(helper.row_to_json(ancien))

    to_send = { "current_page" : s[0].current, "max_pages" : s[0].last , "data" : results }

    # 5. Return
    return json.dumps(to_send)