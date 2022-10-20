from tokenAutorizacion.token import  Token
from flask_restful import Resource
from flask import request
from modelos.modelos import db, Usuario, Response, FileStatus
from validacion.validacion import Validacion
from messageBroker.messagebroker import KafkaConsumer
import datetime

validacion = Validacion()
class Login(Resource, object):
    def post(self):
        kafka_consumer_tareas = KafkaConsumer()
        kafka_consumer_tareas.recibirTareas()
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.json, 'username')
        validacion.validacionParametros(response, request.json, 'password')
        if len(response.errors) == 0:
            validacion.validacionParametroObligatorio(response, request.json, 'username')
            validacion.validacionParametroObligatorio(response, request.json, 'password')
        if len(response.errors) == 0:
            validacion.validacionUsuarioNoEncontrado(response, request.json['username'])
        if len(response.errors) == 0:
            validacion.validacionContrasenaUsuario(response, request.json['username'], request.json['password'])
        if len(response.errors) == 0:
            usuario = Usuario.query.filter(Usuario.username == request.json["username"],
                            Usuario.password == request.json["password"]).first()
            response.message = {'token': Token.crearToken(usuario.id), 'id': usuario.id}
            response.succeded = True

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__