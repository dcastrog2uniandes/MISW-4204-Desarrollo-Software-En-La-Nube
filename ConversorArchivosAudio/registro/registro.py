from flask_restful import Resource
from flask import request
from modelos.modelos import db, Usuario , Response, FileStatus
from validacion.validacion import Validacion
from messageBroker.messagebroker import KafkaConsumer
import datetime

validacion = Validacion()

class Registro(Resource):

    def post(self):
        kafka_consumer_tareas = KafkaConsumer()
        kafka_consumer_tareas.recibirTareas()
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.json, 'username')
        validacion.validacionParametros(response, request.json, 'password1')
        validacion.validacionParametros(response, request.json, 'password2')
        validacion.validacionParametros(response, request.json, 'email')
        if len(response.errors) == 0:
            validacion.validacionParametroObligatorio(response, request.json, 'username')
            validacion.validacionParametroObligatorio(response, request.json, 'password1')
            validacion.validacionParametroObligatorio(response, request.json, 'password2')
            validacion.validacionParametroObligatorio(response, request.json, 'email')
            validacion.validacionFormatoEmail(response, request.json['email'])
            validacion.validacionCoincidenPasswords(response, request.json['password1'], request.json['password2'])
        if len(response.errors) == 0:
            validacion.validacionUsernameExistente(response, request.json['username'])
            validacion.validacionEmailExistente(response, request.json['email'])
        if len(response.errors) == 0:
            nuevo_usuario = Usuario(username = request.json["username"], password = request.json["password1"], email = request.json["email"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            response.message = "usuario creado exitosamente"
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__
  