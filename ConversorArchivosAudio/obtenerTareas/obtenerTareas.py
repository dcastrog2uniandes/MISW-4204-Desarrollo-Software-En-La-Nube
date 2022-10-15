from flask_restful import Resource
from flask import request
from modelos.modelos import db, Usuario , Response, ResponseSchema
from validacion.validacion import Validacion
import datetime

response_schema = ResponseSchema()
class ObtenerTareas(Resource):
    def post(self):
        response = Response()
        response.succeded = True
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = datetime.datetime.now()
        request_ = request.json
        for parametro in ['username', 'password1', 'password2', 'email']:
            if Validacion.validacionParametros( request_usuario, parametro) is not None:
                response.errors = response.errors + [{'error': Validacion.validacionParametros( request_usuario, parametro)}]
                response.succeded = False
            elif Validacion.validacionParametroObligatorio(request_usuario[parametro]) is not None:
                   response.errors = response.errors + [{'error': Validacion.validacionParametroObligatorio(request_usuario[parametro])}]
                   response.succeded = False
        if (Validacion.validacionParametros( request_usuario, 'email') is None) and (Validacion.validacionFormatoEmail(request_usuario['email']) is not None):
            response.errors = response.errors + [{"error": Validacion.validacionFormatoEmail(request_usuario['email'])}]
            response.succeded = False
        if (Validacion.validacionParametros( request_usuario, 'password1') is None) and (Validacion.validacionParametros( request_usuario, 'password2') is None) and (request_usuario['password1'] != request_usuario['password2']):
            response.errors = response.errors + [{"error": { "mensaje": "Las contrasenas no coinciden", "codigo": 1000 }}]
            response.succeded = False
        if (Validacion.validacionParametros( request_usuario, 'username') is None) and (len(Usuario.query.filter(Usuario.username == request_usuario['username']).all())>0):
            response.errors = response.errors + [{"error": { "mensaje": "El usuario ya se encuentra registrado", "codigo": 1001 }}]
            response.succeded = False
        if (Validacion.validacionParametros( request_usuario, 'email') is None) and (len(Usuario.query.filter(Usuario.email == request_usuario['email']).all())>0):
            response.errors = response.errors + [{"error": { "mensaje": "El email ya se encuentra registrado", "codigo": 1002 }}]
            response.succeded = False
        if response.succeded:
            nuevo_usuario = Usuario(username = request_usuario["username"], password = request_usuario["password1"], email = request_usuario["email"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            response.message = "usuario creado exitosamente"
        response.hora_fin = datetime.datetime.now()
        return  response_schema.dump(response)
