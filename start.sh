#!/usr/bin/env bash
DIR=/home/$(whoami)/MISW-4204-DesarrolloNube

sudo mkdir -p /nfs/Archivos
sudo mkdir -p /nfs/home

sudo mount 10.128.0.9:/var/nfs/Archivos /nfs/Archivos
sudo mount 10.128.0.9:/home /nfs/home

cp -r ../Archivos/* /nfs/Archivos
df -h

docker-compose -f $DIR/docker-compose.yml down
docker-compose -f $DIR/docker-compose.yml up -d