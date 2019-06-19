#! /bin/bash

# Создаем сертификаты openssl для nginx
echo "Сейчас будут созданны ssl сертификаты для NGINX, пожалуйста следуйте инструкции на экране."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./docker/nginx/nginx.key -out ./docker/nginx/nginx.crt

if [ `ls ./docker/nginx/ | grep nginx.*` ]
then
    echo "Creating certificates is done."
else
    echo "Certificates is not created."
    exit 0
fi

docker-compose build && docker-compose up -d && docker exec -it python_project python manage.py fill_dbn_