#! /bin/bash


# Удаление Docker-ce и Docker-compose
apt-get purge docker-ce -y
apt-get purge docker-compose -y
apt-get autoremove -y
apt-get autoclean

# Если вы хотите удалить все изображения, контейнеры и тома, выполните следующую команду
rm -rf /var/lib/docker

# Удалить докер из apparmor.d
rm /etc/apparmor.d/docker

# Удалить группу докеров
groupdel docker