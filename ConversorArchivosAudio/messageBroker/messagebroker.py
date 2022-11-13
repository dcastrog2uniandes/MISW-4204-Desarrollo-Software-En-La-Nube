import json
from kafka import KafkaProducer, KafkaConsumer
from actualizarEstado.actualizarEstado import ActualizarEstado
import os

class KafkaProducerCliente:
    def __init__(self, topic):
        server = os.environ.get('SERVER_KAFKA', None)
        if server == None:
            server = 'localhost:9092'

        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=server,
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        
    def enviarTarea(self, mensaje):
        self.producer.send(self.topic, value=mensaje)
        
class KafkaConsumerCliente:
    def __init__(self, topic):
        server = os.environ.get('SERVER_KAFKA', None)
        if server == None:
            server = 'localhost:9092'
        self._consumer = KafkaConsumer( topic,
                                        bootstrap_servers=server,
                                        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                        auto_offset_reset='earliest',
                                        enable_auto_commit=True,
                                        consumer_timeout_ms=1000,
                                        group_id='nflx')

        self.data = []

    @property
    def consumer(self):
        return self._consumer

    @consumer.setter
    def consumer(self, value):
        if isinstance(value, KafkaConsumer):
            self._consumer = value

    def star_read(self):
        self.recibirTareas()
    
    def recibirTareas(self):
        actualizar_estado = ActualizarEstado()
        for t in self.consumer:
            actualizar_estado.actualizarEstadoTarea(t.value)
            