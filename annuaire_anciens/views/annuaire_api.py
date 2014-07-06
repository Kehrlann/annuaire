# coding=utf-8
from annuaire_anciens import app, helper
from annuaire_anciens.helper.security import csrf_exempt
from search import search_fulltext
from flask import request, session
from flask.ext.login import login_required
import json
from urllib2 import unquote

@app.route('/api/v1/ancien', methods=['GET'])
@csrf_exempt
@login_required
def fulltext_api():
    """
    API pour chopper les anciens sur une recherche fulltext

    Les paramètres sont dans la query string, et sont les suivants :
    - q : le texte à recherche (default : None)
    - p : la page (default : 1)

    :return: Une liste d'objets JSON html-encodé de la forme
    {
        'ancien_ecole':        'P',
        'ancien_promo':        2008,
        'entreprise_nom':      'SNCF',
        'ancien_id_ancien':     23154,
        'adresse_code':        '92700',
        'pays_nom':            'FRANCE',
        'ancien_nom':          'Toto',
        'ville_nom':           'COLOMBES',
        'ancien_prenom':       'J&eacute;r&ocirc;me'
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
    s = search_fulltext(fulltext, int(page))

    # 4. Mettre en forme les résultats
    results = []
    for ancien in s[1]:
        results.append(helper.row_to_json(ancien))
        print helper.row_to_json(ancien)

    # 5. Return
    return json.dumps(results)