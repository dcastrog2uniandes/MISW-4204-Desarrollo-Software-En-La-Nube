#!/usr/bin/env bash

echo "Se baja todos container correspondientes desplegados por docker compose"
docker compose down

echo "Se elimina las imagenes correspondientes desplegados por docker compose"
docker rmi api_conversor_archivos_audio:1
docker rmi api_convertir_archivo:1
docker rmi api_enviar_correo:1

echo "Se ejecuta para crea las imagenes"
docker compose build

echo "Se ejecuta para desplegar las imagenes"
docker compose up -d