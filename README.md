# MISW4204-202215 Grupo 4

# Entrega 2
## Pasos para montar la aplicacion en la nube:

### 1. Selecciones las VM de google y desplieguelas de acuerdo a las siguientes especificaciones:

![image](https://user-images.githubusercontent.com/98563858/198889390-98bc1462-c7ca-44d0-9b5c-5f97d540f2d9.png)

NOTA: Para la api api-conversor-archivos, se debe agregar en el firewall que permita trafico externo por el puerto 80 y que asigne una IP publica.
para todas las API se debe establecer ip fijas de acuerdo a la imagen.

![image](https://user-images.githubusercontent.com/98563858/198889441-513bf67f-7e36-47cb-b447-274368fb7e10.png)

### Una vez de creeen las VM se deben seguir los siguientes pasos:
* Ingresar a cada una de esta siguiendo las instrucciones de google para tala fin, SSH, gcloud console, etc.

Seguir los siguientes pasos en orden.

### Configurar servicio de CLOUD SQL
* Crear una instancia de mySQL.
* Permitir llamados de la UP publica, colocar la IP publica de api-conversor-archivos

### Configurar  el servidor file-server-NFS
* Ingresar a la VM.
* Escribir git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git y enter.
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube/fileServer
* Ejecutar ./conf_file_host.sh

### Configurar VM de myapp-kafka
* Ingresar a la VM.
* Escribir git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git y enter.
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejecutar ./instalar.sh
* la maquina se reinicia
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube/Docker-Cloud/Kafka/
* Ejecutar docker-compose up --build -d

### Configurar VM de api-conversor-archivos
* Ingresar a la VM.
* Escribir git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git y enter.
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube/fileServer
* Ejecutar ./conf_file_cliente.sh
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejecutar sudo apt install nginx -y
* Ejecutar sudo cp default /etc/nginx/sites-available
* Ejecutar sudo systemctl restart nginx
* Ejecutar ./instalar.sh
* la maquina se reinicia
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejcutar mv Docker-Cloud/conversorArchivosAudio/* .
* Ejecutar docker-compose up --build -d

### Configurar VM de api-convertir-archivos
* Ingresar a la VM.
* Escribir git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git y enter.
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube/fileServer
* Ejecutar ./conf_file_cliente.sh
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejecutar ./instalar.sh
* la maquina se reinicia
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejcutar mv Docker-Cloud/convertirArchivo/* .
* Ejecutar docker-compose up --build -d

### Configurar VM de api-enviar-correo
* Ingresar a la VM.
* Escribir git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git y enter.
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube/fileServer
* Ejecutar ./conf_file_cliente.sh
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejecutar ./instalar.sh
* la maquina se reinicia
* Ingresar a la carpeta cd /MISW-4204-DesarrolloNube
* Ejcutar mv Docker-Cloud/enviarCorreo/* .
* Ejecutar docker-compose up --build -d

# Entrega 1
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

La documentación de la APIREST se encuentra disponible en: [API Audio Convert](https://documenter.getpostman.com/view/14552180/2s84DssfrN)

### Stack técnológico de la APIREST

- **Framework :** Flask / Flask RESTful / Flask Marshmallow / Flask JWB Extended / Python 3.10
- **ORM:** Flask SQLAlchemy 
- **Base de Dato:** SQLite
- **Servidor HTTP WSGI:** Gunicorn
- **Servidor web HTTP:** Nginx
- **Servicios de Mensajeria:** Kafka / offset Explorer 2.0
- **Software conversor de archivos multimedia:** ffmpeg
- **Pruebas de Estrés:**  JMeter


## Prerrequisitos

- Una maquina con sistema operativo Ubuntu 22.04 con 4 CPUs y 4GB de RAM
- [Docker 20.10.20](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
- [Docker Compose 2.3.3](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)
- [Postman](https://www.postman.com/downloads/)

Opcionales
- Java: desde la terminal ejecutar el comando `sudo apt install -y default-jdk`
- [offset explorer 2.0](https://www.kafkatool.com/download.html): descargar el instalador para Ubuntu en caso de que desee visualizar los topics del broker de mensajeria Kafka
- [JMeter 5.5](https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz): descomprimir y ubicarse en la carpeta `../bin` y ejecutar el comando `./jmeter`


## Ejecución
Luego de descargar este código fuente, ubiquese en la raíz del proyecto y ejecute el comando

```
./desplegar.sh
```
Este script permite levantar los contenedores de Docker de forma automatizada.

### Configurar los Endpoints
Desde Postman debe importar las coleciones que contienen los endpoints para probar la aplicación, que se encuentran en la carpeta `/collections`. Tener en cuenta que se deben establecer las variables dependiendo del endpoint que se vaya a probar. La imagen muestra el apartado **variables** donde se deben realizar los cambios mencionados.

![image](https://user-images.githubusercontent.com/99267339/197371565-75e5dcb6-83b8-4514-b5df-94e6d4264e7d.png)

Para mayor información de los endpoints puede consultar la documentación de la [API](https://documenter.getpostman.com/view/14552180/2s84DssfrN)

## Visualización de métricas con Grafana

Una vez desplegada la aplicación, desde el navegador ingresar a la url `http://localhost:3000` y seleccione el siguiente dashboard:

![dashboard](https://user-images.githubusercontent.com/99267339/197371829-a16e4339-bc1e-425c-98d8-9411b82edc00.png)

Luego se mostraran las siguientes gráficas con los resultados

![graficos](https://user-images.githubusercontent.com/99267339/197371844-7b8159e1-1622-4dba-941f-ed89d98c0cca.png)


## Informes Entrega 1
[ver wiki](https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube/wiki)
