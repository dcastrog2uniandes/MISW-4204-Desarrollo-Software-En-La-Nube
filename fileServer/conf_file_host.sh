#!/usr/bin/env bash

sudo apt update
sudo apt install nfs-kernel-server -y
sudo mkdir /var/nfs/Archivos -p
sudo chmod ugo+rwx /var/nfs/Archivos/
sudo copy exports /etc/
sudo systemctl restart nfs-kernel-server