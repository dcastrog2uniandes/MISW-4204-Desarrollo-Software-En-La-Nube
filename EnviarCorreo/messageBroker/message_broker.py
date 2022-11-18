from google.cloud import pubsub_v1
from EnviarCorreo.send_email import EnviarNotificacion
import os
import json

class KafkaConsumerCliente:
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credencial_google.json'

    timeout = 5.0
    if os.environ.get('GOOGLE_APPLICATION_SUB_NOTIFICAR', None) is None:
        os.environ['GOOGLE_APPLICATION_SUB_NOTIFICAR'] = 'projects/grupo4-cloud-368923/subscriptions/Notificar-sub'
    
    subscription_path = os.environ.get('GOOGLE_APPLICATION_SUB_NOTIFICAR', None)
    
    def callback(self, message):
        notificador = EnviarNotificacion()
        if message.attributes:
            for key in message.attributes:
                notificador.send_email_notification(json.loads(message.attributes.get(key).replace("'", chr(34))))
         
        message.ack()

    def enviarNotificacion(self):
        subscriber = pubsub_v1.SubscriberClient()
        streaming_pull_future = subscriber.subscribe(self.subscription_path, callback=self.callback)
        with subscriber:
            try:                
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()
            
            