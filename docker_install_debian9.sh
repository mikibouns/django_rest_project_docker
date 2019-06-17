#! /bin/bash

# Установка дополнительных пакетов Docker
apt-get install apt-transport-https ca-certificates curl software-properties-common

# Добавляем ключ GPG для хранилища Docker
wget https://download.docker.com/linux/debian/gpg
sudo apt-key add gpg

# Добавляем репозиторий Docker к вашей машине Debian Stretch
echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee -a /etc/apt/sources.list.d/docker.list

# Обновляем базу данных и установите Docker
apt-get install docker-ce

# запускаем Docker
systemctl start docker

# убеждаемся, что Docker установлен правильно, запустив образ hello-world
docker run hello-world

# добавляем Docker в автозагрузку
systemctl enable docker

# добавляем своего пользователя в группу docker
usermod -aG docker $USER

# устанавливаем Docker-compose
curl -L https://github.com/docker/compose/releases/download/1.25.0-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

# устанавливаем права
chmod +x /usr/local/bin/docker-compose

# проверяем версию программы
docker-compose --version