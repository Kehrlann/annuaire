# coding=utf-8
"""
Module d'interaction avec les objets "anciens" de la base de données.
TODO : décrire le schéma de bdd
TODO : séparer les fonctions de lecture et d'écriture
"""

import sys
sys.path.append('..')
from annuaire_anciens import engine
from sqlalchemy import Table, MetaData, or_, and_, select, desc, asc, func
import annuaire_anciens.helper as helper
from datetime import date


# set up the module with the connection and stuff
__engine = engine
__metadata = MetaData()

# set up the tables
__pays = Table('pays', __metadata, autoload=True, autoload_with=__engine)
__ville = Table('ville', __metadata, autoload=True, autoload_with=__engine)
__adresse = Table('adresse', __metadata, autoload=True, autoload_with=__engine)
__asso_ancien_adresse = Table('asso_ancien_adresse', __metadata, autoload=True, autoload_with=__engine)
__entreprise = Table('entreprise', __metadata, autoload=True, autoload_with=__engine)
__experience = Table('experience', __metadata, autoload=True, autoload_with=__engine)
__ancien = Table('ancien', __metadata, autoload=True, autoload_with=__engine)
__mot = Table('mot', __metadata, autoload=True, autoload_with=__engine)

__entreprise_interne = __entreprise.alias()
__villePerso = __ville.alias()
__villePro = __ville.alias()




def count_fulltext(search_terms, actif = True, bloque = False):
    """
    Compter les anciens trouvés par la recherche fulltext

    :param str search_terms:    Termes utilisés pour la recherche


    :param bool actif:          True (default)  =   Chercher uniquement les actifs
                                False           =   Chercher uniquement les inactifs
                                None            =   Chercher TOUS les anciens

    :param bool bloque:         True            =   Chercher uniquement les bloqués
                                False (default) =   Chercher uniquement les autres
                                None            =   Chercher tous les anciens

    :return int:                le nombre d'anciens qui satisfont les termes de recherche
    """
    sel = select([func.count(__ancien.c.id_ancien.distinct())]).where("fulltext @@ to_tsquery('french', :input_str)")
    sel = sel.where(__ancien.c.nouveau == False)


    if actif is not None:
        sel = sel.where(__ancien.c.actif == actif)

    if bloque is not None:
        sel = sel.where(__ancien.c.bloque == bloque)


    res = engine.execute(sel, input_str=helper.prepare_for_fulltext(search_terms)).first()[0]
    return res


def fulltext_search(search_terms, offset = 0, limit =0, actif = True, bloque = False):
    """
    Recherche un ancien dans l'annuaire par fulltext search

    :param str search_terms:    Termes utilisés pour la recherche
    :param int offset:          démarrer la requête au  rang X
    :param int limit:           prendre Y résultats

    :param bool actif:          True (default)  =   Chercher uniquement les actifs
                                False           =   Chercher uniquement les inactifs
                                None            =   Chercher TOUS les anciens

    :param bool bloque:         True            =   Chercher uniquement les bloqués
                                False (default) =   Chercher uniquement les autres
                                None            =   Chercher tous les anciens
    :return:
    """
    aaa = __asso_ancien_adresse

    from_obj = __ancien
    from_obj = from_obj.outerjoin(
    aaa, and_(__ancien.c.id_ancien == aaa.c.id_ancien, aaa.c.actif == True)
    ).outerjoin(
        __adresse, aaa.c.id_adresse == __adresse.c.id_adresse
    ).outerjoin(
        __ville, __adresse.c.id_ville == __ville.c.id_ville
    ).outerjoin(
        __pays, __ville.c.id_pays == __pays.c.id_pays
    ).outerjoin(
        __experience, and_(__ancien.c.id_ancien == __experience.c.id_ancien)
    ).outerjoin(
        __entreprise, __experience.c.id_entreprise == __entreprise.c.id_entreprise
    )

    sel = select(
    [
        __ancien.c.id_ancien.label('id'),
        __ancien.c.prenom.label('prenom'),
        __ancien.c.nom.label('nom'),
        __ancien.c.ecole.label('ecole'),
        __ancien.c.promo.label('promo'),
        __ancien.c.fulltext.label('fulltext'),
        __ville.c.nom.label('ville'),
        __adresse.c.code.label('code_postal'),
        __entreprise.c.nom.label('entreprise'),
        __pays.c.nom.label('pays')
    ],
        from_obj=from_obj,
        use_labels=True
    ).order_by(
        __ancien.c.ecole,
        __ancien.c.promo,
        __ancien.c.nom,
        __ancien.c.prenom,
        desc(__experience.c.actif),
        desc(__experience.c.debut).nullslast()
    )
    sel = sel.where("fulltext @@ to_tsquery('french', :input_str)")
    sel = sel.where(__ancien.c.nouveau == False)

    if actif is not None:
        sel = sel.where(__ancien.c.actif == actif)

    if bloque is not None:
        sel = sel.where(__ancien.c.bloque == bloque)

    sel = sel.distinct(
        __ancien.c.ecole,
        __ancien.c.promo,
        __ancien.c.nom,
        __ancien.c.prenom
    )

    new_sel = sel.alias().select().order_by(
        "ts_rank_cd(fulltext, to_tsquery('french', :input_str)) DESC"
    )

    new_sel = new_sel.offset(offset).limit(limit)

    res = engine.execute(new_sel, input_str=helper.prepare_for_fulltext(search_terms)).fetchall()
    return res


