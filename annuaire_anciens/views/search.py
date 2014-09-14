# coding=utf-8
from flask import session
from werkzeug.datastructures import MultiDict
from annuaire_anciens import helper, annuaire, ECOLES, PAYS

def search_anciens(request_values=None, page=1, admin=False):
    """
    pour effectuer une recherche

    :rtype: list
    :return: [pagination, results, annuaire_form]
    """
    results = []
    pagination = None

    # Affichage de TOUS les anciens pour l'admin
    kwargs = {}
    if admin:
        kwargs = { "actif" : None, "bloque" : None }

    # remplissage du formulaire
    if request_values is not None:
        annuaire_form = annuaire.form.SearchForm(request_values)
    else:
        if 'previous_search' in session:
            d = MultiDict(session['previous_search'])
            annuaire_form = annuaire.form.SearchForm(d)
            request_values = d
        else:
            annuaire_form = annuaire.form.SearchForm()
        # ajout des ecoles dans la dropdown
    annuaire_form.setEcole(ECOLES)
    annuaire_form.setPays(PAYS)

    ecole = request_values.get("ecole", '')
    pays = request_values.get("pays", '')
    annuaire_form.pays.data = pays
    annuaire_form.ecole.data = ecole

    # si POST d'un formulaire valide + user logged : count
    if annuaire_form.validate():

        # comptage des resultats, preparation de la pagination
        count = annuaire.count_annuaire_search(annuaire_form, **kwargs)
        pagination = helper.Pagination(count, 100)
        pagination.current = page

        # recherche sur la page
        results = annuaire.annuaire_search(annuaire_form, pagination.offset, pagination.limit, **kwargs)

    return pagination, results, annuaire_form


def search_fulltext(search_terms=None, page=1, admin=False):
    """
    Effectuer une recherche fullsearch
    :return: [pagination, results]
    """
    results = []
    pagination = None

    # Affichage de TOUS les anciens pour l'admin
    kwargs = {}
    if admin:
        kwargs = { "actif" : None, "bloque" : None }

    if (search_terms is None or search_terms == "") and 'previous_fulltext' in session:
        search_terms = session['previous_fulltext']

    # remplissage du formulaire
    # comptage des resultats, preparation de la pagination
    count = annuaire.count_fulltext(search_terms, **kwargs)
    pagination = helper.Pagination(count, 100)
    pagination.current = page

    # recherche sur la page
    results = annuaire.fulltext_search(search_terms, pagination.offset, pagination.limit, **kwargs)

    return pagination, results
