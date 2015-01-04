# coding=utf-8
from flask import Flask
import config

# Création de l'app SANS static folder. On le crée à posteriori, pour le lier au subdomain
app = Flask(__name__, static_url_path="")

# Chargement de la config par défaut
app.config.from_object(config)

# Écraser la config par défaut si possible avec la variable d'environnement INTERMINES_CONFIG
try:
    app.config.from_envvar('ANNUAIRE_CONFIG')
    print "Loaded external config for : " + app.config['APP_NAME']
except RuntimeError as rte:
    print "error loading the external config, it should be specified in env_var : ANNUAIRE_CONFIG"
except IOError as ioe:
    print "the confing file specified in ANNUAIRE_CONFIG doesn't exist"

# Préparer le logging, dans un fichier tel que spécifié dans la config
if 'LOGFILE' in app.config and not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOGFILE'], maxBytes=1024 * 1024 * 10, backupCount=20)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

# subdomain
if 'DEFAULT_SUBDOMAIN' in app.config:
    app.url_map.default_subdomain = app.config['DEFAULT_SUBDOMAIN']

# ajout du dossier static, qui sera créé dans le sous-domaine
app.static_folder = 'static'
app.add_url_rule('/static/<path:filename>',
              endpoint='static',
              view_func=app.send_static_file)

# sql engine
from sqlalchemy import create_engine
engine = create_engine(app.config['DATABASE_URI'], echo=app.config['DEBUG_SQL'])

# test engine
engine.execute("select 1").scalar()
connection = engine.connect()

import os
os.chdir(os.path.dirname(__file__))
import json
# Get ecoles
with open('var/ecoles.json','r') as f:
    ECOLES = json.load(f)

# Get pays
with open('var/pays.json', 'r') as f:
    PAYS = json.load(f)

# Get adresses écoles
with open('var/mails.json', 'r') as f:
    MAILS = json.load(f)


# Default objects
SUCCESS = { "success" : True }
FAILURE = { "success" : False }

# Forms
import wtforms_json
wtforms_json.init()


# attacher les filtres et les vues à l'application
import helper.filters
import views

# configurer google analytics, google CDN, etc
app.jinja_env.globals['google_analytics'] = app.config['GOOGLE_ANALYTICS']
app.jinja_env.globals['jquery_cdn'] = app.config['JQUERY_CDN']
app.jinja_env.globals['jquery_ui_cdn'] = app.config['JQUERY_UI_CDN']
app.jinja_env.globals['bootstrap_css_cdn'] = app.config['BOOTSTRAP_CSS_CDN']
app.jinja_env.globals['bootstrap_js_cdn'] = app.config['BOOTSTRAP_JS_CDN']
app.jinja_env.globals['app_name'] = app.config['APP_NAME']


# Jinja plugin
app.jinja_env.add_extension("jinja2.ext.do")

connection.close()

print ""
print "=> 3..."
print "=====> 2..."
print "=========> 1..."
print "=============> Blast off !"
print ""