def annuaire_search(form, offset = 0, limit = 0, actif = True, bloque = False):
    """
    Recerche un ancien dans l'annuaire selon les critères specifiés dans le form

    :param WTForm form:         annuaire.form.SearchForm
    :param int offset:          démarrer la requête au  rang X
    :param int limit:           prendre Y résultats

    :param bool actif:          True (default)  =   Chercher uniquement les actifs
                                False           =   Chercher uniquement les inactifs
                                None            =   Chercher TOUS les anciens

    :param bool bloque:         True            =   Chercher uniquement les bloqués
                                False (default) =   Chercher uniquement les autres
                                None            =   Chercher tous les anciens

    :return:
    """
    aaa = __asso_ancien_adresse

    from_obj = _get_from_object(form)
    from_obj = from_obj.outerjoin(
        aaa, and_(__ancien.c.id_ancien == aaa.c.id_ancien, aaa.c.actif == True)
    ).outerjoin(
        __adresse, aaa.c.id_adresse == __adresse.c.id_adresse
    ).outerjoin(
        __ville, __adresse.c.id_ville == __ville.c.id_ville
    ).outerjoin(
        __pays, __ville.c.id_pays == __pays.c.id_pays
    ).outerjoin(
        __experience, and_(__ancien.c.id_ancien == __experience.c.id_ancien)
    ).outerjoin(
        __entreprise, __experience.c.id_entreprise == __entreprise.c.id_entreprise
    )

    sel = select(
    [
        __ancien.c.id_ancien.label('id'),
        __ancien.c.prenom.label('prenom'),
        __ancien.c.nom.label('nom'),
        __ancien.c.ecole.label('ecole'),
        __ancien.c.promo.label('promo'),
        __ville.c.nom.label('ville'),
        __adresse.c.code.label('code_postal'),
        __entreprise.c.nom.label('entreprise'),
        __pays.c.nom.label('pays')
    ],
    from_obj=from_obj,
    use_labels=True
    ).order_by(
        __ancien.c.ecole,
        __ancien.c.promo,
        __ancien.c.nom,
        __ancien.c.prenom,
        desc(__experience.c.actif),
        desc(__experience.c.debut).nullslast()
    )

    sel = sel.where(__ancien.c.nouveau == False)

    if actif is not None:
        sel = sel.where(__ancien.c.actif == actif)

    if bloque is not None:
        sel = sel.where(__ancien.c.bloque == bloque)

    sel = sel.distinct(
        __ancien.c.ecole,
        __ancien.c.promo,
        __ancien.c.nom,
        __ancien.c.prenom
    )
    sel = sel.offset(offset).limit(limit)

    return _filter_search(form, sel).fetchall()


def count_annuaire_search(form, actif = True, bloque = False):
    """
    Compter les anciens dans l'annuaire en fonction d'un formulaire

    :param WTForm form:         formulaire de filtrage

    :param bool actif:          True (default)  =   Chercher uniquement les actifs
                                False           =   Chercher uniquement les inactifs
                                None            =   Chercher TOUS les anciens

    :param bool bloque:         True            =   Chercher uniquement les bloqués
                                False (default) =   Chercher uniquement les autres
                                None            =   Chercher tous les anciens

    :return int:                le nombre d'anciens qui satisfont FORM
    """
    from_obj = _get_from_object(form)
    sel = select([func.count(__ancien.c.id_ancien.distinct())], from_obj=from_obj)
    sel = sel.where(__ancien.c.nouveau == False)


    if actif is not None:
        sel = sel.where(__ancien.c.actif == actif)

    if bloque is not None:
        sel = sel.where(__ancien.c.bloque == bloque)

    return _filter_search(form, sel).first()[0]


def _get_from_object(form):
    """
    Crée from_object à la mode pour une requete SQL. Permet d'alléger les requêtes en ne prenant que les champs
    qui sont nécessaires et en limitant les join.

    Par exemple,
    if !(form.estPerso.data or form.estPro.data):
        alors on ne join pas les tables d'adresses

    :param form: annuaire.form.SearchForm
    :return: sqlalchemy.core.from
    """

    from_obj = __ancien

    ville = None

    if form.ville.data != '':
        ville = form.ville.data

    pays_id = None

    if form.pays.data != '':
        pays_id = int(form.pays.data)

    search_adresse = (pays_id is not None or ville is not None)

    entreprise = form.entreprise.data

    if entreprise is not None and entreprise != '':
        exp = __experience.alias()
        from_obj = from_obj.join(exp).join(__entreprise_interne)


    if search_adresse:
        ex = __experience.alias()
        ad_pro = __adresse.alias()
        aaa = __asso_ancien_adresse.alias()
        ad_perso = __adresse.alias()

        from_obj = from_obj.join(ex, __ancien.c.id_ancien == ex.c.id_ancien)
        from_obj = from_obj.join(ad_pro, ad_pro.c.id_adresse == ex.c.id_adresse)
        from_obj = from_obj.join(__villePro, __villePro.c.id_ville == ad_pro.c.id_ville)

        from_obj = from_obj.join(aaa, __ancien.c.id_ancien == aaa.c.id_ancien)
        from_obj = from_obj.join(ad_perso, ad_perso.c.id_adresse == aaa.c.id_adresse)
        from_obj = from_obj.join(__villePerso, __villePerso.c.id_ville == ad_perso.c.id_ville)

    return from_obj



