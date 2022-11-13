from json import loads
from kafka import KafkaConsumer
from EnviarCorreo.send_email import EnviarNotificacion
import os

class KafkaConsumerCliente:
    def enviarNotificacion(self):
        server = os.environ.get('SERVER_KAFKA', None)
        if server == None:
            server = 'localhost:9092'
        
        consumer = KafkaConsumer (
            'Notificar',
            bootstrap_servers = [server],
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            auto_commit_interval_ms=1000
        )
        for n in consumer:
            notificador = EnviarNotificacion()
            notificador.send_email_notification(n.value)
            