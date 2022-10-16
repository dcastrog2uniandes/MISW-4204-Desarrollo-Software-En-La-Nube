from pickletools import int4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.modelos import db, Usuario , Response, Tarea, TareaSchemaGeneral
from validacion.validacion import Validacion
import datetime
from sqlalchemy import func


tarea_schema = TareaSchemaGeneral()
validacion = Validacion()

class ObtenerTareas(Resource):
    @jwt_required()
    def get(self):
        id_usuario = get_jwt_identity()
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.args, 'order')

        if len(response.errors) == 0:
            validacion.validacionParametroObligatorio(response, request.args, 'order')
            if validacion.validacionParametroOpcionalExistente(request.args, 'max'):
                validacion.validacionParametroObligatorio(response, request.args, 'max')

        if len(response.errors) == 0:
            validacion.validacionListaDeValores(response, request.args, 'order', ['0', '1'])
            if validacion.validacionParametroOpcionalExistente(request.args, 'max'):      
                validacion.validacionNumeroEntero(response, request.args, 'max')

        if len(response.errors) == 0:
            max_tareas = max([ta.id for ta in Tarea.query.all()])
            order_query = int(request.args['order'])
            if validacion.validacionParametroOpcionalExistente(request.args, 'max'):
                max_tareas = int(request.args['max'])       
            response.message = [tarea_schema.dump(ta) for ta in (Tarea.query.filter(Tarea.usuario == id_usuario).order_by(Tarea.id.desc()).all()\
                if order_query == 1  else Tarea.query.filter(Tarea.usuario == id_usuario).order_by(Tarea.id.asc()).all())[0: max_tareas]]
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__