# coding=utf-8
def result_proxy_to_json(array=None, guillemets=False):
    """
    Parcourir un tableau, puis mettre chaque élément dans un tableau JSON

    @param array: tableau
    @param guillemets: mettre des guillemets autour des termes pour une recherche exacte
    @return: array
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