from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request
from modelos.modelos import Usuario, db, Response, Tarea
from validacion.validacion import Validacion
from messageBroker.messagebroker import KafkaProducer
import pathlib
import datetime

validacion = Validacion()
kafka_producer = KafkaProducer()


class CrearTarea(Resource):
    @jwt_required()
    def post(self):
        response = Response()
        response.Succeeded = True
        response.errors = []
        response.Estado = "UPLOADED"
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.headers, 'id')
        validacion.validacionParametros(response, request.json, 'fileName')
        validacion.validacionParametros(response, request.json, 'newFormat')

        if len(response.errors) == 0:
            validacion.validacionExisteArchivo(response, request.json['fileName'])
            validacion.validacionFormatoArchivo(response, request.json['fileName'])
            validacion.validacionTamanioMax(response, request.json['fileName'])
            validacion.validacionNumeroEntero(response, request.headers, 'id')

        if len(response.errors) == 0:
            usuario_tarea = Usuario.query.filter(
                Usuario.id == int(request.headers['id'])).first()
            nueva_tarea = Tarea(fileOriginal=request.json['fileName'], newFormat=request.json['newFormat'], status='UPLOADED', usuario=request.headers['id'])
            db.session.add(nueva_tarea)
            db.session.commit()
            response.message = "Tarea creada exitosamente"
            json_response = {
                'tarea': nueva_tarea.id,
                'usurio': {'id': request.headers['id'],
                           'email': usuario_tarea.email
                           },
                'filepath': request.json['fileName'],
                'newFormat': request.json['newFormat']
            }

            kafka_producer.enviarTarea('Tareas', str(nueva_tarea.id), json_response)

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__
