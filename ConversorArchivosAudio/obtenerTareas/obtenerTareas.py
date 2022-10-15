from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from modelos.modelos import db, Usuario , Response, ResponseSchema, Tarea, TareaSchema
from validacion.validacion import Validacion
import datetime

response_schema = ResponseSchema()
tarea_schema = TareaSchema()
class ObtenerTareas(Resource):
    @jwt_required()
    def get(self):
        response = Response()
        response.succeded = True
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = datetime.datetime.now()
        response.message = [tarea_schema.dump(ta) for ta in Usuario.query.filter(Usuario.id == self.userId).all()[0].tareas]
        response.hora_fin = datetime.datetime.now()
        return  response_schema.dump(response)
