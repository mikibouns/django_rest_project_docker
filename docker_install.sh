#! /bin/bash

docker_on_ubuntu_1804() {
    echo "UBUNTU"
    # Добавляем официальный GPG-ключ Docker-а
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Проверяем fingerprint ключа
    fp=$(apt-key fingerprint 0EBFCD88 2>/dev/null | grep '9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88')

    if [ "$fp" ]
    then
      echo "Fingerprint is Ok"
    else
      echo "Bad fingerprint"
      exit
    fi

    # Настраиваем стабильный Docker-репозиторий
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    # Устанавливаем Docker
    apt-get update && apt-get install docker-ce -y
}

docker_on_debian_9() {
    echo "DEBIAN"
    # Установка дополнительных пакетов Docker
    apt-get install apt-transport-https ca-certificates curl software-properties-common

    # Добавляем ключ GPG для хранилища Docker
    wget https://download.docker.com/linux/debian/gpg
    sudo apt-key add gpg

    # Добавляем репозиторий Docker к вашей машине Debian Stretch
    echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee -a /etc/apt/sources.list.d/docker.list

    # Обновляем базу данных и установите Docker
    apt-get install docker-ce -y
}

# Определяем операционную систему и вызываем необходимую функцию
os=`lsb_release -is` # Получаем имя операционной системы

if [ "$os" == "Debian" ]
then
    docker_on_debian_9
elif [ "$os" == "Ubuntu" ]
then
    docker_on_ubuntu_1804
else
    echo "OS $os not supported"
    exit 0
fi

# Приступаем к настройке Docker в операционной системе

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


