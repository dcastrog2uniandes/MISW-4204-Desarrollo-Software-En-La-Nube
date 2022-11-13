from flask import Flask
from messageBroker.message_broker import KafkaConsumer

app = Flask(__name__)

app_context = app.app_context()
app_context.push()

kafka_consumer_notificaciones = KafkaConsumer()
kafka_consumer_notificaciones.enviarNotificacion()
