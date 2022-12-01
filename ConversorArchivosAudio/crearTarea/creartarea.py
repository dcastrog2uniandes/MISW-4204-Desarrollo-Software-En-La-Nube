from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from modelos.modelos import Usuario, db, Response, Tarea, TareaSchema, FileStatus
from validacion.validacion import Validacion
from messageBroker.messagebroker import KafkaProducerCliente
import datetime
from googleStorage.googleStorage import GoogleStorage
import os

folder_original_name = os.environ.get('GOOGLE_APPLICATION_BUCKET_FOLDER_NAME', None)
if folder_original_name is None:
    folder_original_name = 'ArchivoOriginal/'

folder_conversion_name = os.environ.get('GOOGLE_APPLICATION_BUCKET_FOLDER_CONVERSION_NAME', None)
if folder_conversion_name is None:
    folder_conversion_name = 'ArchivoConversion/'

validacion = Validacion()
tarea_schema = TareaSchema()

class CrearTarea(Resource):
    @jwt_required()
    def post(self):
        id_usuario = get_jwt_identity()
        response = Response()
        googleStorage = GoogleStorage()
        response.Succeeded = True
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.json, 'fileName')
        validacion.validacionParametros(response, request.json, 'newFormat')

        if len(response.errors) == 0:
            file = googleStorage.copy_blob(request.json['fileName'], folder_original_name + request.json['fileName'].split('/')[-1])
            validacion.validacionFormatoArchivo(response, '.' + file.name.split('.')[-1])
            validacion.validacionTamanioMax(response, file.size)
            
        if len(response.errors) == 0:
            name_file = request.json['fileName'].split('/')[-1]
            googleStorage.del_file_to_bucket(request.json['fileName'])
            usuario_tarea = Usuario.query.filter( Usuario.id == int(id_usuario)).first()
            
            nueva_tarea = Tarea(fileCliente=request.json['fileName'], fileConvertido=folder_conversion_name + name_file.split('.')[-2] + request.json['newFormat'], fileOriginal=folder_original_name + name_file, newFormat=request.json['newFormat'], status=FileStatus.UPLOADED.name, usuario=id_usuario)
            db.session.add(nueva_tarea)
            db.session.commit()
            response.message = "Tarea creada exitosamente"
            json_response = {
                "tarea": tarea_schema.dump(Tarea.query.filter(Tarea.id == nueva_tarea.id).first()),
                "usuario": {
                                "id": usuario_tarea.username,
                                "email": usuario_tarea.email
                           }
                }
            kafka_producer = KafkaProducerCliente()
            kafka_producer.enviarTarea(str(nueva_tarea.id), json_response)
        else:
            googleStorage.del_file_to_bucket(folder_original_name + request.json['fileName'].split('/')[-1])

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__
