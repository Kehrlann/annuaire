from flask.ext.login import UserMixin

__author__ = 'dgarnier-moiroux'

class Utilisateur(UserMixin):

    def __init__(self, id_user, mail, id_ancien):
        self.id = id_user
        self._mail = mail
        self._id_ancien = id_ancien

    @property
    def mail(self):
        return self._mail

    @property
    def id_ancien(self):
        return self._id_ancien