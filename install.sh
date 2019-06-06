#! /bin/bash

docker-compose build && docker-compose up -d && docker exec -it dev_path_python_1 python manage.py fill_db