def _filter_search(form, sel):
    """
    Filtrer une requête select en fonction d'un FORM
    :param form: formulaire de filtrage
    :param sel: select query, soit un count soit un requete classique
    :return: sel.WHERE(form)
    """
    nom = form.nom.data

    prenom = form.prenom.data

    ecole = form.ecole.data

    promo = form.promo.data

    entreprise = None

    if form.entreprise.data != '':
        entreprise = form.entreprise.data

    ville = None

    if form.ville.data != '':
        ville = form.ville.data

    pays_id = None

    if form.pays.data != '':
        pays_id = int(form.pays.data)

    perso_pro = form.adresse.data == 'deux'

    est_perso = perso_pro or form.adresse.data == 'perso'

    est_pro = perso_pro or form.adresse.data == 'pro'

    search_adresse = (pays_id is not None or ville is not None)

    # Filtrer par nom
    if nom is not None and nom != '':
        sel = sel.where(_slug_raw_input_by_column(__ancien.c.nom_slug, nom))

    # Filtrer par prénom
    if prenom is not None and prenom != '':
        sel = sel.where(_slug_raw_input_by_column(__ancien.c.prenom_slug, prenom))

    # Filtrer par entreprise
    if entreprise is not None:
        sel = sel.where(_slug_raw_input_by_column(__entreprise_interne.c.slug, entreprise))

    # Filtrer par adresse, perso et/ou pro
    if search_adresse:
        filtre_ville = _where_ville(ville, est_perso, est_pro)
        filtre_pays = _where_pays(pays_id, est_perso, est_pro)

        if filtre_ville is not None:
            sel = sel.where(filtre_ville)
        if filtre_pays is not None:
            sel = sel.where(filtre_pays)

    # filtrer par école
    if ecole is not None and ecole != '':
        sel = sel.where(__ancien.c.ecole == ecole)

    # filtrer par promo
    if promo is not None and promo !='':
        sel = _refine_by_promo(sel, promo) # no slug, post-traitement

    res = engine.execute(sel)
    return res


def find_ancien_by_id(id_ancien, actif = None, nouveau = False, bloque = False):
    """
    Rechercher un ancien par id

    :param int id_ancien: l'id ancien (sisi)

    :param bool actif:      True            =   Chercher uniquement les actifs
                            False           =   Chercher uniquement les inactifs
                            None (default)  =   Chercher TOUS les anciens

    :param bool nouveau:    True            =   Chercher uniquement les nouveaux
                            False (default) =   Chercher uniquement les autres
                            None            =   Chercher tous les anciens

    :param bool bloque:     True            =   Chercher uniquement les bloqués
                            False (default) =   Chercher uniquement les autres
                            None            =   Chercher tous les anciens


    :return:    SELECT DISTINCT *
                    FROM ancien
                    WHERE
                        id_ancien = id_ancien
                        (AND actif = actif)
                        (AND nouveau = nouveau)
                        (AND bloque = bloque);
    """
    sel = select([__ancien], __ancien.c.id_ancien == id_ancien).distinct()

    if actif is not None:
        sel = sel.where(__ancien.c.actif == actif)

    if bloque is not None:
        sel = sel.where(__ancien.c.bloque == bloque)

    if nouveau is not None:
        sel = sel.where(__ancien.c.nouveau == nouveau)


    res = engine.execute(sel).first()
    return res


def find_ancien_by_mail_asso(mail_asso):
    """
    Rechercher un ancien par son "mail à vie" de l'association. Utilisé pour associer
    un user et un ancien.

    :param mail_asso: mail@mines-paris.org (ou mines-nancy.org ou mines-saint-etienne.org)
    :return:
        - SELECT DISTINCT * FROM ancien WHERE mail_asso = mail_asso;
        - First result only
        - NONE if not found
    """
    sel = select([__ancien], __ancien.c.mail_asso == mail_asso).distinct()
    res = engine.execute(sel).first()
    return res


def find_ancien_by_id_linkedin(id_linkedin):
    """
    Trouver un ancien par ID_linkedin.

    :param id_linkedin: l'id renvoyé par LinkedIn pour identifier un compte.
    :return :
        - SELECT DISTINCT * FROM ancien WHERE id_linkedin = id_linkedin;
        - First result only
        - NONE if not found
    """
    sel = select([__ancien], __ancien.c.id_linkedin == id_linkedin).distinct()
    res = engine.execute(sel)
    if res is not None:
        res = res.first()
    return res


