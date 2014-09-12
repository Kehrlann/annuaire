# coding=utf-8
"""
    Vue relatives à l'administration
"""

from flask import request, url_for, redirect, abort
from flask.ext.login import current_user, login_required

from annuaire_anciens import app, annuaire

@app.route("/ancien/<int:id_ancien>/bloquer", methods=["GET"])
@login_required
def bloquer(id_ancien):
    """
    Bloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à bloquer
    """
    if current_user.admin:
        if annuaire.update_ancien_bloque(id_ancien, bloque=True):
            return redirect(url_for('ancien', id_ancien=id_ancien))
        else:
            abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")
    else:
        app.logger.error("BLOCK - FAIL - Illegal blocking attempt."
                         "Id ancien : %s, id user : %s, mail user : %s",
                         id_ancien, current_user.id, current_user.mail)
        abort(403, "Seuls les administrateurs peuvent bloquer ou debloquer un ancien ! "
                   "L'incident a ete enregistre et sera transmis aux "
                   "administrateurs.")


@app.route("/ancien/<int:id_ancien>/debloquer", methods=["GET"])
@login_required
def debloquer(id_ancien):
    """
    Débloquer un ancien. Uniquement utilisable par les administrateurs.

    :param int id_ancien: L'id de l'ancien à débloquer
    """
    if current_user.admin:
        if annuaire.update_ancien_bloque(id_ancien, bloque=False):
            return redirect(url_for('ancien', id_ancien=id_ancien))
        else:
            abort(500, "Oops ! Probleme de mise a jour de l'ancien ...")
    else:
        app.logger.error("BLOCK - FAIL - Illegal unblocking attempt."
                         "Id ancien : %s, id user : %s, mail user : %s",
                         id_ancien, current_user.id, current_user.mail)
        abort(403, "Seuls les administrateurs peuvent bloquer ou debloquer un ancien ! "
                   "L'incident a ete enregistre et sera transmis aux "
                   "administrateurs.")