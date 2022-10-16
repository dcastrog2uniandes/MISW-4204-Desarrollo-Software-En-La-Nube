from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer


class KafkaConsumerTareas():
    consumer = KafkaConsumer(
            'Tareas',
            bootstrap_servers = ['localhost:9092'],
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            consumer_timeout_ms=1000
        )
    
    def recibirMensaje(self):
        print('Consumer tareas !')
        return self.consumer

class KafkaProducer():
    producer = KafkaProducer(
            bootstrap_servers = ['localhost:9092'],
            value_serializer=lambda m: dumps(m).encode('utf-8')
        )
    
    def enviarNotificacion(self, topic, keys, mensaje):
        self.producer.send(topic, key=bytes(keys, 'utf-8'), value=mensaje)
        self.producer.flush()

    def enviarRespuesta(self, topic, keys, mensaje):
        self.producer.send(topic, key=bytes(keys, 'utf-8'), value=mensaje)
        self.producer.flush()
