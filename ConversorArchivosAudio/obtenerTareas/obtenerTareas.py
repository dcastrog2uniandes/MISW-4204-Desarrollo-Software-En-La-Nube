from pickletools import int4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modelos.modelos import db, Usuario , Response, Tarea, TareaSchemaGeneral, FileStatus
from validacion.validacion import Validacion
import datetime
from sqlalchemy import func
from messageBroker.messagebroker import KafkaConsumerCliente

tarea_schema = TareaSchemaGeneral()
validacion = Validacion()

class ObtenerTareas(Resource):
    @jwt_required()
    def get(self):
        kafka_consumer_tareas = KafkaConsumerCliente('Respuesta')
        kafka_consumer_tareas.star_read()
        id_usuario = get_jwt_identity()
        response = Response()
        response.succeded = False
        response.errors = []
        response.Estado = FileStatus.PROCESSED.name
        response.hora_inicio = str(datetime.datetime.now())
        validacion.validacionParametros(response, request.args, 'order')
        existe_max = validacion.validacionParametroOpcionalExistente(request.args, 'max')
        if len(response.errors) == 0:
            validacion.validacionParametroObligatorio(response, request.args, 'order')
            if existe_max:
                validacion.validacionParametroObligatorio(response, request.args, 'max')

        if len(response.errors) == 0:
            validacion.validacionListaDeValores(response, request.args, 'order', ['0', '1'])
            if existe_max:      
                validacion.validacionNumeroEntero(response, request.args, 'max')

        if len(response.errors) == 0:
            validacion.validacionUsuarioSinTareas(response, id_usuario)

        if len(response.errors) == 0:
            order_query = int(request.args['order'])
            tareas_usuario = Tarea.query.filter(Tarea.usuario == id_usuario).order_by(Tarea.id.desc()).all() if order_query == 1 \
                            else Tarea.query.filter(Tarea.usuario == id_usuario).order_by(Tarea.id.asc()).all()
            
            if existe_max:
                max_tareas = int(request.args['max'])
            else:
                max_tareas = len(tareas_usuario)

            response.message = [tarea_schema.dump(ta) for ta in tareas_usuario][0: max_tareas]
            response.succeded = True
        response.hora_fin = str(datetime.datetime.now())
        return response.__dict__