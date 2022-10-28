#!/usr/bin/env bash

sudo apt update
sudo apt autoremove
sudo apt install nfs-kernel-server -y
sudo mkdir /var/nfs/Archivos -p
sudo chmod ugo+rwx /var/nfs/Archivos/
sudo cp exports /etc/
sudo systemctl restart nfs-kernel-server

sudo mkdir /var/nfs/Archivos/ArchivoCliente -p
sudo chmod ugo+rwx /var/nfs/Archivos/ArchivoCliente

sudo mkdir /var/nfs/Archivos/ArchivoConversion -p
sudo chmod ugo+rwx /var/nfs/Archivos/ArchivoConversion

sudo mkdir /var/nfs/Archivos/ArchivoOriginal -p
sudo chmod ugo+rwx /var/nfs/Archivos/ArchivoOriginal

