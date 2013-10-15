# coding=utf-8
from annuaire_anciens import app
from datetime import date, datetime
from jinja2 import evalcontextfilter, Markup

@app.template_filter('int_to_str')
def int_to_str_filter(i):
    """
    Pour concatener des str et des int dans jinja
    """
    if i is not None and type(i) is int:
        return str(i)
    else:
        return ''

@app.template_filter('escape_none')
def escape_none(input_text):
    """
    Pour afficher une str != None
    @param input: string
    @return: str if str, '' if not str
    """
    if input_text:
        return input_text
    else:
        return ''

@app.template_filter('count')
def count(array):
    """
    compter le nombre d'éléments d'un tableau
    @param array:
    @return: nombre d'éléments d'un tableau
    """
    if array is not None:
        return len(array)
    else:
        return 0

@app.template_filter('count_not_null')
def count_not_null(array):
    """
    compter le nombre d'éléments NON NULS d'un tableau
    @param array:
    @return: nombre d'éléments d'un tableau
    """
    if array is not None:
        res = 0
        for element in array:
            if element is not None:
                res = res + 1
        return res
    else:
        return 0


@app.template_filter('hidden')
def hidden(token):
    """
    pour afficher un Cross-Site Request Forgery token
    @param token:
    @return: <input name="_csrf_token" type="hidden" value="'+str(token)+'">
    """
    if token is not None:
        return '<input id="_csrf_token" name="_csrf_token" type="hidden" value="'+str(token)+'">'

@app.template_filter('default_date')
def default_date(date_input):
    """
    vérifie que l'input est une date ; sinon mettre today
    @param string:
    @return: string if not None or str(date.today())
    """
    if date_input is None:
        date_input = date.today()
    return date_input


@app.template_filter('date_to_month')
def date_to_month(date_input):
    """
    transforme une date 1999-03-25 en date 03/1999.
    ignore les dates déjà formattées

    @param string: une string sous la forme 1999-03-25
    @return: date
    """
    try:
        # cas 1 : c'est une date
        result = date_input.strftime("%m/%Y")
    except Exception:
        try:
            # Cas 2 : c'est une str au format %m/%Y. Si on arrive à la convertir, alors return la string directement
            datetime.strptime(date_input, "%m/%Y")
            result = date_input
        except Exception:
            # Sinon return rien
            result = ""
    return result

@app.template_filter('nl2br')
@evalcontextfilter
def nl2br(eval_ctx, value):
    """
    Transforme les sauts de ligne (\n) dans une string en sauts de ligne HTML (<br />)
    @param string_input:
    @return:
    """
    result = ""
    if value is not None:
        result = value.replace('\n',u'<br />')
        if eval_ctx.autoescape:
            result = Markup(result)
    return result

@app.template_filter('to_http')
def to_http(value):
    """
    Permet de rajouter http:// devant un lien, SI celui-ci manque.
    @param value: valeur du lien
    @return: http://+value
    """
    res = ""
    if value is not None and value != '':
        if value.startswith("http://") or value.startswith("https://"):
            res = value
        else:
            res = "http://" + value
    return res