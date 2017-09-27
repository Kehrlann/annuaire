#!/bin/bash
#########
## Restore the DB backup
#########
DB_DUMP_PATH=/tmp/db/annuaire.dmp

if [ ! -f $DB_DUMP_PATH ]; then
    echo "No database dump. Please mount a volume, such that a database dump $DB_DUMP_PATH exists."
    exit 1
fi

set +e
pg_restore -U annuaire -d annuaire $DB_DUMP_PATH
set -e    

#########
## Start the app
#########
export ANNUAIRE_CONFIG=/tmp/db/config.py

if [ ! -f $ANNUAIRE_CONFIG ]; then
    echo "No config found. Please mount a volume, such that a database dump $ANNUAIRE_CONFIG exists."
    exit 1
fi

uwsgi --ini /home/annuaire/uwsgi.ini &

