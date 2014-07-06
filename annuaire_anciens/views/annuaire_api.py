# coding=utf-8
from annuaire_anciens import app, helper
from annuaire_anciens.helper.security import csrf_exempt
from search import search_fulltext
from flask import request
from flask.ext.login import login_required
import json


@app.route('/api/v1/ancien', methods=['GET'])
@csrf_exempt
@login_required
def get_anciens_fulltext():
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

    fulltext = request.args.get('q', None)
    page = request.args.get('p', 1)
    s = search_fulltext(fulltext, int(page))
    results = []
    for ancien in s[1]:
        results.append(helper.row_to_json(ancien))
        print helper.row_to_json(ancien)

    return json.dumps(results)

