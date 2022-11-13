from json import loads
from kafka import KafkaConsumer
from convertir.convert import ConvertirAudio
import os

class KafkaConsumer():
    server = os.environ.get('SERVER_KAFKA', None)
    if server == None:
        server = 'localhost:9092'

    consumer = KafkaConsumer(
        'Tareas',
        bootstrap_servers = ['10.128.0.2:9092'],
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        auto_commit_interval_ms=1000
    )
    
    def recibirTareas(self):
        convertidor_audio = ConvertirAudio()
        for t in self.consumer:
            convertidor_audio.convert_manage(t.value)
            


