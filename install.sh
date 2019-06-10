#! /bin/bash

docker-compose build && docker-compose up -d && docker exec -it django_rest_project_docker_python_1 python manage.py fill_db
