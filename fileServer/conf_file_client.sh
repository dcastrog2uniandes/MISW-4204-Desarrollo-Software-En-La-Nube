#!/usr/bin/env bash

sudo apt update
sudo apt install nfs-common

sudo mkdir -p /nfs/Archivos
sudo mkdir -p /nfs/home

sudo mount 10.128.0.9:/var/nfs/Archivos /nfs/Archivos
sudo mount 10.128.0.9:/home /nfs/home

df -h