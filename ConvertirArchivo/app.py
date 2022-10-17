
from flask import Flask
from .messageBroker import KafkaConsumer
from flask_restful import Api

kafka_consumer_tareas = KafkaConsumer()

app = Flask(__name__)

app_context = app.app_context()
app_context.push()
api = Api(app)

kafka_consumer_tareas.recibirTareas()
