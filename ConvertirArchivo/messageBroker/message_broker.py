from json import loads
from kafka import KafkaConsumer
from convertir.convert import ConvertirAudio

class KafkaConsumer():
    consumer = KafkaConsumer(
        'Tareas',
        bootstrap_servers = ['localhost:9092'],
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
    )
    
    def recibirTareas(self):
        convertidor_audio = ConvertirAudio()
        for t in self.consumer:
            convertidor_audio.convert_manage(t.value)
            

