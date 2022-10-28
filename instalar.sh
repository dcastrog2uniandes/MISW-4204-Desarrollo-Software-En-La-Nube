#!/usr/bin/env bash

echo "Instalar docker"

sudo apt update

sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

sudo apt update

apt-cache policy docker-ce

sudo apt install docker-ce -y

sudo usermod -aG docker ${USER}

id -nG

sudo usermod -aG docker miltongomezt

sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version

# echo "Instalar nginx"

# sudo apt install nginx -y

# sudo cp default /etc/nginx/sites-available

# sudo systemctl restart nginx

sudo reboot -f