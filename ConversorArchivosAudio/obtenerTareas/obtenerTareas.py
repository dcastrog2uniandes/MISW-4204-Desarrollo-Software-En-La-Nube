from pickletools import int4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from modelos.modelos import db, Usuario , Response, Tarea, TareaSchema
from validacion.validacion import Validacion
import datetime


tarea_schema = TareaSchema()
validacion = Validacion()

class ObtenerTareas(Resource):
    @jwt_required()
    def get(self):
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.headers, 'id')
        if len(response.errors) == 0:
            print(type(request.headers['id']))
            validacion.validacionParametroObligatorio(response, request.headers, 'id')
            validacion.validacionNumeroEntero(response, request.headers, 'id')
        if len(response.errors) == 0:
            response.message = [tarea_schema.dump(ta) for ta in Tarea.query.filter(Tarea.usuario == int(request.headers['id'])).all()]
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__