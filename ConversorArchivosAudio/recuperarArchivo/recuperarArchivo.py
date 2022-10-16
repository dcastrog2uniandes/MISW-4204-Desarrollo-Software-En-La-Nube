from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
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
        validacion.validacionParametros(response, request.headers, 'id')
        if len(response.errors) == 0:
            validacion.validacionParametroObligatorio(response, request.headers, 'id')
            validacion.validacionNumeroEntero(response, request.headers, 'id')
            validacion.validacionIdUsuarioNoEncontrado(response, request.headers['id'])
        if len(response.errors) == 0:
            validacion.validacionArchivoNoEncontrado(response, request.headers['id'], filename)
        if len(response.errors) == 0:
           response.message = {'ruta': ([ta.fileOriginal for ta in Tarea.query.all() if ta.fileOriginal.split('/')[-1] == filename] + [ta.fileConvertido for ta in Tarea.query.all() if ta.fileConvertido.split('/')[-1] == filename])[0]}
        return response.__dict__