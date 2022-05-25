#!/bin/sh

chmod +rx /var/www/html/dist

envsubst '' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx

certbot --nginx -d DOMAINNAME -m EMAILADDRESS --agree-tos -n
certbot renew
nginx -s reload

/bin/sh
