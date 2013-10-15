================
Annuaire anciens
================

Ceci est une application d'annuaire des Anciens,  écrite en Python.


Installation :
==============
Import de la base de données :
------------------------------
Les schémas sont disponibles dans /database . Cette application a été conçue pour utiliser PostgreSQL, mais un schéma SQLite est fourni, pour les unit tests.

*TODO* : ajouter un jeu de données basique.


Fichier de configuration :
--------------------------
Le fichier de configuration est **/annuaire_anciens/config.py**. Il est utilisé par défaut lorsqu'aucune configuration externe n'est disponible. Les instructions pour le remplir sont directement dans le fichier, en commentaire. Pensez à choisir votre propre clef secrète !

Pour utiliser une configuration externe, faire pointer la variable d'environnement **ANNUAIRE_CONFIG** vers son emplacement. Si **ANNUAIRE_CONFIG** ne pointe pas vers le fichier, ou que le fichier est incorrect, la config par défaut est utilisée. Un fichier de configuration externe est particulièrement utile pour un déploiement avec WSGI.


Lancement de l'application sans serveur web :
---------------------------------------------
Flask permet de lancer l'application sans configurer de serveur web. Il suffit de lancer **runserver.py**. L'application sera disponible sur http://localhost:5000/. Note : vérifier que le fichier de config contient bien:: 

  DEFAULT_SUBDOMAIN = ''




Technologies utilisées (prérequis) :
====================================
**Python :**

- Python 2.7 (http://python.org/)
- Flask (http://flask.pocoo.org)
- Flask-login (https://flask-login.readthedocs.org/en/latest/)
- sqlalchemy (http://www.sqlalchemy.org/)
- Psycopg2 (http://initd.org/psycopg/)
- WTForms (http://wtforms.readthedocs.org)
- requests (http://docs.python-requests.org)
- lxml (http://lxml.de/)


**UI :**

- Twitter Bootstrap (http://getbootstrap.com/)
- jQuery (http://jquery.com/)
- jQuery UI (http://jqueryui.com)/d
- Datepicker for bootstrap (http://www.eyecon.ro/bootstrap-datepicker/)


**Base de données :**

- Postgresql (http://www.postgresql.org/)