def find_ancien_filtres(nouveau = None, bloque = None):
    """
    Trouver tous les anciens qui ont le flag "nouveau", ou "bloques"


    :param bool nouveau:    True            =   Chercher uniquement les nouveaux
                            False           =   Chercher uniquement les autres
                            None (default)  =   Chercher tous les anciens

    :param bool bloque:     True            =   Chercher uniquement les bloqués
                            False           =   Chercher uniquement les autres
                            None (default)  =   Chercher tous les anciens



    :return:
        - SELECT DISTINCT * FROM ancien WHERE nouveau = True
    """
    sel = select([__ancien]).distinct()

    if nouveau is not None:
        sel = sel.where(__ancien.c.nouveau == nouveau)

    if bloque is not None:
        sel = sel.where(__ancien.c.bloque == bloque)

    return engine.execute(sel).fetchall()


def find_adresse_by_id_ancien(id_ancien, use_labels=True):
    """
    Rechercher une adresse par id_ancien

    :param id_ancien:
    :return: Select * from adresse join asso where asso.id_ancien=truc
    """
    if id_ancien is not None and type(id_ancien) is int:
        aaa = __asso_ancien_adresse
        sel = select(
            [__adresse.c.adresse,
             __adresse.c.code,
             __ville.c.nom.label("ville"),
             __pays.c.nom.label("pays"),
             __pays.c.id_pays],
            and_(aaa.c.id_ancien == id_ancien, aaa.c.actif==True),
            from_obj=aaa.join(__adresse).outerjoin(__ville).outerjoin(__pays),
            use_labels=use_labels).distinct()
        return engine.execute(sel).first()
    else:
        return None


def find_experience_by_id_ancien(id_ancien, use_labels=True):
    """
    Rechercher une experience par id_ancien
    
    :params :
    id_ancien    -- int
    qb           -- custom query builder, see sql.query
    """
    if id_ancien is not None and type(id_ancien) is int:
        ex = __experience
        en = __entreprise
        a = __adresse
        v = __ville
        p = __pays
        sel =  select(
            [ex.c.actif,
             ex.c.id_experience,
             ex.c.telephone,
             ex.c.mobile,
             ex.c.mail,
             ex.c.site,
             ex.c.poste,
             ex.c.description,
             ex.c.debut,
             ex.c.fin,
             ex.c.id_experience_linkedin,
             en.c.nom.label("entreprise"),
             a.c.adresse,
             a.c.code,
             v.c.nom.label("ville"),
             p.c.nom.label("pays"),
             p.c.id_pays],
            ex.c.id_ancien == id_ancien,
            from_obj=ex.outerjoin(en).outerjoin(a).outerjoin(v).outerjoin(p),
            use_labels=use_labels).order_by(desc(ex.c.actif)).order_by(desc(ex.c.debut).nullslast()).distinct()
        return engine.execute(sel)
    else:
        return None

def find_experience_by_id_ancien_id_experience(id_ancien, id_experience, use_labels=True):
    """
    Rechercher une experience par id_ancien et id_experience
    Ces doubles id assurent que l'experience esst bien associée à l'ancien étudié

    :params :
    id_ancien    -- int
    qb           -- custom query builder, see sql.query
    """
    if id_ancien is not None and type(id_ancien) is int:
        ex = __experience
        en = __entreprise
        a = __adresse
        v = __ville
        p = __pays
        sel =  select(
            [ex.c.actif,
             ex.c.id_experience,
             ex.c.telephone,
             ex.c.mobile,
             ex.c.mail,
             ex.c.site,
             ex.c.poste,
             ex.c.description,
             ex.c.debut,
             ex.c.fin,
             ex.c.id_experience_linkedin,
             en.c.nom.label("entreprise"),
             a.c.adresse,
             a.c.code,
             v.c.nom.label("ville"),
             p.c.nom.label("pays"),
             p.c.id_pays],
            and_(ex.c.id_ancien == id_ancien, ex.c.id_experience == id_experience),
            from_obj=ex.outerjoin(en).outerjoin(a).outerjoin(v).outerjoin(p),
            use_labels=use_labels).order_by(desc(ex.c.debut)).order_by(desc(ex.c.actif).nullslast()).distinct()
        return engine.execute(sel).first()
    else:
        return None

def find_nom_autocomplete(term, limit=5):
    """
    Rechercher une liste de noms pour l'autocomplete

    :param term: terme de recherche (un seul)
    :return: SELECT nom FROM ancien WHERE ancien.nom_slug LIKE 'term%'
    """
    result = None
    if not (term is None or term == ""):
        sel = select([__ancien.c.nom], __ancien.c.nom_slug.like(helper.slugify(term)+'%'))
        sel = sel.distinct().order_by(__ancien.c.nom).limit(limit)
        result = engine.execute(sel)
    return result


def find_ville_autocomplete(term, limit=5):
    """
    Rechercher une liste de villes pour l'autocomplete

    :param term: terme de recherche (un seul)
    :return: SELECT nom FROM ville WHERE ville.slug LIKE 'term%'
    """
    result = None
    if not (term is None or term == ""):
        sel = select([__ville.c.nom], __ville.c.slug.like(helper.slugify(term)+'%'))
        sel = sel.distinct().order_by(__ville.c.nom).limit(limit)
        result = engine.execute(sel)
    return result


