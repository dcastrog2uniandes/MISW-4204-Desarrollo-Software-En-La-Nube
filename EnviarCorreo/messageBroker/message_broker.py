from json import loads
from kafka import KafkaConsumer
from EnviarCorreo.send_email import EnviarNotificacion
import os

class KafkaConsumer():
    server = os.environ.get('SERVER_KAFKA', None)
    if server == None:
        server = 'localhost:9092'

    consumer = KafkaConsumer(
        'Notificar',
        bootstrap_servers = [server],
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        auto_commit_interval_ms=1000
    )
    
    def enviarNotificacion(self):
        notificador = EnviarNotificacion()

        for n in self.consumer:
            notificador.send_email_notification(n.value)
            