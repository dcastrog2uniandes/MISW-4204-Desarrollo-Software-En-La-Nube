# MISW-4204-DesarrolloNube

## Instalar ffmpeg

Es un proyecto de software de código abierto gratuito que consta de un gran conjunto de bibliotecas y programas para manejar video, audio y otros archivos multimedia.

```
sudo apt-get install ffmpeg 
```

## Instalar offset explorer 2.0

Desde la pagina oficial https://www.kafkatool.com/download.html descargar el instalador para Ubuntu

### Instalar Java

Apache Kafka requiere Java para ejecutarse. Ejecute el siguiente comando para instalar OpenJDK predeterminado en su sistema desde los repositorios oficiales de Ubuntu.

```
sudo apt install -y default-jdk
```

## Levantar los servicios Zookeeper y Kafka 

Desde la carpeta ```/docker``` levantar las imagenes docker con el comando
```
docker compose up -d
```

## Levantar Microservicios
A continuación se listas los microservicios 

| Microservicios         | Puerto | Comando                                                       |
|------------------------|--------|---------------------------------------------------------------|
| ConversorArchivosAudio | 5000   | ```gunicorn --bind 0.0.0.0:5000 wsgi:ap```                    |
| ConvertirArchivo       | 5001   | ```gunicorn --bind 0.0.0.0:5001 -w 1 --timeout 600 wsgi:ap``` |
| EnviarCorreo           | 5002   | ```gunicorn --bind 0.0.0.0:5002 -w 1 --timeout 600 wsgi:ap``` |

## Instalar dependencias proyecto flask
Desde la carpeta raiz ejecutar el comando

```
pip3 install -r requirements.txt
```
