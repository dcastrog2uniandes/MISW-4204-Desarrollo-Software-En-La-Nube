# MISW4204-202215 Grupo 4

# Entrega 3 - Sistema Conversión Cloud - Escalabilidad en la Capa Web

En el proyecto se debe habilitar las siguientes [APIs de Google](https://console.cloud.google.com/apis/library?project=IdProyecto):

1. `Cloud Storage JSON API`
2. `Cloud Storage`

Se debe crear las credenciales para el consumo de la APIs.Genere las credenciales en formato `json` y guardelo en la carpeta `/Key` con el nombre `credencial_google.json`

__Nota:__ Tenga en cuenta que debe partir de la configuración de la __Entrega # 2__

## Pasos para configurar Autoescalamiento de la Capa Web

### Crear imagen
Se debe crear una imagen de arranque con un disco de origen basado en la `api-conversor-archivos` para la creación dinámica de instancias al momento de realizar AutoScalling. Desde el menú principal de la consola de GPC ir a: _Compute Engine_ -> _almacenamiento_ -> _imagenes_ -> y _crear nueva imagen_ con la siguiente especificaciones:

<div align="center">

| Campo              | Valor                    |
|--------------------|--------------------------|
| origen             | Disco                    |
| Disco origen       | api-conversor-archivos   |
| Ubicación          | Regional                 |
| Seleccionar región | us-central1 (lowa)       |

</div>
     
### Crear plantilla de instancia
Desde el menú principal de la consola de GPC ir a: _Compute Engine_ -> _Plantillas de instancia_ y _Crear Plantillas de Intancias_ con las siguientes especificaciones:

<div align="center">
     
| Campo             | Valor                                                                |
|-------------------|----------------------------------------------------------------------|
| Serie             | N1                                                                   |
| Tipo de Maquina   | f1-micro (1 vCPU / 614MB)                                            |
| Disco de arranque | imagen personalizada (seleccionar imagen creada en el paso anterior) |
     
</div>

### Crear Grupo de Instancias (MIG)
Desde el menú principal de la consola de GPC ir a: _Compute Engine_ -> _Grupo de Instancias_ -> _Crear Grupo de Instancias_ -> _New Managed Instance Group (stateless)_ e ingrese la siguiente configuración:

<div align="center">
     
| Campo                       | Valor                                              |
|-----------------------------|----------------------------------------------------|
| nombre                      | _nombre-grupo_                                     |
| Instance template           | Seleccionar el template creado en el paso anterior |
| Ubicación                   | Zona única                                         |
| Región                      | us-central1- (lowa)                                |
| Zona                        | us-central1-a                                      |
| Número minimo de instancias | 1                                                  |
| Número máximo de instancias | 3                                                  |
| Autoscaling Metrics         | Agregar las métricas deseadas                      |
| Periodo de Inactividad      | 120s                                               |
| Agregar Puerto              | 80                                                 |

</div>

### Crear Balanceador de Carga
Desde el menú principal de la consola de GPC ir a: _Compute Engine_ -> _Herramientas de Redes_ -> _Servicios de red_ -> _Balanceo de cargas_ -> _Crear Balanceador de Cargas_ -> _Balanceador de cargas HTTP(S)_. Para crear el balanceador es necesario crear un _servicio de backend_ y un _servicio de verificación de estado_. Estos están incluidos en el formulario principal al crear el balanceador. Use la siguientes especificaciones. 

<div align="center">
     
| Campo                          | Valor                                  |
|--------------------------------|----------------------------------------|
| nombre                         | _nombre_servicio_                      |
| Tipo de Backend                | Grupo de instancias                    |
| Protocolo                      | HTTP                                   |
| Grupo de instancias            | Selecionar grupo creado en el paso anterior       |
| Número de puerto               | 80                                     |
| Modo de balanceo               | Utilización                            |
| Utilización máxima del backend | 80%                                    |
| Máximo de RPS                  | 10                                     |
| Capacidad                      | 100%                                   |
| Verificación de estado         | Crear con la configuración por defecto | 

</div>

### Agregar Servicio de Monitoring
Desde el menú principal de la consola de GPC ir a: _Compute Engine_ -> _Herramientas de Redes_ -> _Monitoring_ -> _Descripción general_ -> _Instalar un agente_ -> _Configurar agentes_ y seleccionar la(s) instancia(s) en las que se va a instalar este servicio. Finalmente click en _Instalar el Agente de Operaciones_

##### Configuración adicional arranque instancias de VM
En la instancia `api-conversor-archivos` se deben ejecutar los siguientes comandos para que en caso de reiniciarse o hacer uso de esta imagen para la generación dinámica de instancias estas tengan los permisos necesarios para acceder al sistema de archivos. 

```
sudo chmod u+x start.sh
sudo cp start.sh /etc/init/d
cd /etc/rc2.d
sudo ln -s /etc/init.d/start.sh
sudo mv start.sh S70start.sh
```

### Informes Entrega 3
[ver wiki](https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube/wiki)

# Entrega 2 - Sistema Conversión Cloud - Despliegue Básico en la Nube Pública
## Pasos para desplegar la aplicación en la nube de Google:

### 1. Cree instancias de VM en la consola de GCP y desplieguelas de acuerdo a las siguientes especificaciones:

<div align="center">
     
| API - Microservicio    | Servicio     | Serie | Tipo maquina              | Disco de Arranque       | IP           |
|------------------------|--------------|-------|---------------------------|-------------------------|--------------|
| api-conversor-archivos* | Instancia VM | N1    | f1-micro (1 vCPU / 614MB) | Ubuntu 18.04 / 10GB SSD | `10.128.0.6`   |
| api-convertir-archivos  | Instancia VM | N1    | f1-micro (1 vCPU / 614MB) | Ubuntu 18.04 / 10GB SSD | `10.128.0.4`   |
| api-enviar-correo      | Instancia VM | N1    | f1-micro (1 vCPU / 614MB) | Ubuntu 18.04 / 10GB SSD | `10.128.0.5`   |
| file-server-nfs        | Instancia VM | N1    | f1-micro (1 vCPU / 614MB) | Ubuntu 18.04 / 10GB SSD | `10.128.0.9`   |
| myapp-kafka            | Instancia VM | E2    | e2-small (2 vCPU / 2GB)   | Ubuntu 18.04 / 10GB SSD | `10.128.0.2`   |
| jmeter-test            | Instancia VM | E2    | e2-small (2 vCPU / 2GB)   | Ubuntu 18.04 / 10GB SSD | `10.128.0.7`   |
| bd-conversor-audior**    | Cloud SQL    | MySQL | 4 vCPU                    | 26GB / 100GB SSD        | `34.27.228.33` |

</div>

**Zona:** us-central1-a

*_firewall_ que permita tráfico externo por el puerto `80` y que asigne una IP pública.

**Permite llamados de la IP pública de la _api-conversor-archivos_

Todas las instancias de VM debe tener IP fijas (ip efimera personalizada) de acuerdo a la tabla.



## Una vez se creen las VM, debe ingresar a cada una (vía SSH o gcloud console) y siga los siguientes pasos en **orden**.

### 1. Configurar servicio de _Cloud SQL_
1. Crear una instancia de MySQL. Configúrela para que permita llamados de la IP pública de la _api-conversor-archivos_
      * id de instancia: `bd-conversor-audio`
      * contraseña: `admin123456`
      * configuracion: `development`
      * ip pública: `xx.xxx.xxx.xx` (ip pública api-conversor-archivos)
      * versión: `MySQL 8.0`
      
2. Cree una base de datos con el nombre `conversorAudio` 
      
3. Verificar la conexión a la base de datos. Desde la terminal de `gcloud` ejecute el comando `gcloud sql connect bd-conversor-audio --user=root`
4. Escribir la contraseña y verifique que se abra el shell de MySQL

### 2. Configurar el servidor _file-server-nfs_
1. Ingresar a la VM.
2. Ejecutar el comando `git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git`
3. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube/fileServer`
4. Ejecutar `./conf_file_host.sh`

### 3. Configurar VM _myapp-kafka_
1. Ingresar a la VM.
2. Ejecutar el comando `git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git`
3. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
4. Ejecutar `./instalar.sh`
5. En este punto la maquina se reinicia, debe volver a restablecer la conexión (SSH o gcloud console)
6. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube/Docker-Cloud/Kafka/`
7. Ejecutar `docker-compose up --build -d`

### 4. Configurar VM _api-conversor-archivos_
1. Ingresar a la VM.
2. Ejecutar `git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git`
3. Editar el archivo `docker-compose.yml` que se encuentra en `cd /MISW-4204-DesarrolloNube`. Cambie las variables `PUBLIC_IP_ADDRESS` y `PROJECT_ID` de acuerdo con la ip pública de la **base de datos** y el **id del proyecto**, respectivamente. 

      ```
      ...
      api-conversorArchivosAudio:
        environment:
          - PUBLIC_IP_ADDRESS=xx.xxx.xxx.xx
          - PROJECT_ID=id-proyecto-gcp
      ...
      ```
4. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube/fileServer`
5. Ejecutar `./conf_file_client.sh`
6. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
7. Ejecutar `sudo apt install nginx -y`
8. Ejecutar `sudo cp default /etc/nginx/sites-available`
9. Ejecutar `sudo systemctl restart nginx`
10. Ejecutar `./instalar.sh`
11. En este punto la maquina se reinicia, debe volver a restablecer la conexión (SSH o gcloud console)
12. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
13. Ejecutar `mv Docker-Cloud/conversorArchivosAudio/* .`
14. Ejecutar `docker-compose up --build -d`

### 5. Configurar VM _api-convertir-archivos_
1. Ingresar a la VM.
2. Ejecutar `git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git`
3. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube/fileServer`
4. Ejecutar `./conf_file_client.sh`
5. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
6. Ejecutar `./instalar.sh`
7. En este punto la maquina se reinicia, debe volver a restablecer la conexión (SSH o gcloud console)
8. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
9. Ejecutar `mv Docker-Cloud/convertirArchivo/* .`
10. Ejecutar `docker-compose up --build -d`

### 6. Configurar VM _api-enviar-correo_
1. Ingresar a la VM.
2. Ejecutar `git clone https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube.git`
3. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube/fileServer`
4. Ejecutar `./conf_file_client.sh`
5. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
6. Ejecutar `./instalar.sh`
7. En este punto la maquina se reinicia, debe volver a restablecer la conexión (SSH o gcloud console)
8. Ingresar a la carpeta `cd /MISW-4204-DesarrolloNube`
9. Ejecutar `mv Docker-Cloud/enviarCorreo/* .`
10. Ejecutar `docker-compose up --build -d`

## Informes Entrega 2
[ver wiki](https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube/wiki)

# Entrega 1 - Sistema Conversión Cloud - Entorno Tradicional

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

## Pasos para desplegar la aplicación en un ambiente local
### Prerrequisitos

- Una maquina con sistema operativo Ubuntu 22.04 con 4 CPUs y 4GB de RAM
- [Docker 20.10.20](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
- [Docker Compose 2.3.3](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)
- [Postman](https://www.postman.com/downloads/)

Opcionales
- Java: desde la terminal ejecutar el comando `sudo apt install -y default-jdk`
- [offset explorer 2.0](https://www.kafkatool.com/download.html): descargar el instalador para Ubuntu en caso de que desee visualizar los topics del broker de mensajeria Kafka
- [JMeter 5.5](https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz): descomprimir y ubicarse en la carpeta `../bin` y ejecutar el comando `./jmeter`


### Ejecución
Luego de descargar este código fuente, ubiquese en la raíz del proyecto y ejecute el comando

```
./desplegar.sh
```
Este script permite levantar los contenedores de Docker de forma automatizada.

#### Configurar los Endpoints
Desde Postman debe importar las coleciones que contienen los endpoints para probar la aplicación, que se encuentran en la carpeta `/collections`. Tener en cuenta que se deben establecer las variables dependiendo del endpoint que se vaya a probar. La imagen muestra el apartado **variables** donde se deben realizar los cambios mencionados.

![image](https://user-images.githubusercontent.com/99267339/197371565-75e5dcb6-83b8-4514-b5df-94e6d4264e7d.png)

Para mayor información de los endpoints puede consultar la documentación de la [API](https://documenter.getpostman.com/view/14552180/2s84DssfrN)

### Visualización de métricas con Grafana

Una vez desplegada la aplicación, desde el navegador ingresar a la url `http://localhost:3000` y seleccione el siguiente dashboard:

![dashboard](https://user-images.githubusercontent.com/99267339/197371829-a16e4339-bc1e-425c-98d8-9411b82edc00.png)

Luego se mostraran las siguientes gráficas con los resultados

![graficos](https://user-images.githubusercontent.com/99267339/197371844-7b8159e1-1622-4dba-941f-ed89d98c0cca.png)


### Informes Entrega 1
[ver wiki](https://github.com/mcgomeztuniandes/MISW-4204-DesarrolloNube/wiki)
