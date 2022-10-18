from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer
from actualizarEstado.actualizarEstado import ActualizarEstado

class KafkaProducer():
    server = os.environ.get('SERVER_KAFKA', None)
    if server == None:
        server = 'localhost:9092'

    producer = KafkaProducer(
            bootstrap_servers = [server],
            value_serializer=lambda m: dumps(m).encode('utf-8')
        )
    
    def enviarTarea(self, topic, keys, mensaje):
        self.producer.send(topic, key=bytes(keys, 'utf-8'), value = mensaje)
        self.producer.flush()

class KafkaConsumer():
    consumer = KafkaConsumer(
        'Respuesta',
        bootstrap_servers = ['localhost:9092'],
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
    )
    

    def recibirTareas(self):
        actualizar_estado = ActualizarEstado()
        for t in self.consumer:
            actualizar_estado.actualizarEstadoTarea(t.value)