def find_entreprise_autocomplete(term, limit=5):
    """
    Rechercher une liste d'entreprise pour l'autocomplete

    :param term: terme de recherche (un seul)
    :return: SELECT nom FROM entreprise WHERE entreprise.slug LIKE 'term%'
    """
    result = None
    if not (term is None or term == ""):
        sel = select([__entreprise.c.nom], __entreprise.c.slug.like(helper.slugify(term)+'%'))
        sel = sel.distinct().order_by(__entreprise.c.nom).limit(limit)
        result = engine.execute(sel)
    return result


def find_mot_autocomplete(term, limit=10):
    """
    Recherche une liste de mot dans la table mot. Limite les réponses à _limit_ réponses.
    On recherche d'abord l'expression complète, par exemple
    '''SNCF Services'''
    Puis on recherche le dernier mot, ici, '''Services'''

    :param term: terme de recherche, une seule string
    :return: SELECT mot FROM mot WHERE mot.slug LIKE 'slugify(term)%' OR mot.slug LIKE 'slugify(last_term%)'
    """
    result = None
    if not (term is None or  term == ""):
        slug = helper.slugify(term)
        condition1 = __mot.c.slug.like(slug +'%')

        sel = select([__mot.c.mot]).where(condition1).order_by(desc(__mot.c.occurence)).limit(limit)
        result = engine.execute(sel).fetchall()
        #last_word = slug.strip("-").split("-")[-1]
        #if len(result) == 0 and last_word != "":
        #    condition2 = __mot.c.slug.like(last_word+"%")
        #    sel = select([__mot.c.mot]).where(condition2).order_by(desc(__mot.c.occurence)).limit(limit)
        #    result = engine.execute(sel).fetchall()
    return result



def create_ancien(prenom, nom, promo, ecole, mail_asso, diplome):
    """
    Créer un ancien à partir des données d'un formulaire

    :param str prenom:
    :param str nom:
    :param int promo:
    :param str ecole: In E, P, N
    :param str mail_asso:
    :param str diplome:
    :return:
    """
    ins = __ancien.insert().returning(__ancien.c.id_ancien).values(
        prenom=prenom,
        prenom_slug=helper.slugify(prenom),
        nom=nom,
        nom_slug=helper.slugify(nom),
        ecole=ecole,
        promo=promo,
        mail_asso=mail_asso,
        diplome=diplome,
    )
    inserted_id = engine.execute(ins).first()[0]
    update_ancien_date(inserted_id)
    return inserted_id



def update_ancien_date(id_ancien):
    """
    Mettre à jour ancien.date_update pour marquer que la fiche ancien à été mise à jour à la date du jour
    :param id_ancien: l'id de l'ancien
    :return: boolean success = true si l'update fonctionne
    """
    success = False
    if helper.is_valid_integer(id_ancien):
        up = __ancien.update().where(
                __ancien.c.id_ancien == id_ancien
            ).values(
                date_update=date.today()
            )
        result = engine.execute(up)
        if result is not None:

            # Update le ts_vector (fulltext) associé à l'ancien en question.
            # Étrangement, il faut EXPLICITEMENT démarrer une transaction et la commiter
            conn = engine.connect()
            trans = conn.begin()
            conn.execute(func.reset_fulltext_by_id_ancien(id_ancien))
            trans.commit()
            conn.close()

            success = True
    return success

def update_fiche_ancien(id_ancien, telephone="", mobile="", site="", mail_perso=""):
    """
    Mettre à jour une fiche ancien par id_ancien
    :param id_ancien: int, l'id_ancien
    :param telephone: str < 20 char
    :param mobile: str < 20 char
    :param site: str < 200 char
    :param mail_perso: str < 75 char
    :return: boolean success = true si l'update fonctionne
    """
    success = False
    if helper.is_valid_integer(id_ancien):
        up = __ancien.update().where(
            __ancien.c.id_ancien == id_ancien
        ).values(
            telephone=telephone,
            mobile= mobile,
            site = site,
            mail_perso=mail_perso
        )
        result = engine.execute(up)
        if result is not None:
            success = update_ancien_date(id_ancien)
    return success


def update_actif(id_ancien, actif):
    """
    Mettre à jour une fiche ancien : la rendre active ou inactive

    :param int id_ancien:   Id de l'ancien à modifier
    :param bool actif:      Status à affecter à l'ancien
    :return: bool succes = true si l'update fonctionne
    """
    success = False
    up = __ancien.update().where(
            __ancien.c.id_ancien == id_ancien
        ).values(
            actif=actif
        )
    result = engine.execute(up)
    if result is not None:
        success = update_ancien_date(id_ancien)
    return success


def update_linkedin_ancien(id_ancien, id_linkedin=None, url_linkedin=None):
    """
    Mettre à jour le compte linkedin d'un ancien

    :param id_ancien: id de l'ancien en question
    :param id_linkedin: id_linkedin à sauvegarder
    :param url_linkedin:  profil public linkedin à sauvegarder
    :return: True si success
    """
    success = False
    if helper.is_valid_integer(id_ancien):
        up = __ancien.update().where(
            __ancien.c.id_ancien == id_ancien
        ).values(
            id_linkedin=id_linkedin,
            url_linkedin= url_linkedin
        )
        result = engine.execute(up)
        if result is not None:
            success = update_ancien_date(id_ancien)
    return success

