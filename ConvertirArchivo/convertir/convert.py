import os
from kafka.kafka import KafkaConsumerTareas, KafkaProducer

from mp3.conversor import convert_audio_to_mp3
from ogg.conversor import convert_audio_to_ogg
from wav.conversor import convert_audio_to_wav

kafka_producer = KafkaProducer()
kafka_consumer_tareas = KafkaConsumerTareas()

def convertr_manage():

    tareas = kafka_consumer_tareas.recibirMensaje()

    for t in tareas:

        output_format = t.newFormat
        filepath = t.filepath
        root, extension = os.path.splitext(filepath)
        name_output_file = 'archivo_resultado'
        mensaje = {
            'user': t.usuario.id,
            'email_user': t.usuario.email,
            'new_format': t.newFormat,
            'file': t.filepath
        }
        respuesta = {
            'estado': 'PROCESSED',
            'outputfile': name_output_file,
            'new_format': t.newFormat,
            'file': t.filepath
        }
        

        if extension == '.wav':
            if output_format == '.mp3':
                r = convert_audio_to_mp3(filepath, name_output_file, extension)
            if output_format == '.ogg':
                r = convert_audio_to_ogg(filepath, name_output_file, extension)

        if extension == '.ogg':
            if output_format == '.mp3':
                r = convert_audio_to_mp3(filepath, name_output_file, extension)
            if output_format == '.wav':
                r = convert_audio_to_wav(filepath, name_output_file, extension)
        
        if extension == '.mp3':
            if output_format == '.wav':
                r = convert_audio_to_wav(filepath, name_output_file, extension)
            if output_format == '.ogg':
                r = convert_audio_to_ogg(filepath, name_output_file, extension)

        if r['ok']:
            kafka_producer.enviarNotificacion('Notificar', t.tarea, mensaje)
        else:
            respuesta['estado'] = 'FAILED'

        kafka_producer.enviarRespuesta('Respuesta',t.tarea,respuesta)