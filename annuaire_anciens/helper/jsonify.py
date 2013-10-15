# coding=utf-8
def result_proxy_to_json(array=None, guillemets=False):
    """
    Parcourir un tableau, puis mettre chaque élément dans un tableau JSON

    @param array: tableau
    @param guillemets: mettre des guillemets autour des termes pour une recherche exacte
    @return: array
    """
    before = '"'
    after = '"'
    if guillemets:
        before = '"\\"'
        after = '\\""'
    result = "["
    for e in array:
        # ajouter des guillemets autour de chacun des termes
        result += before + e[0].replace("\n", "") + after
        result += ","
    # faire sauter la dernière virgule, fermer le crochet
    if len(result) > 1:
        result = result[:-1]+"]"
    else:
        result = "[]"
    return result