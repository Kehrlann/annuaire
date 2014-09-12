# coding=utf-8
"""
    Toutes les API se rapportant à l'administration
"""

from flask import url_for, redirect, abort
from annuaire_anciens.helper.security import admin_required
import json
from annuaire_anciens import app, annuaire

@app.route("/api/v1/ancien/<int:id_ancien>/bloquer", methods=["PUT"])
@admin_required
def bloquer_api(id_ancien):
    """
    Bloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à bloquer
    """
    if annuaire.update_ancien_bloque(id_ancien, bloque=True):
        return json.dumps({ "succes" : True })
    else:
        abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")


@app.route("/api/v1/ancien/<int:id_ancien>/debloquer", methods=["PUT"])
@admin_required
def debloquer_api(id_ancien):
    """
    Débloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à débloquer
    """
    if annuaire.update_ancien_bloque(id_ancien, bloque=False):
        return json.dumps({ "succes" : True })
    else:
        abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")