def update_photo(id_ancien, filename):
    """
    Mettre à jour la photo d'un ancien, par ID
    :param id_ancien: int, id de l'ancien (ya rly)
    :param filename: le nom de la photo
    :return: boolean success = true si l'update fonctionne
    """
    success = False
    up = __ancien.update().where(__ancien.c.id_ancien == id_ancien).values(photo=filename)
    result = engine.execute(up)
    if result is not None:
        success = update_ancien_date(id_ancien)
    return success

def update_adresse_perso(id_ancien, ville, id_pays, adresse="", code=""):
    """
    Mettre à jour l'adresse active d'un ancien, en updatant ou insérant.
    En updatant ou insérant la ville au passage

    :param id_ancien: int, id_ancien
    :param adresse: str, l'adresse en texte libre
    :param ville: str, la ville en texte libre
    :param code: int, le ocde postal en texte libre puis converti en int
    :param id_pays: int
    :return: boolean success = true si ça marche, false sinon
    """
    success = False
    id_adresse = None
    new_adresse = True

    aaa = __asso_ancien_adresse
    # 1 : est-ce que l'adresse existe ?
    sel = select([aaa.c.id_adresse]).where(and_(aaa.c.actif == True, aaa.c.id_ancien == id_ancien))
    res = engine.execute(sel).first()
    if res is not None:
        id_adresse = res[0]
        new_adresse = False

    id_adresse = _insert_update_adresse(ville, id_pays, id_adresse, adresse, code)

    if new_adresse:
        # insérer l'asso
        ins =  __asso_ancien_adresse.insert().values(id_ancien=id_ancien, id_adresse=id_adresse, actif=True)
        engine.execute(ins)
    success = update_ancien_date(id_ancien)
    return success

def update_experience(id_ancien, id_experience, ville, id_pays, adresse, code,
                      entreprise, poste, description, mail, site, telephone, mobile,
                      date_debut, date_fin=None, id_experience_linkedin=None):
    """
    Mettre à jour / insérer une expérience pro ancien

    :param id_ancien:
    :param id_experience:
    :param ville:
    :param id_pays:
    :param adresse:
    :param code:
    :param entreprise:
    :param poste:
    :param description:
    :param mail:
    :param site:
    :param telephone:
    :param mobile:
    :return: inserted_id, l'id de l'expérience insérée / mise à jour
    """
    success = False
    inserted_id = None

    if id_ancien is not None:

        # s'occuper de l'adresse
        id_adresse = None
        sel = select([__experience.c.id_adresse]).where(and_(__experience.c.id_ancien == id_ancien, __experience.c.id_experience == id_experience))
        res = engine.execute(sel).first()
        if res is not None:
            id_adresse = res[0]
        id_adresse = _insert_update_adresse(ville, id_pays, id_adresse, adresse, code)

        # s'occuper de l'entreprise
        id_entreprise = None
        sel = select([__entreprise.c.id_entreprise]).where(_slug_by_column(__entreprise.c.slug, helper.slugify(entreprise), True))
        res = engine.execute(sel).first()
        if res is not None:
            id_entreprise = res[0]

        if id_entreprise is None and entreprise != "":
            ins = __entreprise.insert().values(nom=entreprise, slug=helper.slugify(entreprise))
            engine.execute(ins)
            sel = select([__entreprise.c.id_entreprise]).where(_slug_by_column(__entreprise.c.slug, helper.slugify(entreprise), True))
            id_entreprise = engine.execute(sel).first()[0]

        # insert / update experience
        if id_experience is not None:

            # update ssi l'expérience est associée au bon ancien
            up = __experience.update().where(
                and_(
                    __experience.c.id_experience == id_experience,
                    __experience.c.id_ancien == id_ancien
                )
            ).values(
                id_entreprise = id_entreprise,
                id_adresse = id_adresse,
                poste = poste,
                description = description,
                telephone = telephone,
                mobile = mobile,
                mail = mail,
                site = site,
                debut = date_debut,
                fin = date_fin
            )
            engine.execute(up)

        else:
            ins = __experience.insert().values(
                id_ancien = id_ancien,
                id_entreprise = id_entreprise,
                id_adresse = id_adresse,
                poste = poste,
                description = description,
                telephone = telephone,
                mobile = mobile,
                mail = mail,
                site = site,
                debut = date_debut,
                fin = date_fin,
                id_experience_linkedin = id_experience_linkedin
            )
            engine.execute(ins)
            print ins

        success = update_ancien_date(id_ancien)
    return success


def insert_experience(id_ancien, ville, id_pays, adresse, code,
                      entreprise, poste, description, mail, site, telephone, mobile,
                      date_debut, date_fin=None, id_experience_linkedin=None):
    """
    Insérer une expérience pro

    :param id_ancien:
    :param ville:
    :param id_pays:
    :param adresse:
    :param code:
    :param entreprise:
    :param poste:
    :param description:
    :param mail:
    :param site:
    :param telephone:
    :param mobile:
    :param date_debut:
    :param date_fin:
    :param id_experience_linkedin:
    :return:
    """

    return update_experience    (   id_ancien, None, ville, id_pays, adresse, code,
                                    entreprise, poste, description, mail, site, telephone, mobile,
                                    date_debut, date_fin, None
                                )


