from json import loads
from kafka import KafkaConsumer
from EnviarCorreo.send_email import EnviarNotificacion
import os

class KafkaConsumer():
    server = os.environ.get('SERVER_KAFKA', None)
    if server == None:
        server = '10.128.0.2:9092'

    consumer = KafkaConsumer(
        'Notificar',
        bootstrap_servers = [server],
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    
    def enviarNotificacion(self):
        notificador = EnviarNotificacion()

        for n in self.consumer:
            notificador.send_email_notification(n.value)
            