# coding=utf-8
"""
    Vue relatives à l'administration
"""

from flask import url_for, redirect, abort, render_template, flash
from annuaire_anciens.helper.security import admin_required
from annuaire_anciens import app
import admin_api
import json

@app.route("/admin", methods=["GET"])
@admin_required
def admin():
    """
    Page centrale d'administration
    :return:
    """
    return render_template("admin/admin.html")

@app.route("/ancien/<int:id_ancien>/bloquer", methods=["GET"])
@admin_required
def bloquer(id_ancien):
    """
    Bloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à bloquer
    """
    try:
        success = json.loads(admin_api.bloquer_api(id_ancien))["succes"]
        if success:
            return redirect(url_for('ancien', id_ancien=id_ancien))
        else:
            abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")
    except:
        abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")


@app.route("/ancien/<int:id_ancien>/debloquer", methods=["GET"])
@admin_required
def debloquer(id_ancien):
    """
    Débloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à débloquer
    """
    try:
        success = json.loads(admin_api.debloquer_api(id_ancien))["succes"]
        if success:
            return redirect(url_for('ancien', id_ancien=id_ancien))
        else:
            abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")
    except:
        abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")