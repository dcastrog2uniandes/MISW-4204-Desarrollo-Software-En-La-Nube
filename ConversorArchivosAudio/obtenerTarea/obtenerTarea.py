from flask_restful import Resource
from flask_jwt_extended import jwt_required
from modelos.modelos import db, Usuario , Response, Tarea, TareaSchema
from validacion.validacion import Validacion
import datetime


tarea_schema = TareaSchema()
validacion = Validacion()

class ObtenerTarea(Resource):
    @jwt_required()
    def get(self, id_task):
        response = Response()
        response.succeded = True
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = str(datetime.datetime.now())
        response.message = tarea_schema.dump(Tarea.query.filter(Tarea.id == id_task).first())        
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__