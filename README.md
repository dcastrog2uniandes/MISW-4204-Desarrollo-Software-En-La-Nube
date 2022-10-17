# MISW4204-202215

## Conversor de Audio

Back-end de una aplicación web tipo APIREST que permite a los usuarios subir archivos de audio y solicitar el cambio de formato de estos para descargarlos. La aplicación permite a un usuario registrarse con un correo electronico, usuario y contraseña. Debido a que no se cuenta con un front-end, se utiliza POSTMAN para probar cada uno de los endpoints del APIREST. La aplicación permite el procesamiento de conversión de archivos de audio para los siguientes 3 formatos:

- MP3
- OGG
- WAV

Los servicios REST expuestos por la aplicación son los siguientes:

| Método HTTP | Nombre                                              | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POST        | Registro Usuario                                    | Permite crear una cuenta de usuario en la aplicaicón. Los campos solicitados son un usuario, correo electrónico y contraseña. El correo debe ser único en la plataforma.                                                                                                                                                                                                                                                                            |
| POST        | Iniciar sesión                                      | Por medio del correo electronico y la contraseña, se retorna un token de sesión para validar la identidad del usuario lo que le permitirá utilizar los recursos de la aplicación                                                                                                                                                                                                                                                                    |
| GET         | Tareas de conversión disponibles                    | Retorna todas las tareas de conversión. El servicio entrega el identificador de la tarea, el nombre y la extensión del archivo original, a qué extensión desea convertir y si está disponible o no. El usuario debe proveer el token de autenticación para realizar dicha operación                                                                                                                                                                 |
| POST        | Cambiar formato de archivo cargado por el usuario   | El usuario debe proveer el archivo que desea convertir, el formato al cual desea cambiarlo y el token de autenticación para realizar dicha operación. El archivo debe ser almacenado en la plataforma, se debe guardar en base datos la marca de tiempo en el que fue subido el archivo y el estado del proceso de conversión (uploaded o processed). Cuando el archivo se termina de procesar se debe notificar al usuario vía correo electrónico. |
| GET         | Información tarea                                   | Retorna la información de una tarea de conversión específica                                                                                                                                                                                                                                                                                                                                                                                        |
| GET         | Descargar archivo                                   | Permite recuperar/descargar el archivo que original o el archivo procesado de un usuario                                                                                                                                                                                                                                                                                                                                                            |
| PUT         | Cambiar formato archivo disponible en la aplicación | Permite cambiar el nuevo formato de conversión de un archivo que esté disponible en la aplicación. Si el estado del proceso de conversión es “processed”, se debe actualizar el estado a “uploaded”, y borrar el archivo procesado anteriormente. El usuario debe proveer el identificador de la tarea, indicar el nuevo formato. Cuando el archivo se termina de procesar se debe notificar al usuario vía correo electrónico                      |
| DELETE      | Borrar archivos                                     | Permite borrar el archivo original y el archivo convertido de un usuario, si y sólo si el estado del proceso de conversión es Disponible. El usuario debe proveer el identificador de la tarea                                                                                                                                                                                                                                                      |

La documentación de la APIREST se encuentra disponible en una colección de POSTMAN

### Stack técnológico de la APIREST

- **Framework :** Flask / Flask RESTful / Flask Marshmallow / Flask JWB Extended / Python 3.10
- **ORM:** Flask SQLAlchemy 
- **Base de Dato:** SQLite
- **Servidor HTTP WSGI:** Gunicorn
- **Servidor web HTTP:** Nginx
- **Servicios de Mensajeria:** Kafka / offset Explorer 2.0
- **Software conversor de archivos multimedia:** ffmpeg
- **Pruebas de Estrés:**  JMeter

## Servidor de Desarrollo


### Instalar dependencias proyecto flask
Desde la carpeta raiz ejecutar el comando

```
pip3 install -r requirements.txt
```

### Instalar ffmpeg

Es un proyecto de software de código abierto gratuito que consta de un gran conjunto de bibliotecas y programas para manejar video, audio y otros archivos multimedia.

```
sudo apt-get install ffmpeg 
```

#### Instalar offset explorer 2.0

Desde la pagina oficial https://www.kafkatool.com/download.html descargar el instalador para Ubuntu

#### Instalar Java

Apache Kafka requiere Java para ejecutarse. Ejecute el siguiente comando para instalar OpenJDK predeterminado en su sistema desde los repositorios oficiales de Ubuntu.

```
sudo apt install -y default-jdk
```

### Levantar los servicios Zookeeper y Kafka 

Desde la carpeta ```/docker``` levantar las imagenes docker con el comando
```
docker compose up -d
```

### Levantar Microservicios
Teniendo en cuenta la arquitectura diseñada, se listas los microservicios y los puertos donde se ejecutan:

| Microservicio          | Puerto | Comando                                                       |
|------------------------|--------|---------------------------------------------------------------|
| ConversorArchivosAudio | 5000   | ```gunicorn --bind 0.0.0.0:5000 wsgi:ap```                    |
| ConvertirArchivo       | 5001   | ```gunicorn --bind 0.0.0.0:5001 -w 1 --timeout 600 wsgi:ap``` |
| EnviarCorreo           | 5002   | ```gunicorn --bind 0.0.0.0:5002 -w 1 --timeout 600 wsgi:ap``` |

## Análisis de Capacidad
.....

## Plan de pruebas
....

## Ejecución Pruebas de Estrés 
.....

### Escenario 1
....

### Escenario 2
....



### Resultados
Se encuentra en un documento disponible en la wiki: Escenario y Pruebas de Estrés API REST y Batch
