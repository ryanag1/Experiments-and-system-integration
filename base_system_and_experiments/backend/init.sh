#!/bin/bash

rm -rf .pid/
envsubst '172.0.1.10 "http://DOMAINNAME/","http://DOMAINNAME/","https://DOMAINNAME/","https://DOMAINNAME/"' < /usr/src/app/config/config_server.ini.template > /usr/src/app/config/config_server.ini
python -m ducts server start -c ./config/config_server.ini &

if [ "$SERVICE_NAME" = "backend-dev" ]; then
    watchmedo shell-command -W -R -p '*.py' --ignore-patterns="projects/*/*" -c 'echo ${watch_src_path}; python -m ducts server stop && python -m ducts server start -c ./config/config_server.ini' ./
else
    /bin/bash
fi
