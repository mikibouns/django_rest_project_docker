# django_rest_project_docker

##Установка и настройка
####Требования
+ OC Ubuntu 18.04
+ Docker-ce 18.09.6
+ Docker-compose 1.25.0-rc1

####Подготовка
*C помощью файла* [docker_install_ubuntu1804.sh](https://github.com/mikibouns/django_rest_project_docker/blob/master/docker_install_ubuntu1804.sh) *происходит установка и настройка docker-ce и docker-compose*
```buildoutcfg
sudo chmod +x docker_install_ubuntu1804.sh
sudo ./docker_install_ubuntu1804.sh
```
####Установка и настройка проекта
*Выполняем следующие команды находясь в корне проекта (django_rest_project_docker)*
```buildoutcfg
sudo chmod +x install.sh
sudo ./install.sh
```
В результате выполнения скрипта [install.sh](https://github.com/mikibouns/django_rest_project_docker/blob/master/install.sh) будут установлены и запущенны следующие компоненты:
+ [postgres:10.8](https://hub.docker.com/_/postgres)
+ [adminer](https://hub.docker.com/_/adminer/)
+ [python:3.6](https://hub.docker.com/_/python)
+ [nginx](https://hub.docker.com/_/nginx/)


После [установки и настройки](#Установка-и-настройка) проекта вам будет доступна панель администрирования http://your_hostname/admin/ и RootAPI http://your_hostname/api/v1/.

Учетные данные суперпользователя: 
```
login: administ
password: Testtest123
```

## Авторизация и аутентификация

Регистрация нового пользователя:

+ URL: http://your_hostname/api/v1/users/
+ method: POST
>Request
```buildoutcfg
{
  "address": "<string>",
  "fio": "<string>",
  "password": "<string>"
}
```
>Response
```
{
    "success": 1,
    "user_id": 8,
    "token": "35edb217ece459a3175ffe4995627bef4c085b0e"
}
```

Как получить токен зарегестрированному пользователю:
+ URL: http://your_hostname/api/v1/get_token/
+ method: POST
>Request
```buildoutcfg
{
  "username": "<string>",
  "password": "<string>"
}
```
>Response
```buildoutcfg
{
  "token": "1d7bdc13b9f7fe39355d9811f20abec461ce884d"
}
```
Аутентификация токеном, пример:
```
curl -X GET http://your_hostname/api/v1/users/ -H "Authorization: Token 1d7bdc13b9f7fe39355d9811f20abec461ce884d"
```

## Документация

Для документирования API использовал:
+ Django-rest-swagger 
+ Самоописывающий API DRF
+ Встроенную документацию для API DRF
