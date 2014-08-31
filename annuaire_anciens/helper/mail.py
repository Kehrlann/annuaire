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
        u'Vous avez demandé l\'ouverture d\'un compte sur https://mines-alumni.com. Afin de l\'activer, ' \
        u'veuillez cliquer sur le lien ci-dessous :\n' \
        u'https://%s/activation/%s\n\n' \
        u'Cordialement,\n' \
        u'L\'équipe mines-alumni' % (_SERVER_NAME, activation_code)
    _send_mail("no-reply@mines-alumni.com", to, "Mines-Alumni : Activation de votre compte", message)


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