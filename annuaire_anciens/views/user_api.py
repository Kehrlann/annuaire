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

@app.route("/api/v1/me/ancien", methods=["POST"])
@login_required
def create_ancien_api():
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
            abort(500, "Nous n'avons pas trouve ta fiche ancien."
                       "Si le probleme persiste, merci de contacter les administrateurs.")

        elif ancien["nouveau"]:
            # TODO : en attente de validation ...
            # TODO : Quel code retour ?
            abort(400, "Ta fiche ancien est en attente de validation. Un mail te sera envoye lors de la validation.")

        else:
            # TODO : duplicate
            # TODO : quel code retour ? 419 ?
            abort(419, "Tu as deja une fiche ancien ! Tu ne peux pas en creer une seconde.")


@app.route("/api/v1/me", methods=["PUT"])
@login_required
def update_ancien_api():
    """
    Mettre à jour ma fiche ancien.

    Input (JSON):
    {
        "telephone"     :   str ,
        "mobile"        :   str ,
        "site"          :   str ,
        "mail_perso"    :   str
    }

    Tous les champs sont optionnels.

    :return:    { "succes"  :   true/false  }
    """
    ancien  =   _get_valid_ancien()
    data    =   _get_valid_data()

    succes = annuaire.update_fiche_ancien(
        id_ancien   =   ancien["id_ancien"],
        telephone   =   data.get("telephone",   ancien["telephone"]),
        mobile      =   data.get("mobile",      ancien["mobile"]),
        site        =   data.get("site",        ancien["site"]),
        mail_perso  =   data.get("mail_perso",  ancien["mail_perso"])
    )

    return json.dumps({"succes":succes})


@app.route("/api/v1/me/adresse", methods=["PUT"])
@login_required
def update_adresse_api():
    """
    Mettre à jour mon adresse. C'est une interface unifiée, même
    si techniquement, l'adresse peut ne pas exister préalablement.

    Input (JSON) :
    {
        "ville"         :   str ,
        "id_pays"       :   int ,
        "adresse"       :   str ,
        "code"          :   str
    }

    :return:    { "succes"  :   true/false  }
    """
    ancien  =   _get_valid_ancien()
    data    =   _get_valid_data()

    succes  =   annuaire.update_adresse_perso(
        id_ancien   =   ancien["id_ancien"],
        ville       =   data.get("ville",       ""),
        id_pays     =   data.get("id_pays",     None),
        adresse     =   data.get("adresse",     ""),
        code        =   data.get("code",        "")
    )

    return json.dumps({"succes":succes})



@app.route("/api/v1/me/experience", methods=["POST"])
@login_required
def add_experience_api():
    """
    Ajouter une expérience à un ancien.

    Input (JSON) :
    {
        "id_experience"     :   int             ,
        "ville"             :   str             ,
        "id_pays"           :   int             ,
        "adresse"           :   str             ,
        "code"              :   str             ,
        "entreprise"        :   str             ,
        "poste"             :   str             ,
        "description"       :   str             ,
        "mail"              :   str             ,
        "site"              :   str             ,
        "telephone"         :   str             ,
        "mobile"            :   str             ,
        "date_debut"        :   date (MM/yyyy)  ,
        "date_fin"          :   date (MM/yyyy)
    }

    :return:
    """
    ancien  =   _get_valid_ancien()
    data    =   _get_valid_data()
    abort(501, "Not implemented (yet) !")

    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # succes  =   annuaire.update_experience(
    #     id_ancien,
    #     id_experience,
    #     ville,
    #     id_pays,
    #     adresse,
    #     code,
    #     entreprise,
    #     poste,
    #     description,
    #     mail,
    #     site,
    #     telephone,
    #     mobile,
    #     date_debut,
    #     date_fin=None,
    # )


@app.route("/api/v1/me/experience/<int:id_experience>", methods=["PUT"])
@login_required
def update_experience_api(id_experience):
    """
    Modifier une expérience

    :return:
    """
    abort(501, "Not implemented (yet) !")


@app.route("/api/v1/me/experience/<int:id_experience>/set_default", methods=["PUT"])
@login_required
def experience_set_default_api(id_experience):
    """
    Définir une expérience comme étant celle par "défaut", "principale", "active"
    Affichée dans la liste des résultats de recheche.

    :param id_experience:
    :return:
    """
    if current_user.id_ancien is None:
        abort(403, "Tu n'as pas encore de fiche ancien. Il faut d'abord creer une fiche "
                   "ancien avant de pouvoir modifier tes experiences.")
    else:
        if annuaire.ancien_has_experience(current_user.id_ancien, id_experience):
            annuaire.set_default_experience(current_user.id_ancien, id_experience)
            return json.dumps({ "succes" : True })
        else:
            abort(404, "Aucune experience avec cet id n'est associee a ton compte.")




@app.route("/api/v1/me/experience/<int:id_experience>", methods=["DELETE"])
@login_required
def delete_experience_api(id_experience):
    """
    Effacer une expérience

    :param id_experience:
    :return:
    """
    abort(501, "Not implemented (yet) !")


def _get_valid_ancien():
    """
    Récupérer l'ancien associé à l'utilisateur courant.

    Si l'ancien n'existe pas,   abort   404
    Si l'ancien est bloqué,     abort   403 (??)

    :return: L'ancien :o)
    """
    ancien = annuaire.find_ancien_by_id(current_user.id_ancien, actif=None, nouveau=False, bloque=None)
    if ancien is None:
        abort(404, "Pas d'ancien associe a ce compte.")
    elif ancien["bloque"]:
        abort(403, "Il semblerai que tu compte soit bloque. "
           "Merci de contacter un administrateur pour le "
           "faire debloquer.")
    else:
        return ancien


def _get_valid_data():
    """
    Récupérer des données qui ont été envoyées (...) au format JSON.

    Si le parser plante : abort 400

    :return:    Les données sous forme de dictionnaire.
    """
    try:
        return json.loads(request.data)
    except:
        abort(400, "Les donnees n'ont pas ete envoyees au format JSON valide.")

