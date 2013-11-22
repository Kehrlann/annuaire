# coding=utf-8
from annuaire_anciens import app, helper, annuaire
from flask import render_template, request
from annuaire_anciens.helper.security import csrf_exempt
from helper import search_anciens
from flask import session
from flask.ext.login import current_user, login_required


@app.route('/annuaire', methods=['GET', 'POST'])
@csrf_exempt
@login_required
def annuaire_view():
    avance = False
    if request.args.get('type') == 'avance':
        avance = True
    search = search_anciens(request.form, 1, request.method == 'POST')
    pagination = search[0]
    results = search[1]
    annuaireForm = search[2]
    if request.method == 'POST':
        session['previous_search'] = request.form
    elif 'previous_search' in session:
        session.pop('previous_search')
    return render_template('annuaire/annuaire.html',
        form = annuaireForm,
        results = results,
        pagination = pagination,
        utilisateur = current_user,
        avance=avance)


@app.route('/anciens', methods=['GET'])
@app.route('/anciens/page/<int:page>', methods=['GET'])
@login_required
def tableau_anciens(page):
    search = search_anciens(None, page, True)
    pagination = search[0]
    results = search[1]
    return render_template('annuaire/_tableau_anciens.html',
        results = results,
        pagination = pagination)


@app.route('/autocomplete/nom', methods=['GET'])
@login_required
def autocomplete_nom():
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_nom_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result, True)
    return result

@app.route('/autocomplete/ville', methods=['GET'])
@login_required
def autocomplete_ville():
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_ville_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result, True)
    return result


@app.route('/autocomplete/entreprise', methods=['GET'])
@login_required
def autocomplete_entreprise():
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_entreprise_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result, True)
    return result


@app.route('/autocomplete/compte/ville', methods=['GET'])
@login_required
def autocomplete_ville_simple():
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_ville_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result)
    return result

@app.route('/autocomplete/compte/entreprise', methods=['GET'])
@login_required
def autocomplete_entreprise_simple():
    result = []
    if request.args.has_key('term'):
        query_result = annuaire.find_entreprise_autocomplete(request.args['term'])
        result = helper.result_proxy_to_json(query_result)
    return result

@app.route('/ancien/<int:id_ancien>')
@login_required
def ancien(id_ancien):
    # get data by id ancien
    ancien = annuaire.find_ancien_by_id(id_ancien)
    adresse = annuaire.find_adresse_by_id_ancien(id_ancien)
    experiences = annuaire.find_experience_by_id_ancien(id_ancien)
    # load page
    return render_template('annuaire/ancien.html', ancien=ancien, adresse=adresse,  experiences=experiences, utilisateur=current_user)

