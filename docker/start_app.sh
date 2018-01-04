#!/bin/bash
export ANNUAIRE_CONFIG=/tmp/config.py

if [ ! -f $ANNUAIRE_CONFIG ]; then
    echo "No config found. Please mount a volume, such that a config file $ANNUAIRE_CONFIG exists in the image."
    exit 1
fi

uwsgi --ini /home/annuaire/uwsgi.ini &

