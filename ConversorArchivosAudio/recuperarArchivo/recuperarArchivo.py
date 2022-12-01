from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from googleStorage.googleStorage import GoogleStorage
from modelos.modelos import Response, Tarea, FileStatus
from validacion.validacion import Validacion
import datetime
import os

validacion = Validacion()
folder_cliente_name = os.environ.get('GOOGLE_APPLICATION_BUCKET_FOLDER_CLIENTE_NAME', None)
if folder_cliente_name is None:
    folder_cliente_name = 'ArchivoCliente/'

class RecuperarArchivo(Resource):
    @jwt_required()
    def get(self, filename):
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        id_usuario = get_jwt_identity()
        validacion.validacionArchivoNoEncontrado(response, id_usuario, filename)
        if len(response.errors) == 0:
            filepath = [a for a in ([ta.fileOriginal for ta in Tarea.query.filter(Tarea.usuario == id_usuario).all() if ta.fileOriginal is not None] + [ta.fileConvertido for ta in Tarea.query.filter(Tarea.usuario == id_usuario).all() if ta.fileConvertido is not None]) if a.split('/')[-1] == filename][0]
            if validacion.validacionExisteArchivoActualizar(filepath):
                googleStorage = GoogleStorage()
                googleStorage.copy_blob(filepath, folder_cliente_name + filename)
                response.message = 'El archivo ' + filename +  ' fue recuperado en la ruta del bucket ' + folder_cliente_name 
                response.succeded = True    
            response.hora_fin = str(datetime.datetime.now())
        return response.__dict__
