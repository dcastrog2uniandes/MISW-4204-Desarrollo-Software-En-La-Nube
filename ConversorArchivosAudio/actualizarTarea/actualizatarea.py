from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request
from modelos.modelos import Usuario, db, Response, Tarea
from validacion.validacion import Validacion
import datetime

validacion = Validacion()

class ActualizarTarea(Resource):
    @jwt_required()
    def put(self):
        response = Response()
        response.Succeeded = True
        response.errors = []
        response.Estado = "UPLOADED"
        response.hora_inicio = str(datetime.datetime.now())

        validacion.validacionParametros(response, request.headers, 'id')
        validacion.validacionParametros(response, request.json, 'fileName' )
        validacion.validacionParametros(response, request.json, 'newFormat' )
        validacion.validacionExisteArchivo(response, request.json['fileName'] )
        validacion.validacionFormatoArchivo(response, request.json['fileName'] )
        validacion.validacionTamanioMax(response, request.json['fileName'] )
    

        if len(response.errors) == 0:
            nueva_tarea = Tarea(fileOriginal=request.json['fileName'], newFormat=request.json['newFormat'], status='UPLOADED', usuario=request.headers['id'])
            db.session.add(nueva_tarea)
            db.session.commit()
            response.message = "Tarea creada exitosamente"

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__