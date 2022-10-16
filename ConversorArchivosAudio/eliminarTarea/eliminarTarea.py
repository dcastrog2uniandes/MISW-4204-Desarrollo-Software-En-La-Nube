from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos.modelos import db, Response, Tarea, TareaSchema, FileStatus
from eliminarFile.eliminarFile import EliminarFile
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
            response. errors = response.errors + self.__eliminarFile__(tarea)
            db.session.delete(tarea)
            db.session.commit()
            response.message = {"menssage": "Se elimino la tarea {} correctamente".format(id_task)}
            response.succeded = True

        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__

    def __eliminarFile__(self, tarea):
        responseFile = Response()
        responseFile.errors = []
        eliminarFile = EliminarFile()
        if tarea.status == FileStatus.PROCESSED:
            validacion.validacionExisteArchivo(responseFile, tarea.fileConvertido)

            if len(responseFile.errors) == 0:
                eliminarFile.eliminar(tarea.fileConvertido)

            return responseFile.errors