def ancien_has_experience(id_ancien, id_experience):
    """
    Vérifier qu'une expérience donnée est bien associée à l'ancien
    en question.

    :param id_ancien:
    :param id_experience:
    :return:
    """
    sel = select(
        [__experience.c.id_experience],
        and_(__experience.c.id_experience==id_experience, __experience.c.id_ancien==id_ancien)
    )
    res = engine.execute(sel).first()
    return res is not None


def set_default_experience(id_ancien, id_experience):
    """
    marquer une expérience comme "active", et "désactiver" les
    autre expériences d'un ancien donner.

    :param id_ancien:
    :param id_experience:
    :return:
    """
    up = __experience.update().where(__experience.c.id_ancien==id_ancien).values(actif=False)
    engine.execute(up)
    up = __experience.update().where(__experience.c.id_experience==id_experience).values(actif=True)
    engine.execute(up)


def update_ancien_bloque(id_ancien, bloque):
    """
    Bloquer ou débloquer un ancien

    :param int id_ancien:   l'id de l'ancien à bloquer/débloquer
    :param bool bloque:     Pour bloquer (True) ou débloquer (False)
    :return:
    """
    success = False
    if id_ancien is not None and bloque is not None:
        up = __ancien.update().where(
                __ancien.c.id_ancien == id_ancien
        ).values(
            bloque = bloque
        )
        engine.execute(up)

        success = True

    return success


def update_ancien_valider(id_ancien):
    """
    Valider un ancien

    :param int id_ancien:   l'id de l'ancien à valider
    """
    success = False
    if id_ancien is not None:
        up = __ancien.update().where(
                __ancien.c.id_ancien == id_ancien
        ).values(
            nouveau = False
        )
        engine.execute(up)

        success = True

    return success



def remove_experience(id_ancien, id_experience):
    """
    Supprimer une experience, en vérifiant qu'elle est bien associée au bon ancien

    :param id_ancien:
    :param id_experience:
    :return:
    """

    suppr = __experience.delete().where(
        and_(
            __experience.c.id_ancien == id_ancien,
            __experience.c.id_experience == id_experience
        )
    )
    success = update_ancien_date(id_ancien)
    engine.execute(suppr)


def _insert_update_adresse(ville, id_pays, id_adresse, adresse="", code=""):
    """
    Mettre à jour une adresse perso ou pro, en updatant ou insérant.
    En updatant ou insérant la ville au passage

    :param id_ancien: int, id_ancien
    :param adresse: str, l'adresse en texte libre
    :param ville: str, la ville en texte libre
    :param code: int, le ocde postal en texte libre puis converti en int
    :param id_pays: int
    :return: id_adresse: l'id de l'adresse insérée / updatéee
    """
    # 2 : est-ce que la ville existe ? si non, insert !
    id_ville = None
    if helper.is_valid_integer(id_pays):
        sel = select([__ville.c.id_ville])
        sel = sel.where(and_(_slug_by_column(__ville.c.slug, helper.slugify(ville), True), __ville.c.id_pays == id_pays))
        sel = sel.distinct()
        res = engine.execute(sel).first()

        if res is not None:
            # si la ville existe, on récupère son numéro
            id_ville = res[0]

        elif (ville is not None and ville != "") and (id_pays is not None and id_pays != ""):
            # si la ville n'existe pas, mais qu'il y a un texte et un pays
            # on l'insère et on récupère son numéro
            ins = __ville.insert().values(nom=ville, slug=helper.slugify(ville), id_pays=id_pays)
            engine.execute(ins)
            sel = select([__ville.c.id_ville])
            sel = sel.where(and_(_slug_by_column(__ville.c.slug, helper.slugify(ville), True), __ville.c.id_pays == id_pays))
            res = engine.execute(sel).first()
            id_ville = res[0]

    # 3 : update (ou insert) de l'adresse
    if id_ville is not None:

        if id_adresse is not None:
            a = __adresse
            # si l'adresse existe, la mettre à jour
            up = a.update().where(a.c.id_adresse == id_adresse).values(id_ville=id_ville, adresse=adresse, code=code)

            engine.execute(up)

        else:
            a = __adresse

            # si l'adresse n'existe pas, l'insérer
            ins = a.insert().values(id_ville=id_ville, adresse=adresse, code=code)
            engine.execute(ins)

            sel = select([a.c.id_adresse]).where(and_(a.c.id_ville == id_ville, a.c.adresse == adresse, a.c.code == code))
            id_adresse = engine.execute(sel).first()[0]

    return id_adresse

def _slug_raw_input_by_column(col, raw_input=None):
    """
    Methode interne, pour comparer une str de requete au slug d'une colonne

    :param col: sqlalchemy.Column
    :param raw_input: str, raw input
    :return: col.slug == slug(raw_input)
    """
    result = None
    if col is not None:
        # traiter les recherches larges
        normal = helper.clean_normal_search(raw_input)
        if normal:
            for string in normal:
                if string is not None:
                    if result is not None:
                        result |= _slug_by_column(col, string)
                    else:
                        result = _slug_by_column(col, string)

        # traiter les recherches exactes (=entre guillements)
        exact = helper.clean_exact_search(raw_input)
        if exact:
            for string in exact:
                if string is not None:
                    if result is not None:
                        result |= _slug_by_column(col, string, True)
                    else:
                        result = _slug_by_column(col, string, True)

    return result



