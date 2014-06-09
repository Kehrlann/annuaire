#coding=utf-8
"""
Ceci est la config par défaut de l'application. Pour utiliser votre propre configuration, copier ce fichier,
puis le référencer avec la variable d'environnement INTERMINES_CONFIG.
"""


# General
APP_NAME = "PA's app"  # Nom de l'appli, pour être sûr de bien avoir chargé la config
SERVER_NAME = "localhost:5000"   # Host. Les callbacks LinkedIn sont faits sur cette adresse
DEFAULT_SUBDOMAIN = ""   # Subdomain principal de l'appli, pour le routing Flask. Peut être www.default
SECRET_KEY = "%830q1>d?qw:" # Clef secrete pour signer les cookies de session
SESSION_COOKIE_PATH = "/"

LOGIN_DISABLED = False      # Forcer flask.ext.login à utiliser le login. Par défaut, en TESTING, est = True

# Debug
DEBUG = False       # Mode DEBUG de flask. En production, toujours = FALSE
DEBUG_SQL = False   # Mode DEBUG de sqlalchemy (verbeux)

# Database URI, plus d'info : http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html#sqlalchemy.create_engine
DATABASE_URI = "postgresql+psycopg2://localhost:5432/annuaire"

# Upload
UPLOAD_FOLDER = "/Users/paduc/Desktop"                   # Dossier où uploader les photos d'ancien
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Formats de photo autorisés
MAX_CONTENT_LENGTH = 2 * 1024 * 1024                # Taille maximale des requêtes

# email
SMTP_SERVER = 'host:port'   # SMTP server, par exemple smtp.gmail.com:587
SMTP_USERNAME = 'username'  # Utilisateur SMTP
SMTP_PASSWORD = 'password'  # Mot de passe SMTP

# google analytics
GOOGLE_ANALYTICS = None     # Script javascript à inclure dans les pages pour GA. Si = None, pas de google Analytics
JQUERY_CDN = None           # Adresse du CDN jQuery à utiliser. Si = None, utilisation de la ressource locale
JQUERY_UI_CDN = None        # Adresse du CDN jQuery UI à utiliser. Si = None, utilisation de la ressource locale
BOOTSTRAP_CSS_CDN = None    # Adresse du CDN Bootstrap.css à utiliser. Si = None, utilisation de la ressource locale
BOOTSTRAP_JS_CDN = None     # Adresse du CDN Bootstrap.js à utiliser. Si = None, utilisation de la ressource locale

# LinkedIn
LINKEDIN_KEY = "key"                                # Clef API linkedin
LINKEDIN_SECRET = "secret"                          # Secret Linkedin
LINKEDIN_SCOPE = "r_basicprofile%20r_fullprofile"   # Infos profil LinkeDin. full_profile pour avoir les expériences

# logging
LOGFILE="local/annuaire.log"     # Fichier de log