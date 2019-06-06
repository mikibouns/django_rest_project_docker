#! /bin/bash

# добавляем официальный GPG-ключ Docker-а
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# проверяем fingerprint ключа
fp=$(apt-key fingerprint 0EBFCD88 2>/dev/null | grep '9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88')

if [ "$fp" ]
then
  echo "Fingerprint is Ok"
else
  echo "Bad fingerprint"
  exit
fi

# настраиваем стабильный Docker-репозиторий
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# устанавливаем Docker
apt-get update && apt-get install docker-ce -y

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
