# coding=utf-8
from annuaire_anciens import app, helper, annuaire, ECOLES, PAYS
from flask import render_template, request
from annuaire_anciens.helper.security import csrf_exempt
from search import search_anciens, search_fulltext
from flask import session
from flask.ext.login import current_user, login_required


@app.route('/annuaire', methods=['GET', 'POST'])
@csrf_exempt
@login_required
def annuaire_view():
    avance = False
    fulltext = False
    if request.args.get('type') == 'avance':
        avance = True
    elif request.args.get('type') == 'fulltext':
        fulltext = True

    annuaire_form = annuaire.SearchForm()
    annuaire_form.setEcole(ECOLES)
    annuaire_form.setPays(PAYS)

    # recherche "normale" : construction du formulaire puis recherche
    if not fulltext:
        if 'previous_fulltext' in session:
            session.pop('previous_fulltext')

        if request.method == 'POST':
            session['previous_search'] = request.form
        elif 'previous_search' in session:
            session.pop('previous_search')

        s = search_anciens(request.form, 1)
        pagination = s[0]
        results = s[1]
        annuaire_form = s[2]

    # recherche "fulltext" : recherche brute
    else:
        if 'previous_search' in session:
            session.pop('previous_search')

        if request.method == 'POST':
            session['previous_fulltext'] = request.form.get("fulltext")
        elif 'previous_fulltext' in session:
            session.pop('previous_fulltext')

        s = search_fulltext(request.form.get("fulltext"), 1)
        pagination = s[0]
        results = s[1]


    return render_template('annuaire/annuaire.html',
        form = annuaire_form,
        results = results,
        pagination = pagination,
        utilisateur = current_user,
        avance=avance)


@app.route('/anciens', methods=['GET'])
@app.route('/anciens/page/<int:page>', methods=['GET'])
@login_required
def tableau_anciens(page):
    if 'previous_search' in session:
        s = search_anciens(None, page)
    elif 'previous_fulltext' in session:
        s = search_fulltext(None, page)
    else:
        s = [None, []]
    pagination = s[0]
    results = s[1]
    return render_template('annuaire/_tableau_anciens.html',
        results = results,
        pagination = pagination)


@app.route('/autocomplete/nom', methods=['GET'])
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

@app.route('/autocomplete/ville', methods=['GET'])
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


@app.route('/autocomplete/entreprise', methods=['GET'])
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


@app.route('/autocomplete/compte/ville', methods=['GET'])
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

@app.route('/autocomplete/compte/entreprise', methods=['GET'])
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

@app.route('/autocomplete/fulltext', methods=['GET'])
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

