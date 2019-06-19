#! /bin/bash

docker-compose build && docker-compose up -d && docker exec -it python_project python manage.py fill_dbn_