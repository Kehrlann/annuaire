# coding=utf-8
"""
    Toutes les API se rapportant à l'administration
"""

from flask import abort, request
from annuaire_anciens.helper.security import admin_required, csrf_exempt
import json
from annuaire_anciens import app, annuaire, helper, user


@app.route("/api/v1/admin/ancien", methods=["GET"])
@admin_required
def ancien_api():
    """
    Bloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à bloquer
    """
    args = { "bloque" : request.args.get('bloque', None), "nouveau" : request.args.get('nouveau', None) }
    res = annuaire.find_ancien_filtres(**args)
    to_send = []
    champs_utilises = ["id_ancien", "nom", "prenom", "promo", "ecole", "mail_asso", "diplome"]
    for r in res:
        to_send.append(dict([(key, r[key]) for key in champs_utilises]))
    return json.dumps(to_send)


@app.route("/api/v1/admin/ancien/<int:id_ancien>/valider", methods=["PUT"])
@admin_required
def valider_ancien_api(id_ancien):
    """
    Valider un ancien.

    :param id_ancien: L'id de l'ancien à valider
    """
    if annuaire.update_ancien_valider(id_ancien):
        utilisateur = user.find_user_by_id_ancien(id_ancien)
        helper.send_fiche_activee_mail(utilisateur["mail"])
        return json.dumps({ "succes" : True })
    else:
        abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")



@app.route("/api/v1/admin/ancien/<int:id_ancien>/refuser", methods=["PUT"])
@admin_required
def refuser_ancien_api(id_ancien):
    """
    Refuser une fiche ancien : nouveau = False et bloque = True

    :param id_ancien: L'id de l'ancien à refuser
    """
    if annuaire.update_ancien_valider(id_ancien) and annuaire.update_ancien_bloque(id_ancien, True):
        return json.dumps({ "succes" : True })
    else:
        abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")




@app.route("/api/v1/admin/ancien/<int:id_ancien>/bloquer", methods=["PUT"])
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


@app.route("/api/v1/admin/ancien/<int:id_ancien>/debloquer", methods=["PUT"])
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


@app.route("/api/v1/admin/user/<int:id_user>/admin", methods=["PUT"])
@admin_required
def donner_admin_api(id_user):
    """
    Donner le status d'admin à un utilisateur. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à admin
    """
    if user.update_user_admin(id_user, admin=True):
        return json.dumps({ "succes" : True })
    else:
        abort(500, "Oops ! Probleme de mise a jour de l'utilisateur ...")


@app.route("/api/v1/admin/user/<int:id_user>/unadmin", methods=["PUT"])
@admin_required
def retirer_admin_api(id_user):
    """
    Donner le status d'admin à un utilisateur. Uniquement utilisable par les administrateurs.

    :param int id_user: L'id de l'ancien à un-admin
    """
    if user.update_user_admin(id_user, admin=False):
        return json.dumps({ "succes" : True })
    else:
        abort(500, "Oops ! Probleme de mise a jour de l'utilisateur ...")