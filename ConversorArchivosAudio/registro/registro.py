from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask import request
from modelos.modelos import db, Usuario , Response, ResponseSchema
from validacion.validacion import Validacion
import datetime

response_schema = ResponseSchema()
class Registro(Resource):
    def post(self):
        response = Response()
        response.Succeeded = True
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = datetime.datetime.now()
        request_usuario = request.json
        for parametro in ['username', 'password1', 'password2', 'email']:
            Validacion.validacionParametros(parametro)
            Validacion.validacionParametroObligatorio(request_usuario[parametro])        
        if (request_usuario['password1'] != request_usuario['password2'] ):
            response.errors = response.errors + [{"error": { "mensaje": "Las contrasenas no coinciden", "codigo": 1000 }}]
            response.Succeeded = False
        if (len(Usuario.query.filter(Usuario.username == request_usuario['username']).all())>0):
            response.errors = response.errors + [{"error": { "mensaje": "El usuario ya se encuentra registrado", "codigo": 1001 }}]
            response.Succeeded = False
        if (len(Usuario.query.filter(Usuario.email == request_usuario['email']).all())>0):
            response.errors = response.errors + [{"error": { "mensaje": "El email ya se encuentra registrado", "codigo": 1002 }}]
            response.Succeeded = False
        if response.Succeeded:
            nuevo_usuario = Usuario(username=request_usuario["username"], password = request_usuario["password1"], email = request_usuario["email"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            response.message = "usuario creado exitosamente"
        response.hora_fin = datetime.datetime.now()
        return  response_schema.dump(response)