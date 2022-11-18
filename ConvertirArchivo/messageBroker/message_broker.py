import json
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from convertir.convert import ConvertirAudio

class KafkaConsumer():
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credencial_google.json'

    timeout = 5.0
    if os.environ.get('GOOGLE_APPLICATION_SUB_TAREAS', None) is None:
        os.environ['GOOGLE_APPLICATION_SUB_TAREAS'] = 'projects/grupo4-cloud-368923/subscriptions/Tareas-sub'
    
    subscription_path = os.environ.get('GOOGLE_APPLICATION_SUB_TAREAS', None)
    
    def callback(self, message):
        if message.attributes:
            for key in message.attributes:
                convertidor_audio = ConvertirAudio()
                convertidor_audio.convert_manage(json.loads(message.attributes.get(key).replace("'", chr(34))))
        
        message.ack()
    
    def recibirTareas(self):
        subscriber = pubsub_v1.SubscriberClient()
        streaming_pull_future = subscriber.subscribe(self.subscription_path, callback=self.callback)
        with subscriber:
            try:                
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()
            


