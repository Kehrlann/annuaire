# coding=utf-8
"""
    API relatives à l'utilsateur et à la gestion de son compte.
"""
from flask import request, session, abort
from flask.ext.login import current_user, login_required
import json

from annuaire_anciens import app, annuaire, user, SUCCESS, FAILURE, PAYS, helper
from datetime import datetime

from annuaire_anciens.helper.error_handlers import FormErrorCustom


@app.route("/api/v1/me", methods=["GET"])
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

    return json.dumps({"success":succes})


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

    return json.dumps({"success":succes})


@app.route("/api/v1/me/experience/<int:id_experience>", methods=["GET"])
@login_required
def get_experience_api(id_experience):
    """
    BLAH BLAH BLAH

    :param id_experience:
    :return:
    """
    ancien  =   _get_valid_ancien()
    experience = None
    # Verifier que l'ancien a bien le droit de modifier cette expérience
    try:
        experience = annuaire.find_experience_by_id_ancien_id_experience(ancien["id_ancien"], id_experience, False)
    except:
        abort(500)

    if experience is None:
        abort(403, "Vous ne pouvez modifier QUE les infos liees a votre propre compte")
    else:
        # Close the cursor
        return json.dumps(helper.row_to_json(experience))



@app.route("/api/v1/me/experience/<int:id_experience>", methods=["PUT"])
@login_required
def update_experience_api(id_experience):
    """
    Modifier une expérience

    :return:
    """
    ancien      =   _get_valid_ancien()
    experience  =   None
    # Verifier que l'ancien a bien le droit de modifier cette expérience
    try:
        experience = annuaire.find_experience_by_id_ancien_id_experience(ancien["id_ancien"], id_experience)
    except:
        abort(500)

    if experience is None:
        abort(403, "Vous ne pouvez modifier QUE les infos liees a votre propre compte")


    experience_form = user.update_experience_form.from_json(request.json)

    experience_form.set_pays(PAYS)
    form_confirmed = experience_form.validate()

    if not form_confirmed:
        print experience_form.errors
        raise FormErrorCustom("Erreur de saisie", experience_form.errors)

    else:
        try:
            date_debut = datetime.strptime(experience_form.date_debut.data, '%m/%Y')
        except ValueError:
            date_debut = None
        try:
            date_fin = datetime.strptime(experience_form.date_fin.data, '%m/%Y')
        except ValueError:
            date_fin = None

        success = annuaire.update_experience(
            current_user.id_ancien,
            id_experience,
            experience_form.ville.data,
            experience_form.pays.data,
            experience_form.adresse.data,
            experience_form.code.data,
            experience_form.entreprise.data,
            experience_form.poste.data,
            experience_form.description.data,
            experience_form.mail.data,
            experience_form.site.data,
            experience_form.telephone.data,
            experience_form.mobile.data,
            date_debut,
            date_fin
        )

        if success:
            return json.dumps(SUCCESS)

    abort(500, "Oops ! Erreur interne, vous ne devriez pas arriver ici ...")



@app.route("/api/v1/me/experience", methods=["POST"])
@login_required
def add_experience_api():
    """
    Ajouter une expérience

    :return:
    """
    ancien      =   _get_valid_ancien()
    experience  =   None

    experience_form = user.update_experience_form.from_json(request.json)

    experience_form.set_pays(PAYS)
    form_confirmed = experience_form.validate()

    if not form_confirmed:
        print experience_form.errors
        raise FormErrorCustom("Erreur de saisie", experience_form.errors)

    else:
        try:
            date_debut = datetime.strptime(experience_form.date_debut.data, '%m/%Y')
        except ValueError:
            date_debut = None
        try:
            date_fin = datetime.strptime(experience_form.date_fin.data, '%m/%Y')
        except ValueError:
            date_fin = None

        id_exp = annuaire.insert_experience(
            current_user.id_ancien,
            experience_form.ville.data,
            experience_form.pays.data,
            experience_form.adresse.data,
            experience_form.code.data,
            experience_form.entreprise.data,
            experience_form.poste.data,
            experience_form.description.data,
            experience_form.mail.data,
            experience_form.site.data,
            experience_form.telephone.data,
            experience_form.mobile.data,
            date_debut,
            date_fin
        )
        if id_exp:
            return json.dumps({ "id_experience" : id_exp })

    abort(500, "Oops ! Erreur interne, vous ne devriez pas arriver ici ...")


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
            return json.dumps(SUCCESS)
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
    ancien      =   _get_valid_ancien()
    experience  =   None
    # Verifier que l'ancien a bien le droit de modifier cette expérience
    try:
        experience = annuaire.find_experience_by_id_ancien_id_experience(ancien["id_ancien"], id_experience)
    except:
        abort(500)

    if experience is None:
        abort(403, "Vous ne pouvez modifier QUE les infos liees a votre propre compte")

    annuaire.remove_experience(ancien['id_ancien'], id_experience)

    return json.dumps(SUCCESS)


@app.route('/api/v1/me/toggleActif', methods=['PUT'])
@login_required
def update_actif():
    """
    Toggle l'état d'une fiche ancien : actif, inactif

    :return:
    """
    ancien      =   _get_valid_ancien()

    if ancien is not None:
        annuaire.update_actif(ancien['id_ancien'], not ancien['actif'])
        app.logger.info(
            "ANCIEN - successfully updated ancien :%s, set actif : %s, user : %s",
            ancien['id_ancien'],
            not ancien['actif'],
            current_user.id)

        return json.dumps({ "actif" : not ancien["actif"] })


    abort(500, "Oops ! Erreur interne, vous ne devriez pas arriver ici ...")

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

