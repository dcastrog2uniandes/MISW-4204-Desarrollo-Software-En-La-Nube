from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from flask import request
from ConversorArchivosAudio.modelos.modelos import TareaSchema
from modelos.modelos import db, Response, ResponseSchema, Tarea
from validacion.validacion import Validacion
import datetime

response_schema = ResponseSchema()

class CrearTarea(Resource):
    @jwt_required()
    def post(self):
        response = Response()
        response.Succeeded = True
        response.errors = []
        response.Estado = "UPLOADED"
        response.hora_inicio = datetime.datetime.now()
        request_tarea = request.json

        for parametro in ['fileName', 'newFormat']:
            Validacion.validacionParametros(parametro)
            Validacion.validacionParametroObligatorio(request_tarea[parametro])

        if response.Succeeded:
            nueva_tarea = Tarea(fileConvertido=request_tarea['fileName'], newFormat=request_tarea['newFormat'], status='UPLOADED')
            db.session.add(nueva_tarea)
            db.session.commit()
            response.message = "Tarea creada exitosamente"

        response.hora_fin = datetime.datetime.now()
        return  response_schema.dump(response)