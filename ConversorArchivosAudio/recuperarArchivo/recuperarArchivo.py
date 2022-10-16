from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.modelos import Response, Tarea
from validacion.validacion import Validacion
import datetime

validacion = Validacion()

class RecuperarArchivo(Resource):
    @jwt_required()
    def get(self, filename):
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = "PROCESSED"
        response.hora_inicio = str(datetime.datetime.now())
        id_usuario = get_jwt_identity()
        validacion.validacionArchivoNoEncontrado(response, id_usuario, filename)
        if len(response.errors) == 0:
            response.message = {'ruta': [a for a in ([ta.fileOriginal for ta in Tarea.query.filter(Tarea.usuario == id_usuario).all() if ta.fileOriginal is not None] + [ta.fileConvertido for ta in Tarea.query.filter(Tarea.usuario == id_usuario).all() if ta.fileConvertido is not None]) if a.split('/')[-1] == filename][0] }
            response.succeded = True
        return response.__dict__