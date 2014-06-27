# coding=utf-8
from wtforms import Form, PasswordField, validators, TextField, SelectField, TextAreaField, BooleanField
import operator
import annuaire_anciens.helper as helper
from annuaire_anciens import MAILS

class change_password_form(Form):
    """
    Form pour changer son mot de passe :
    - old_password
    - new password
    - new_passwod_confirm
    """
    old_password = PasswordField('Ancien mot de passe')
    new_password = PasswordField('Nouveau mot de passe', [validators.Required(message="Veuillez saisir un mot de passe"), validators.Length(min=6, max=25, message="Le mot de passe doit contenir entre 6 et 25 caract&egrave;res")])
    new_password_confirm = PasswordField('Confirmer mot de passe', [validators.EqualTo('new_password', message='Mots de passe diff&eacute;rents')])


class login_form(Form):
    """
    Form de login
    - mail
    - password
    """
    mail = TextField('Mail', [validators.Required()])
    password = PasswordField('Mot de passe', [validators.Required()])
    rememberme = BooleanField('Se souvenir de moi')


class registration_form(Form):
    """
    Registration form
    - mail ancien (pour vérification du compte)
    - password
    - password_confirm
    """
    mail_ancien = TextField('Mail @mines-xxx.org*', [validators.Required("Veuillez saisir une adresse de validation")])
    choices = [(k,v) for k,v in MAILS.items()] # on fait une liste [(@mines-paris.org, @mines-paris.org),...]
    domaine_ancien = SelectField('Extension', choices=choices)
    password = PasswordField('Mot de passe*', [validators.Required(message="Veuillez saisir un mot de passe"), validators.Length(min=6, max=25, message="Le mot de passe doit contenir entre 6 et 25 caract&egrave;res")])


