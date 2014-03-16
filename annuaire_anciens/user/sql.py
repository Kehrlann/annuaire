# coding=utf-8
import sys
from utilisateur import Utilisateur

sys.path.append('..')
from annuaire_anciens import engine
from werkzeug.security import check_password_hash as check, generate_password_hash as gen
from sqlalchemy import Table, Sequence, MetaData, select
from datetime import datetime

__engine = engine
__metadata = MetaData()
__utilisateur = Table('utilisateur', __metadata, autoload = True, autoload_with = __engine)
__inscription = Table('inscription', __metadata, autoload = True, autoload_with = __engine)
__s_id_photo = Sequence('s_id_photo')


def find_user_by_mail(form):
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
        utilisateur = __utilisateur
        sel = select([utilisateur]).where(__utilisateur.c.mail == mail)
        res = engine.execute(sel)
    if res is not None:
        row = res.first()
        print res
        if row is not None and check(row['password'], password):
            return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'])

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
        return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'])
    return None


def find_user_by_id_ancien(id_ancien):
    """
    Rechercher un utilisateur par id ancien
    @param id_ancien:  int, id_ancien
    @return: Utilisateur (None if not exist)
    """
    if id_ancien is  not None:
        sel = select([__utilisateur]).where(__utilisateur.c.id_ancien == id_ancien)
        result = engine.execute(sel)
        if result is not None:
            row = result.first()
            if row is not None:
                return Utilisateur(row['id_utilisateur'], row['mail'], row['id_ancien'])
    return None



def find_inscription_by_id_ancien(id_ancien):
    """
    Rechercher une inscription par id ancien
    @param id_ancien:  int, id_ancien
    @return: inscription (None if not exist)
    """
    if id_ancien is  not None:
        sel = select([__inscription]).where(__inscription.c.id_ancien == id_ancien)
        result = engine.execute(sel)
        if result is not None:
            inscription = result.first()
            return inscription
    return None


def create_preinscription(id_ancien, password, code_activation):
    """
    Créer une préinscription pour un id_ancien donné.
    On suppose qu'il n'existe pas de préinscription pour cet id_ancien. Si c'est le cas, SQL exception

    @param id_ancien:
    @param password: mot de passe en clair
    @param code_activation: code d'activation qu'on va également envoyer par mail
    """
    if id_ancien is not None and password is not None and password != "":
        ins = __inscription.insert().values(
            id_ancien=id_ancien,
            password=gen(password,'pbkdf2:sha512:1000', 12),
            date_inscription=datetime.now(),
            code_activation=code_activation
        )
        engine.execute(ins)

def validate_preinscription(inscription, ancien):
    """
    Valider une préinscription pour un ancien donné.
    1/ On crée l'utilisateur associé
    2/ On efface la préinscription associée

    @param inscription: la préinscription à valider
    @param ancien: l'ancien à associer au compte
    @return:
    """
    if inscription is not None and ancien is not None:
        ins = __utilisateur.insert().values(
            id_ancien = inscription['id_ancien'],
            mail = ancien['mail_asso'],
            password = inscription['password']
        )
        engine.execute(ins)

        suppr = __inscription.delete().where(__inscription.c.id_inscription==inscription['id_inscription'])
        engine.execute(suppr)


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


def get_next_photo_id():
    """
    récupérer un id pour la photo pour ne pas écraser une photo existante

    @return: long, un id
    """
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
