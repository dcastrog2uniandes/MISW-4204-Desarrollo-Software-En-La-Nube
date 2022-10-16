from json import dumps, loads
from kafka import KafkaConsumer


class KafkaConsumerNotificaciones():
    consumer = KafkaConsumer(
            'Notificar',
            bootstrap_servers = ['localhost:9092'],
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            consumer_timeout_ms=1000
        )
    
    def enviarNotificacion(self):
        return self.consumer
        
