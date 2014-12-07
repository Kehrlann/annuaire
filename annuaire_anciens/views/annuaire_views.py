# coding=utf-8
"""
    Vue relatives à l'annuaire.
"""

from annuaire_anciens import app, annuaire, ECOLES, PAYS
from flask import render_template
from annuaire_anciens.helper.security import csrf_exempt
from flask.ext.login import login_required


@app.route('/annuaire', methods=['GET'])
@csrf_exempt
@login_required
def annuaire_view():
    """
    Vue pour render l'annuaire. Permet de préparer le form à afficher sur la page et de render le template.

    :return:
    """
    annuaire_form = annuaire.SearchForm()
    annuaire_form.setEcole(ECOLES)
    annuaire_form.setPays(PAYS)

    return render_template('annuaire/annuaire.html',
        form = annuaire_form)