def _slug_by_column(col, slug=None, exact=False):
    """
    Comparer le contenu d'une colonne avec un slug

    :param col: sqlalchemy.Column
    :param slug: str, slugged
    :param exact: bool, True => comparer le mot exact ; False => comparer le mot aux mots composés du slug
    :return:    col == slug [OR col LIKE 'slug-%' OR col LIKE '%-slug' OR col LIKE '%-slug-%']
    """
    result = None

    if col is not None:
        if slug is not None:
            # recherche exacte par defaut
            result = (col == slug)
            # si ce n'est pas une recherche exacte,
            # alors on cherche sur les termes commencant/finissant par slug
            if not exact:
                result |= or_(col.like(slug + '-%'), col.like('%-' + slug), col.like('%-' + slug + '-%'))

    return result


def _where_ville(ville_raw=None, est_perso=True, est_pro=False):
    """
    Methode interne recuperer une condition de filtrage par ville, perso ou pro

    :param ville_raw: str, input raw sur lequel rechercher
    :param est_perso: recherche dans les villes perso
    :param est_pro: recherche dans les villes pro
    :return: condition SQL (ville.slug == ville_raw)
    """
    pe = __villePerso
    pr = __villePro

    result = None

    if ville_raw is not None:
        result = None

        if est_perso:
            result = _slug_raw_input_by_column(pe.c.slug, ville_raw)
        if est_pro:
            if result is None:
                result = _slug_raw_input_by_column(pr.c.slug, ville_raw)
            else:
                result |= _slug_raw_input_by_column(pr.c.slug, ville_raw)

        return result

    else:
        return None


def _where_pays(id_pays=None, est_perso=True, est_pro=False):
    """
    Methode interne recuperer une condition de filtrage par pays, perso ou pro

    :param id_pays: id du pays
    :param est_perso: recherche dans les villes perso
    :param est_pro: recherche dans les villes pro
    :return: condition SQL (pays.id_pays == id)_pays)
    """

    pe = __villePerso
    pr = __villePro

    result = None

    if id_pays is not None and type(id_pays) is int:
        result = None

        if est_perso:
            result = (pe.c.id_pays == id_pays)
        if est_pro:
            if result is None:
                result = (pr.c.id_pays == id_pays)
            else:
                result |= (pr.c.id_pays == id_pays)

        return result
    else:
        return None

def _refine_by_promo(select, promo_list=None):
    """
    Methode interne pour affiner un select par promo, en utilisant une liste de promos

    @note:
    On a une str qui represente une liste de promos ou de ranges de promos (type 2008-2010)
    si on a 2008 on fait promo = 2008
    si on a 08   on fait promo = 1908 ou promo = 2008

    :param select: le select à affiner
    :param promo_list: la liste des promos à filtrer
    :return: select WHERE promo IN promo_list
    """
    if select is not None:
        statement = None

        if promo_list is not None:
            anc = __ancien

            # on decoupe l'input par les caracteres espace
            # pour faire une list de promos
            for subset in promo_list.strip().split():
                # on redecoupe par tiret '-', pour voir si on a des promos solo
                # ou bien des ranges de promo
                sub_tab = subset.split('-')
                if len(sub_tab) > 1:
                    # si on trouve un tiret on prend les deux premiers elements
                    annee_debut = sub_tab[0]
                    annee_fin = sub_tab[1]
                elif len(sub_tab) == 1:
                    # sinon on considere qu'on a pas de fin
                    annee_debut = sub_tab[0]
                    annee_fin = None

                # si on a juste une annee
                if helper.is_valid_integer(annee_debut) and not helper.is_valid_integer(annee_fin):
                    # note : on traite les annees pour taper 08 et que ca cherche sur 2008 et 1908
                    if statement is not None:
                        statement |= _or_annee(statement, annee_debut)
                    else:
                        statement = _or_annee(statement, annee_debut)

                # si on a un range d'annees
                else:
                    if helper.is_valid_integer(annee_debut) and helper.is_valid_integer(annee_fin):
                        if statement is not None:
                            statement |= (anc.c.promo.between(annee_debut, annee_fin))
                        else:
                            statement = anc.c.promo.between(annee_debut, annee_fin)

        if statement is not None:
            return select.where(statement)

        else:
            return select

    else:
        return None

def _or_annee(statement, promo):
    """
    Methode interne pour creer un OR sur une annee de promo

    :param statement: le statement conditionnel
    :param promo: int, la promo
    :return:
        Si promo est entre 0 et 99, alors
            statement | ancien.promo == promo + 1900 | ancien.promo == promo + 2000
        else
            statement | ancien.promo == promo
    """
    anc = __ancien
    result = statement
    if promo is not None:
        promo = int(promo)
        if 0 <= promo <= 99:
            if statement is not None:
                result = statement | (anc.c.promo == (promo + 2000)) | (anc.c.promo == (promo + 1900))
            else:
                result = (anc.c.promo == (promo + 2000)) | (anc.c.promo == (promo + 1900))

        else:
            if statement is not None:
                result = statement | (anc.c.promo == promo)
            else:
                result = (anc.c.promo == promo)

    return result