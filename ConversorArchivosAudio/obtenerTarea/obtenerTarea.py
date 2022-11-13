import sys
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from modelos.modelos import Response, Tarea, TareaSchema, FileStatus
from validacion.validacion import Validacion
import datetime
from messageBroker.messagebroker import KafkaConsumerCliente

tarea_schema = TareaSchema()
validacion = Validacion()

class ObtenerTarea(Resource):
    @jwt_required()
    def get(self, id_task):
        kafka_consumer_tareas = KafkaConsumerCliente('Respuesta')
        kafka_consumer_tareas.star_read()
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionTareaExistente(response, id_task)
        if len(response.errors) == 0:
            response.message = tarea_schema.dump(Tarea.query.filter(Tarea.id == id_task).first())
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__