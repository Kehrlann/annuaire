from flask.ext.login import UserMixin


class Utilisateur(UserMixin):

    def __init__(self, id_user, mail, id_ancien, actif, admin):
        self.id = id_user
        self._mail = mail
        self._id_ancien = id_ancien
        self._actif = actif
        self._admin = admin

    @property
    def mail(self):
        return self._mail

    @property
    def id_ancien(self):
        return self._id_ancien

    @property
    def actif(self):
        return self._actif

    @property
    def admin(self):
        return self._admin