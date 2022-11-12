from flask_jwt_extended import jwt_required
from flask_restful import Resource
from googleStorage.googleStorage import GoogleStorage
from modelos.modelos import db, Response, Tarea, TareaSchema, FileStatus
import datetime
from validacion.validacion import Validacion
tarea_schema = TareaSchema()
validacion = Validacion()

class EliminarTarea(Resource):
    @jwt_required()
    def delete(self, id_task):
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionTareaExistente(response, id_task)
        if len(response.errors) == 0:
            tarea = Tarea.query.filter(Tarea.id == id_task).first()
            self.__eliminarFile__(tarea)
            #response.errors = response.errors + self.__eliminarFile__(tarea)
            db.session.delete(tarea)
            db.session.commit()
            response.message = {"menssage": "Se elimino la tarea {} correctamente".format(id_task)}
            response.succeded = True

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__

    def __eliminarFile__(self, tarea):
        googleStorage = GoogleStorage()

        if validacion.validacionExisteArchivoActualizar(tarea.fileOriginal):
            googleStorage.del_file_to_bucket(tarea.fileOriginal)

        if validacion.validacionExisteArchivoActualizar(tarea.fileConvertido):
            googleStorage.del_file_to_bucket(tarea.fileConvertido)
        
