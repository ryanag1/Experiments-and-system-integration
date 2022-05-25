#!/bin/ash

PATH=$(echo $PATH):/node_modules/.bin

node -e "$(cat override-packages.js)"

if [ "$SERVICE_NAME" = "frontend-dev" ]; then
    npm run serve
else
    npm run build
fi
