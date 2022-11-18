from actualizarEstado.actualizarEstado import ActualizarEstado
import os
import json
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

class KafkaProducerCliente:
    if os.environ.get('GOOGLE_APPLICATION_PUB_TAREAS', None) is None:
        os.environ['GOOGLE_APPLICATION_PUB_TAREAS'] = 'projects/grupo4-cloud-368923/topics/Tareas'

    topic_path = os.environ.get('GOOGLE_APPLICATION_PUB_TAREAS', None)

    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credencial_google.json'
    
    def enviarTarea(self, keys, mensaje):        
        publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
            enable_message_ordering=True,
        ))
        publisher.publish(self.topic_path, str(keys).encode("utf-8"), datos=str(mensaje))
        
class KafkaConsumerCliente:
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credencial_google.json'

    timeout = 5.0
    if os.environ.get('GOOGLE_APPLICATION_SUB_RESPUESTA', None) is None:
        os.environ['GOOGLE_APPLICATION_SUB_RESPUESTA'] = 'projects/grupo4-cloud-368923/subscriptions/Respuesta-sub'

    subscription_path = os.environ.get('GOOGLE_APPLICATION_SUB_RESPUESTA', None)
    def callback(self, message):
        actualizar_estado = ActualizarEstado()
        if message.attributes:
            for key in message.attributes:
                actualizar_estado.actualizarEstadoTarea(json.loads(message.attributes.get(key).replace("'", chr(34))))
        message.ack()

    def recibirTareas(self):
        subscriber = pubsub_v1.SubscriberClient()
        streaming_pull_future = subscriber.subscribe(self.subscription_path, callback=self.callback)
        with subscriber:
            try:
                streaming_pull_future.result(timeout=self.timeout)
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()
