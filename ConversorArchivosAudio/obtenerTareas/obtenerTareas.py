from pickletools import int4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from modelos.modelos import db, Usuario , Response, Tarea, TareaSchemaGeneral
from validacion.validacion import Validacion
import datetime
from sqlalchemy import func


tarea_schema = TareaSchemaGeneral()
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
            validacion.validacionParametroObligatorio(response, request.headers, 'id')
            validacion.validacionNumeroEntero(response, request.headers, 'id')
            validacion.validacionIdUsuarioNoEncontrado(response, request.headers['id'])
        if validacion.validacionParametroOpcionalExistente(request.headers, 'order'):
            validacion.validacionListaDeValores(response, request.headers, 'order', ['0','1'])
        if len(response.errors) == 0:
            max_tareas = max([ta.id for ta in Tarea.query.all()])
            order_query = 0
            if validacion.validacionParametroOpcionalExistente(request.headers, 'order'):
                order_query = int(request.headers['order'])
            if validacion.validacionParametroOpcionalExistente(request.headers, 'max'):
                max_tareas = int(request.headers['max'])       
            response.message = [tarea_schema.dump(ta) for ta in (Tarea.query.filter(Tarea.usuario == int(request.headers['id'])).order_by(Tarea.id.desc()).all()\
                if order_query == 1  else Tarea.query.filter(Tarea.usuario == int(request.headers['id'])).order_by(Tarea.id.asc()).all())[0: max_tareas]]
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__