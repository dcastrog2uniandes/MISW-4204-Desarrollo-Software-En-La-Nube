from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.modelos import Response, Tarea, FileStatus
from validacion.validacion import Validacion
from messageBroker.messagebroker import KafkaConsumer
import datetime
import shutil

validacion = Validacion()

class RecuperarArchivo(Resource):
    @jwt_required()
    def get(self, filename):
        kafka_consumer_tareas = KafkaConsumer()
        kafka_consumer_tareas.recibirTareas()
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        id_usuario = get_jwt_identity()
        validacion.validacionArchivoNoEncontrado(response, id_usuario, filename)
        if len(response.errors) == 0:
            filepath = [a for a in ([ta.fileOriginal for ta in Tarea.query.filter(Tarea.usuario == id_usuario).all() if ta.fileOriginal is not None] + [ta.fileConvertido for ta in Tarea.query.filter(Tarea.usuario == id_usuario).all() if ta.fileConvertido is not None]) if a.split('/')[-1] == filename][0]
            validacion.validacionExisteArchivo(response, filepath)
        if len(response.errors) == 0:
            validacion.validacionArchivoNoEstaDescargado(response, '../Archivos/ArchivoCliente', filename)
        if len(response.errors) == 0:
            ruta_destino = shutil.copy(filepath, '../Archivos/ArchivoCliente')
            response.message = 'El archivo fue recuperado en la ruta ' + ruta_destino 
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__