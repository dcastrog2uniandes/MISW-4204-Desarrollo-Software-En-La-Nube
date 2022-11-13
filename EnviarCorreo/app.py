from flask import Flask
from messageBroker.message_broker import KafkaConsumerCliente

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

kafka_consumer_notificaciones = KafkaConsumerCliente()
kafka_consumer_notificaciones.enviarNotificacion()
