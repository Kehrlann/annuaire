#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from annuaire_anciens import app

_SMTP_SERVER = app.config['SMTP_SERVER']
_SMTP_USERNAME = app.config['SMTP_USERNAME']
_SMTP_PASSWORD = app.config['SMTP_PASSWORD']
_SERVER_NAME = app.config['SERVER_NAME']

if 'DEFAULT_SUBDOMAIN' in app.config and app.config['DEFAULT_SUBDOMAIN'] != '' and app.config['DEFAULT_SUBDOMAIN'] != None:
    _SERVER_NAME = app.config['DEFAULT_SUBDOMAIN'] + "." + _SERVER_NAME


def send_activation_mail(to, activation_code):
    """
    Envoyer le mail d'activation du compte

    :param to: destinataire
    :param activation_code: code d'activation, à insérer dans le mail.
    :return: None
    """
    message = \
        u'Bonjour !\n\n' \
        u'Tu as demandé l\'ouverture d\'un compte sur https://mines-alumni.com. Afin de l\'activer, ' \
        u'merci de cliquer sur le lien ci-dessous :\n' \
        u'https://%s/activation/%s\n\n' \
        u'Cordialement,\n' \
        u'L\'équipe mines-alumni' % (_SERVER_NAME, activation_code)
    _send_mail("no-reply@mines-alumni.com", to, "Mines-Alumni : Activation de ton compte", message)


def send_reset_password_mail(to, activation_code):
    """
    Envoyer le mail de reset d'un mot de pass

    :param to: destinataire
    :param activation_code: code d'activation, à insérer dans le mail.
    :return:
    """
    message = \
        u'Bonjour !\n\n' \
        u'Tu as demandé un reset de mot de passe sur https://mines-alumni.com. Pour compléter la procédure, ' \
        u'merci de cliquer sur le lien ci-dessous :\n' \
        u'https://%s/reset/%s\n\n' \
        u'Cordialement,\n' \
        u'L\'équipe mines-alumni' % (_SERVER_NAME, activation_code)
    _send_mail("no-reply@mines-alumni.com", to, "Mines-Alumni : Reset de ton mot de passe", message)


def send_fiche_activee_mail(to):
    """
    Envoyer un mail de notification à un ancien que sa fiche a été activée sur le
    site.

    :param str to: destinataire
    """
    message = \
        u'Bonjour !\n\n' \
        u'Ta fiche ancien sur https://mines-alumni.com vient d\'être validée par un administrateur. ' \
        u'Tu apparaîtras désormais dans les résultats des recherches dans l\'annuaire. Pour mettre ta fiche' \
        u'à jour, ou la retirer des résultats de recherche, connecte-toi sur le site et clique sur "mon compte".\n\n' \
        u'Cordialement,\n' \
        u'L\'équipe mines-alumni'
    _send_mail("no-reply@mines-alumni.com", to, "Mines-Alumni : Validation de ta fiche ancien", message)


def _send_mail(sender, recipient, subject, message):
    """
    Envoyer un mail.
    Crée un MIMEText avec le message, et met les autres champs dans les headers.

    :param sender: adresse d'émission
    :param recipient: destinataire
    :param subject: sujet du mail
    :param message:
    :return: None
    """
    msg = MIMEText(message.encode('UTF-8'))
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    s = smtplib.SMTP(_SMTP_SERVER)
    s.starttls()
    s.login(_SMTP_USERNAME,_SMTP_PASSWORD)
    s.sendmail(_SMTP_USERNAME, recipient, msg.as_string())
    s.quit()