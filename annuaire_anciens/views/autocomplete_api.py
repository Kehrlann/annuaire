# coding=utf-8
"""
    API utilisées dans des autocompletes (noms, villes, entreprises, etc)
"""


from annuaire_anciens import app, helper, annuaire
from flask import request
from flask.ext.login import login_required


@app.route('/api/v1/autocomplete/nom', methods=['GET'])
@login_required
def autocomplete_nom():
    """
    Autocomplete sur le nom. Utilise le plugin jquery-ui "autocomplete"

    La requête est faite dans le querystring avec term=<le_nom_recherché>

    :return: Liste de noms, au format JSON , avec double quotes
    """
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_nom_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result, True)
    return result

@app.route('/api/v1/autocomplete/ville', methods=['GET'])
@login_required
def autocomplete_ville():
    """
    Autocomplete sur le nom d'une ville. Utilise le plugin jquery-ui "autocomplete"

    La requête est faite dans le querystring avec term=<la_ville>

    :return: Liste de noms de villes, au format JSON
    """
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_ville_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result, True)
    return result


@app.route('/api/v1/autocomplete/entreprise', methods=['GET'])
@login_required
def autocomplete_entreprise():
    """
    Autocomplete sur le nom d'une entreprise. Utilise le plugin jquery-ui "autocomplete"

    La requête est faite dans le querystring avec term=<l_entreprise>

    :return: Liste de noms d'entreprises, au format JSON, avec double quotes
    """
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_entreprise_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result, True)
    return result


@app.route('/api/v1/autocomplete/compte/ville', methods=['GET'])
@login_required
def autocomplete_ville_simple():
    """
    Autocomplete sur le nom d'une ville. Utilise le plugin jquery-ui "autocomplete"

    La requête est faite dans le querystring avec term=<la_ville>

    :return: Liste de noms de villes, au format JSON, sans double quotes
    """
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_ville_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result)
    return result

@app.route('/api/v1/autocomplete/compte/entreprise', methods=['GET'])
@login_required
def autocomplete_entreprise_simple():
    """
    Autocomplete sur le nom d'une entreprise. Utilise le plugin jquery-ui "autocomplete"

    La requête est faite dans le querystring avec term=<l_entreprise>

    :return: Liste de noms d'entreprises, au format JSON, sans double quotes
    """
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_entreprise_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result)
    return result

@app.route('/api/v1/autocomplete/fulltext', methods=['GET'])
@login_required
def autocomplete_fulltext():
    """
    Autocomplete sur la liste de tous les mots dans l'annuaire. Permet de trouver des anciens
    grâce à une recherche fulltext, en suggérant des mots (nom de ville, nom d'ancien, nom d'entreprise ...)

    La requête est faite dans le querystring avec term=<mot>

    :return: Liste de noms de mots, au format JSON
    """
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_mot_autocomplete(request.args['term'], limit=5)
        result = helper.result_proxy_to_json(query_result)
    return result