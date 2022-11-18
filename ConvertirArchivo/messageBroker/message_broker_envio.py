import os
from google.cloud import pubsub_v1

class KafkaProducerRespuestas():
    if os.environ.get('GOOGLE_APPLICATION_PUB_RESPUESTA', None) is None:
        os.environ['GOOGLE_APPLICATION_PUB_RESPUESTA'] = 'projects/grupo4-cloud-368923/topics/Respuesta'

    topic_path_respuesta = os.environ.get('GOOGLE_APPLICATION_PUB_RESPUESTA', None)

    if os.environ.get('GOOGLE_APPLICATION_PUB_NOTIFICAR', None) is None:
        os.environ['GOOGLE_APPLICATION_PUB_NOTIFICAR'] = 'projects/grupo4-cloud-368923/topics/Notificar'

    topic_path_notificar = os.environ.get('GOOGLE_APPLICATION_PUB_NOTIFICAR', None)
    
    def enviarNotificacion(self, keys, mensaje):
        publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
            enable_message_ordering=True,
        ))
        publisher.publish(self.topic_path_notificar, str(keys).encode("utf-8"), datos=str(mensaje))

    def enviarRespuesta(self, keys, mensaje):
        publisher = pubsub_v1.PublisherClient(publisher_options = pubsub_v1.types.PublisherOptions(
            enable_message_ordering=True,
        ))
        publisher.publish(self.topic_path_respuesta, str(keys).encode("utf-8"), datos=str(mensaje))


