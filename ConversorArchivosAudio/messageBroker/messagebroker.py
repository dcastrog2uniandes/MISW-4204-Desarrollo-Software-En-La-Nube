from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer
from actualizarEstado.actualizarEstado import ActualizarEstado
import os

class KafkaProducerCliente:
    server = os.environ.get('SERVER_KAFKA', None)
    if server == None:
        server = 'localhost:9092'

    producer = KafkaProducer(
            group_id='my-group-kafka',
            bootstrap_servers = server,
            value_serializer=lambda m: dumps(m).encode('utf-8')
        )
    
    def enviarTarea(self, topic, keys, mensaje):
        self.producer.send(topic, key=bytes(keys, 'utf-8'), value = mensaje)
        self.producer.flush()

class KafkaConsumerCliente:
    server = os.environ.get('SERVER_KAFKA', None)
    if server == None:
        server = 'localhost:9092'

    consumer = KafkaConsumer(
        'Respuesta',
        group_id='my-group',
        bootstrap_servers = server,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=1000
    )
    
    def recibirTareas(self):
        actualizar_estado = ActualizarEstado()
        for t in self.consumer:
            actualizar_estado.actualizarEstadoTarea(t.value)
            