# coding=utf-8
import operator
from wtforms import Form, TextField, SelectField, BooleanField, RadioField

class SearchForm(Form):
    """
    Le formulaire de recherche de l'annuaire, avec
    - prenom (str)
    - nom (str)
    - ecole (int)
    - promo (str)
    - ville (str)
    - pays (int)
    - pro (bool)
    - perso (bool)
    - entreprise (str)
    """
    prenom = TextField('Pr&eacute;nom')
    nom = TextField('Nom')
    ecole = SelectField('Ecole')
    promo = TextField('Promo')
    ville = TextField('Ville')
    pays = SelectField('Pays')
    entreprise = TextField('Entreprise')
    adresse = RadioField('Adresses', choices=[('perso','perso uniquement'),('pro','pro uniquement'),('deux','les deux')], default='deux')


    def setEcole(self, ecole_dict):
        """
        Charger la liste des écoles dans le formulaire
        @param ecole_dict: dict contenant la liste des "ecole.id" : "ecole.nom"
        @return: None
        """
        self.ecole.choices = map(lambda x:(x,ecole_dict.get(x)),ecole_dict)
        #blank choice
        self.ecole.choices.insert(0, ('', ''))

    def setPays(self, pays_dict):
        """
        Charger la liste des pays dans le formulaire
        @param pays_dict: dict contenant la liste des "pays.id" : "pays.nom"
        @return: None
        """
        pays_sort = sorted(pays_dict.iteritems(), key = operator.itemgetter(1))
        self.pays.choices = map(lambda x: (x[0], x[1]), pays_sort)
        #blank choice
        self.pays.choices.insert(0, ('', ''))