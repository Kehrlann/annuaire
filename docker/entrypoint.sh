#!/bin/bash
service nginx start
su annuaire -c "/home/annuaire/start_app.sh"

exec "$@"
while true; do sleep 1; done

