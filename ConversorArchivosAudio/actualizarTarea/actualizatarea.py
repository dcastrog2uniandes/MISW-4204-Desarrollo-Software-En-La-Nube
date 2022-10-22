from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from modelos.modelos import Usuario, db, Response, Tarea, TareaSchema, FileStatus
from validacion.validacion import Validacion
from messageBroker.messagebroker import KafkaProducer
from eliminarFile.eliminarFile import EliminarFile 
import datetime

validacion = Validacion()
tarea_schema = TareaSchema()

class ActualizarTarea(Resource):
    @jwt_required()
    def put(self, id_task):
        kafka_producer = KafkaProducer()
        id_usuario = get_jwt_identity()
        response = Response()
        response.Succeeded = True
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.json, 'newFormat')
        validacion.validacionTareaExistente(response, id_task)

        if len(response.errors) == 0:  
            tarea_actualizar = Tarea.query.filter(Tarea.id == id_task).first()  
            validacion.validacionFormatoArchivoDestino(response, tarea_actualizar.fileOriginal, request.json['newFormat'] )
            
        if len(response.errors) == 0:
            if tarea_actualizar.status == FileStatus.PROCESSED.name and validacion.validacionExisteArchivo(tarea_actualizar.fileConvertido):
                eliminarFile = EliminarFile()
                eliminarFile.eliminar(tarea_actualizar.fileConvertido)


            name_file = tarea_actualizar.fileConvertido.split('/')[-1].split('.')[-2]

            tarea_actualizar.fileConvertido='../Archivos/ArchivoConversion/'+name_file+request.json['newFormat']
            tarea_actualizar.newFormat=request.json['newFormat']
            tarea_actualizar.status=FileStatus.PROCESSED.name
            db.session.commit()
            
            response.message = "Tarea actualizada exitosamente"
            usuario_tarea = Usuario.query.filter( Usuario.id == int(id_usuario)).first()

            json_response = {
                'tarea': tarea_schema.dump(tarea_actualizar),
                'usuario': {
                                'id': usuario_tarea.username,
                                'email': usuario_tarea.email
                           }
                }

            kafka_producer.enviarTarea('Tareas', str(tarea_actualizar.id), json_response)

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__