class update_ancien_form(Form):
    """
    Form pour mettre un jour un ancien
    """
    nom = TextField('Nom')
    promo = TextField('Promo')
    diplome = TextField('Dipl&ocirc;me')
    telephone = TextField(
        'Fixe',
        [
            validators.Length(
                min=5,
                max=20,
                message="Le t&eacute;l&eacute;phone ne doit pas d&eacute;passer 20 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )

    mobile = TextField(
        'Mobile',
        [
            validators.Length(
                min=5,
                max=20,
                message="Le t&eacute;l&eacute;phone ne doit pas d&eacute;passer 20 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )

    site = TextField(
        'Site web',
        [
            validators.Length(
                min=5,
                max=200,
                message="Le site ne doit pas d&eacute;passer 200 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )
    mail_perso = TextField(
        'Mail perso',
        [
            validators.Length(
                min=5,
                max=60,
                message="Le mail ne doit pas d&eacute;passer 60 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )
    mail_asso = TextField('Mail asso')


    def load_ancien(self, ancien):
        """
        Charger un ancien dans un formulaire

        @param ancien: dict ancien à charger
        @return: None
        """
        if ancien is not None:
            if ancien['prenom'] is not None:
                self.nom.data = ancien['prenom'] + " " + ancien['nom']
            else:
                self.nom.data = ancien['nom']

            self.promo.data = ancien['ecole'] + " " + str(ancien['promo'])
            self.diplome.data = ancien['diplome']
            self.telephone.data = ancien['telephone']
            self.mobile.data = ancien['mobile']
            self.site.data = ancien['site']
            self.mail_asso.data = ancien['mail_asso']
            self.mail_perso.data = ancien['mail_perso']


class update_adresse_form(Form):
    """
    Form pour mettre à jour une adresse
    """
    adresse = TextField(
        'Adresse',
            [
                validators.Length(
                    min=0,
                    max=200,
                    message="L'adresse ne doit pas d&eacute;passer 200 caract&egrave;res"
                ),
                validators.Optional()
            ]
    )

    ville = TextField(
        'Ville',
        [
            helper.RequiredIfOther(
                'pays',
                message='Vous devez renseigner un pays ET une ville, ou aucun des deux.'
            )
        ]
    )

    code = TextField(
        'C. postal',
        [
            validators.Length(
                min=2,
                max=10,
                message="Le code doit faire entre 2 et 10 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )

    pays = SelectField(
        'Pays',
        [
            helper.RequiredIfOther('ville', message='Vous devez renseigner une ville ET un pays, ou aucun des deux.')
        ]
    )

    def load_adresse(self, adresse):
        """
        Charger l'adresse d'un ancien spécifique

        @param adresse: dict adresse à charger
        @return: None
        """
        if adresse is not None:
            self.adresse.data = adresse['adresse_adresse']
            self.code.data = adresse['adresse_code']
            self.ville.data = adresse['ville_nom']
            self.pays.data = str(adresse['pays_id_pays'])

    def set_pays(self, pays_dict):
        """
        Charger la liste des pays dans la select box

        @param pays_dict: dictionnaire json contenant la liste des pays
        @return: None
        """
        pays_sort = sorted(pays_dict.iteritems(), key = operator.itemgetter(1))
        self.pays.choices = map(lambda x: (x[0], x[1]), pays_sort)
        self.pays.choices.insert(0, ('', ''))   #blank choice


class update_experience_form(Form):
    """
    Form pour mettre à jour une expérience
    """
    entreprise = TextField('Entreprise *', [validators.Required(message="Champ obligatoire")])
    poste = TextField(
        'Poste',
            [
                validators.Length(
                    min=0,
                    max=100,
                    message="Le poste ne doit pas d&eacute;passer 100 caract&egrave;res"
                ),
                validators.Optional()
            ]
    )

    description = TextAreaField(
        'Description',
        [
            validators.Length(
                min=0,
                max=2000,
                message="La description ne doit pas d&eacute;passer 2000 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )

    ville = TextField(
        'Ville',
        [
            helper.RequiredIfOther(
                'pays',
                message='Vous devez renseigner un pays ET une ville, ou aucun des deux.'
            )
        ]
    )

    pays = SelectField(
        'Pays',
        [
            helper.RequiredIfOther('ville', message='Vous devez renseigner une ville ET un pays, ou aucun des deux.')
        ]
    )

    adresse = TextField(
        'Adresse',
        [
            validators.Length(
                min=0,
                max=200,
                message="L'adresse ne doit pas d&eacute;passer 200 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )

    code = TextField(
        'C. postal',
        [
            validators.Length(
                min=2,
                max=10,
                message="Le code doit faire entre 2 et 10 caract&egrave;res"
            ),
            validators.Optional()
        ]
    )
    date_debut = TextField(
        'Date de d&eacute;but *',
        [
            validators.Required('Date de d&eacute;but obligatoire'),
            helper.ValidDateMonth("La date d'entr&eacute;e doit &ecirc;tre au format mm/aaaa")
        ]
    )
    date_fin = TextField(
        'Date de fin',
        [
            helper.ValidDateMonth("La date de sortie doit &ecirc;tre au format mm/aaaa"),
            validators.Optional()
        ]
    )

    mail = TextField('Mail')
    site = TextField('Site')
    telephone = TextField('Telephone')
    mobile = TextField('Mobile')


    def load_experience(self, experience):
        """
        charger une experience

        @param experience: dict experience à charger
        @return: None
        """
        self.entreprise.data = experience['entreprise_nom']
        self.poste.data = experience['experience_poste']
        self.description.data = experience['experience_description']
        self.adresse.data = experience['adresse_adresse']
        self.ville.data = experience['ville_nom']
        self.code.data = experience['adresse_code']
        self.pays.data = str(experience['pays_id_pays'])
        self.site.data = experience['experience_site']
        self.telephone.data = experience['experience_telephone']
        self.mobile.data = experience['experience_mobile']
        self.mail.data = experience['experience_mail']

        self.date_debut.data = experience['experience_debut']

        self.date_fin.data = experience['experience_fin']


    def set_pays(self, pays_dict):
        """
        Charger la liste des pays dans la select box

        @param pays_dict: dictionnaire json contenant la liste des pays
        @return: None
        """
        pays_sort = sorted(pays_dict.iteritems(), key = operator.itemgetter(1))
        self.pays.choices = map(lambda x: (x[0], x[1]), pays_sort)
        self.pays.choices.insert(0, ('', ''))   #blank choice
