# coding=utf-8
import sys
from utilisateur import Utilisateur

sys.path.append('..')
from annuaire_anciens import engine
from werkzeug.security import check_password_hash as check, generate_password_hash as gen
from sqlalchemy import Table, Sequence, MetaData, select

__engine = engine
__metadata = MetaData()
__utilisateur = Table('utilisateur', __metadata, autoload = True, autoload_with = __engine)
__s_id_photo = Sequence('s_id_photo')


def find_user_by_mail(mail, actif_only=True):
    """
    Rechercher un utilisateur dans l'annuaire

    @param mail: le mail de l'utilisateur
    @rtype: Utilisateur
    @return: un utilisateur
    """
    if mail is not None:
        condition = __utilisateur.c.mail == mail.lower()
        if actif_only:
            condition &= __utilisateur.c.actif
        sel = select([__utilisateur]).where(condition)
        res = engine.execute(sel)
        if res is not None:
            row = res.first()
            if row is not None:
                return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'], row['actif'])
    return None


def find_user_by_mail_and_password(form, actif_only=True):
    """
    Rechercher un utilisateur dans l'annuaire

    @param form: request form
    @rtype: Utilisateur
    @return: un utilisateur
    """
    mail = form.mail.data
    password = form.password.data
    res = None
    if password is None:
        password = ""
    if mail is not None:
        condition = __utilisateur.c.mail == mail.lower()
        if actif_only:
            condition &= __utilisateur.c.actif
        sel = select([__utilisateur]).where(condition)
        res = engine.execute(sel)
    if res is not None:
        row = res.first()
        if row is not None and check(row['password'], password):
            return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'], row['actif'])
    return None

def find_user_by_id(id_user):
    """
    Rechercher un utilisateur

    @param id_user: user id, no shit ...

    @rtype : Utilisateur
    @return : Utilisateur (None if not exist)
    """

    res = __select_user_by_id(id_user)
    if res is not None:
        row = res.first()
        return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'], row['actif'])
    return None


def find_user_by_id_ancien(id_ancien, actif_only=False):
    """
    Rechercher un utilisateur par id ancien
    @param id_ancien:  int, id_ancien
    @return: Utilisateur (None if not exist)
    """
    if id_ancien is  not None:
        condition = __utilisateur.c.id_ancien == id_ancien
        if actif_only:
            condition &= __utilisateur.c.actif
        sel = select([__utilisateur]).where(condition)
        result = engine.execute(sel)
        if result is not None:
            row = result.first()
            if row is not None:
                return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'], row['actif'])
    return None


def activate_user(id_user):
    """
    Activer un utilisateur

    @param id_user: L'utilisateur à activer
    """
    res = False
    if id_user is not None:
        up = __utilisateur.update().where(__utilisateur.c.id_utilisateur == id_user).values(actif=True)
        engine.execute(up)
        res = True
    return res


def update_password_by_id(id_user, old_pass, new_pass):
    """
    Mettre a jour le mot de passe d'un utilisateur. Pour verification, on utilise son ancien mot de passe

    @param id_user: user id_user
    @param old_pass: ancien mot de passe, doit être vérifié pour voir si on a le droit d'update (mieux qu'un fresh login)
    @param new_pass: nouveau mot de passe

    @rtype : bool

    @return : True si ok, False si nok
    """
    result = False
    res = __select_user_by_id(id_user)
    if old_pass is None:
        old_pass = ""
    if res is not None and new_pass is not None:
        row = res.first()
        if row is not None and check(row['password'], old_pass) and new_pass is not None:
            up = __utilisateur.update(
            ).where(
                __utilisateur.c.id_utilisateur == id_user
            ).values(
                password = gen(new_pass,'pbkdf2:sha512:1000', 12)
            )
            engine.execute(up)
            result = True
    return result


def confirm_password(id_user, password):
    """
    verifier que l'utilisateur a bien saisi le bon mot de passe

    @params :
    id_user         -- user id
    password    -- pass

    @return : True si c'est le bon pass, False si c'est le mauvais
    """
    result = False
    if password is None:
        password = ""
    res = __select_user_by_id(id_user)
    if res is not None:
        row = res.first()
        if row is not None and check(row['password'], password):
            result = True
    return result


def update_id_ancien(id_user, id_ancien):
    """
    Mettre à jour l'id_ancien pour un utilisateur donné

    @params :
    id_user     -- user id
    id_ancien   -- id de l'ancien à associer à ce compte

    @return : L'objet utilisateur
    """
    res = False
    if id_ancien and id_user:
        up = __utilisateur.update().where(
            __utilisateur.c.id_utilisateur == id_user
        ).values(
            id_ancien = id_ancien
        )
        sql_result = engine.execute(up)
        if sql_result is not None:
            sql_result.close() # close this shit.
            res = True
    return res


def create_user(mail, password):
    """
    Créer un utilisateur dans la base de données.
    @param mail: le mail de l'utilisateur, unique
    @param password: le mot de passe
    """
    res = False
    if mail is not None:
        ins = __utilisateur.insert().values(
            id_ancien = None,
            mail = mail,
            password = password
        )
        engine.execute(ins)
        res = True
    return res


def get_next_photo_id():
    """
    récupérer un id pour la photo pour ne pas écraser une photo existante
    @return: long, un id
    """
    # TODO : déplacer ça dans l'annuaire
    res = engine.execute(__s_id_photo)
    return res


def __select_user_by_id(id_user=None):
    """
    Recuperer un user par mail (unique)

    @param id_user: id de l'utilisateur
    @rtype : sqlalchemy.core.ResultProxy
    @return : SELECT * FROM utilisateur WHERE id_utilisateur=id_user;
    """
    result = None
    if id_user is  not None:
        sel = select([__utilisateur]).where(__utilisateur.c.id_utilisateur == id_user)
        result = engine.execute(sel)
    return result
