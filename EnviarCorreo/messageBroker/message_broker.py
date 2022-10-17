from json import loads
from kafka import KafkaConsumer
from EnviarCorreo.send_email import EnviarNotificacion

class KafkaConsumer():
    consumer = KafkaConsumer(
        'Notificar',
        bootstrap_servers = ['localhost:9092'],
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
    )
    
    def enviarNotificacion(self):
        notificador = EnviarNotificacion()

        for n in self.consumer:
            notificador.send_email_notification(n.value)
            
        
