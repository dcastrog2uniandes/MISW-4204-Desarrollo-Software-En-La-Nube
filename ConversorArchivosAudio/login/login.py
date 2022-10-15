from tokenAutorizacion.token import  Token
from flask_restful import Resource
from flask import request
from modelos.modelos import db, Usuario, Response, ResponseSchema
from validacion.validacion import Validacion
import datetime

response_schema = ResponseSchema()
class Login(Resource):
    def post(self):
        response = Response()
        response.succeded = True
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = datetime.datetime.now()
        request_usuario = request.json
        for parametro in ['username', 'password']:
            if Validacion.validacionParametros( request_usuario, parametro) is not None:
                response.errors = response.errors + [{'error': Validacion.validacionParametros( request_usuario, parametro)}]
                response.succeded = False
            elif Validacion.validacionParametroObligatorio(request_usuario[parametro]) is not None:
                   response.errors = response.errors + [{'error': Validacion.validacionParametroObligatorio(request_usuario[parametro])}]
                   response.succeded = False
        if response.succeded:
            usuario = Usuario.query.filter(Usuario.username == request_usuario["username"],
                                       Usuario.password == request_usuario["password"]).first()
            if usuario is None:
                response.errors = response.errors + [{'error': {'mensaje': 'No se encuentra el usuario.', 'codigo': 1007}}]
                response.succeded = False
            else:
                response.message = {'token': Token.crearToken(usuario.id), 'userId': usuario.id}
        response.hora_fin = datetime.datetime.now()
        return response_schema.dump(response)