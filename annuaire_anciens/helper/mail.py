#coding=utf-8
import smtplib
from email.mime.text import MIMEText
from annuaire_anciens import app

_SMTP_SERVER = app.config['SMTP_SERVER']
_SMTP_USERNAME = app.config['SMTP_USERNAME']
_SMTP_PASSWORD = app.config['SMTP_PASSWORD']
_SERVER_NAME = app.config['SERVER_NAME']

if 'DEFAULT_SUBDOMAIN' in app.config and 'DEFAULT_SUBDOMAIN' != '' and 'DEFAULT_SUBDOMAIN' != None:
    _SERVER_NAME = app.config['DEFAULT_SUBDOMAIN'] + "." + _SERVER_NAME


def send_activation_mail(to, id_ancien, activation_code):
    """
    Envoyer le mail d'activation du compte d'ancien
    @param to: destinataire
    @param activation_code: code d'activation, à insérer dans le mail.
    @return: None
    """
    message = \
        u'Bonjour !\n\n' \
        u'Vous avez demandé l\'ouverture d\'un compte sur http://mines-alumni.com. Afin de l\'activer, ' \
        u'veuillez cliquer sur le lien ci-dessous :\n' \
        u'http://%s/activation/%s/%s\n\n' \
        u'Cordialement,\n' \
        u'L\'équipe mines-alumni' % (_SERVER_NAME,id_ancien,activation_code)
    _send_mail("no-reply@mines-alumni.com", to, "Mines-Alumni : Activation de votre compte", message)


def _send_mail(sender, recipient, subject, message):
    """
    Envoyer un mail.
    Crée un MIMEText avec le message, et met les autres champs dans les headers.

    @param sender: adresse d'émission
    @param recipient: destinataire
    @param subject: sujet du mail
    @param message:
    @return: None
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