# coding=utf-8
"""
    API relatives à l'utilsateur et à la gestion de son compte.
"""
from flask import request, session, abort
from flask.ext.login import current_user, login_required, login_user
import json

from annuaire_anciens import app, annuaire, user
from annuaire_anciens.helper.security import generate_csrf_token



@app.route("/api/v1/user/me", methods=["GET"])
@login_required
def user_info_api():
    """
    Obtenir toutes les infos relatives à l'utilisateur (notamment
    son id ancien associé).

    :return:
    """
    return json.dumps(
        {
            "id"            :   current_user.id,
            "id_ancien"     :   current_user.id_ancien,
            "mail"          :   current_user.mail
        }
    )

@app.route("/api/v1/ancien", methods=["POST"])
@login_required
def create_ancien_api(id_ancien):
    """
    Créer ma fiche ancien

    :param id_ancien:
    :return:
    """
    if current_user.id_ancien is None:
        abort(501, "Not implemented (yet) !")

    else:
        ancien = annuaire.find_ancien_by_id(current_user.id_ancien, actif=None, nouveau=None, bloque=None)

        if ancien is None:
            # TODO : Bug ....
            abort(500, "Nous n'avons pas trouvé ta fiche ancien."
                       "Si le problème persiste, merci de contacter les administrateurs.")

        elif ancien["nouveau"]:
            # TODO : en attente de validation ...
            # TODO : Quel code retour ?
            abort(400, "Ta fiche ancien est en attente de validation. Un mail te sera envoyé lors de la validation.")

        else:
            # TODO : duplicate
            # TODO : quel code retour ? 419 ?
            abort(419, "Tu as déjà une fiche ancien ! Tu ne peux pas en créer une seconde.")


@app.route("/api/v1/ancien/<int:id_ancien>", methods=["PUT"])
@login_required
def update_ancien_api(id_ancien):
    """
    Mettre à jour ma fiche ancien

    :param id_ancien:
    :return:
    """
    abort(501, "Not implemented (yet) !")


@app.route("/api/v1/ancien/<int:id_ancien>/adresse", methods=["PUT"])
@login_required
def update_ancien_api(id_ancien):
    """
    Mettre à jour mon adresse. C'est une interface unifiée, même
    si techniquement, l'adresse peut ne pas exister préalablement.

    :param id_ancien:
    :return:
    """
    abort(501, "Not implemented (yet) !")



@app.route("/api/v1/ancien/<int:id_ancien>/experience", methods=["POST"])
@login_required
def add_experience_api(id_ancien):
    """
    Ajouter une expérience à un ancien

    :param id_ancien:
    :return:
    """
    abort(501, "Not implemented (yet) !")



@app.route("/api/v1/ancien/<int:id_ancien>/experience/<int:id_experience>", methods=["PUT"])
@login_required
def update_experience_api(id_ancien, id_experience):
    """
    Modifier une expérience

    :param id_ancien:
    :return:
    """
    abort(501, "Not implemented (yet) !")



@app.route("/api/v1/ancien/<int:id_ancien>/experience/<int:id_experience>", methods=["DELETE"])
@login_required
def delete_experience_api(id_ancien, id_experience):
    """
    Effacer une expérience

    :param id_ancien:
    :return:
    """
    abort(501, "Not implemented (yet) !")



def _is_this_me(id_ancien):
    """
    Vérifier que l'ancien modifié est bien l'ancien
    qui fait le call ...

    Sinon, abort avec une 403 Forbidden

    :param int id_ancien:   L'id de l'ancien en question
    :return:                Abort si illegal, None si autre
    """
    if current_user.id_ancien != id_ancien:
        abort(403, "Tu n'as pas le droit de modifier la fiche d'un autre ancien !")


def _is_not_blocked(ancien):
    """
    Vérifier que l'ancien modifié n'est pas bloqué ....

    Sinon, abort avec une 403 Forbidden

    :param int id_ancien:   L'id de l'ancien en question
    :return:                Abort si illegal, None si autre
    """
    if ancien is not None and ancien["bloque"]:
        # TODO : bloqué
        # TODO : quel code retour ?
        abort(403, "Il semblerai que tu compte soit bloqué."
                   "Merc")
