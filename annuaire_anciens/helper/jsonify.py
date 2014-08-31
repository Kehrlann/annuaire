# coding=utf-8

import htmlentitydefs as entity


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


def row_to_json(row):
    """
    Prendre une row de `sqlalchemy.ResultProxy`, et le transformer en dictionnaire,
    avec comme clefs les noms de colonnes.

    Le dictionnaire est HTML-encodé.

    :param row: Une row de `sqlalchemy.ResultProxy`
    :return: Un dictionnaire, HTML-ENCODED
    """
    d = {}
    for key in row._parent.keys:
        if isinstance(row[key], unicode):
            d[key] = _decode_to_entity(row[key])
        else:
            d[key] = row[key]

    return d



def _decode_to_entity(u):
    """
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
