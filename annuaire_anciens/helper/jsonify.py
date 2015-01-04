# coding=utf-8

import htmlentitydefs as entity
from datetime import date

def result_proxy_to_json(array=None, guillemets=False):
    """
    Parcourir un result proxy, prendre le premier élément,
    puis mettre chaque élément dans un tableau JSON. Différencie le cas "recherche
    large" et "recherche exacte" en injectant des guillemets si nécessaire.

    TODO : vérifier s'il ne faudrait pas plutôt utiliser json.dumps

    :param array: tableau
    :param guillemets: mettre des guillemets autour des termes pour une recherche exacte
    :return: array
    """

    result = "["
    for e in array:
        if guillemets and e[0].find(" ") != -1:
            before = '"\\"'
            after = '\\""'
        else:
            before = '"'
            after = '"'
        # ajouter des guillemets autour de chacun des termes
        result += before + e[0].replace("\n", "") + after
        result += ","
        # faire sauter la dernière virgule, fermer le crochet
    if len(result) > 1:
        result = result[:-1]+"]"
    else:
        result = "[]"
    return result


def row_to_json(row, excluded_keys=None):
    """
    Prendre une row de `sqlalchemy.ResultProxy`, et le transformer en dictionnaire,
    avec comme clefs les noms de colonnes.

    Attention, dans le cas spécifique des dates, qui ne sont pas JSON-isable telles
    quelles, on les formatte au format yyyyMMdd.


    Le dictionnaire est HTML-encodé.

    :param sqlalchemy.ResultProxy row:  Une row de `sqlalchemy.ResultProxy`
    :param list excluded_keys:          Les noms de colonne à exlure.
                                        Pratique dans les cas où on veut manipuler
                                        des données avant de l'envoyer au client ;
                                        mais qu'on ne veut pas envoyer toutes les
                                        données manipulées.
    :return:                            Un dictionnaire, HTML-ENCODED
    """
    d = {}

    if row is None:
        return d

    if excluded_keys is None:
        excluded_keys = []


    for key in row._parent.keys:

        # Cas 0 : Clef à ignorer
        if key in excluded_keys:
            pass

        # Cas 1 : C'est une date, la dump en string
        elif type(row[key]) is date:
            d[key] = row[key].strftime("%m/%Y")

        # Cas 2 : Tout le reste, return as-if
        else:
            d[key] = row[key]

    return d

def _decode_to_entity(u):
    """
    !! deprecated
    Transformer un unicode en ASCII html-encoded

    Cas particulier : retourne "" si u est nul

    :param u: l'entrée unicode
    :return: u.decode('ascii', 'html') (ça n'existe pas mais #yolo).
    """

    if u is not None and not isinstance(u, unicode):
        raise TypeError("Can only convert unicode, not {}".format(type(u)))

    res = ""
    for i in u:
        if ord(i) in entity.codepoint2name:
            name = entity.codepoint2name.get(ord(i))
            res += "&" + name + ";"
        else:
            res += i
    return res
