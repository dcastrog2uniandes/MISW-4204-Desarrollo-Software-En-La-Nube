import os
from messageBroker.message_broker import KafkaProducer
from mp3.conversor import ConversorMP3
from ogg.conversor import ConversorOGG
from wav.conversor import ConversorWAV

kafka_producer = KafkaProducer()


class ConvertirAudio:
    def convert_manage(self,object):
        conversor_wav = ConversorWAV()
        conversor_mp3 = ConversorMP3()
        conversor_ogg = ConversorOGG()

        tarea = object['tarea']
        usuario = object['usuario']
        
        output_format = tarea['newFormat']
        filepath = tarea['fileOriginal']
        root, extension = os.path.splitext(filepath)
        name_output_file = tarea['fileConvertido']

        mensaje = {
            'user': usuario['id'],
            'email_user': usuario['email'],
            'new_format': tarea['newFormat'],
            'file': tarea['fileOriginal']
        }
        respuesta = {
            'estado': 'PROCESSED',
            'outputfile': name_output_file,
            'new_format': tarea['newFormat'],
            'file': tarea['fileOriginal']
        }
        
        if extension == '.wav':
            if output_format == '.mp3':
                r = conversor_mp3.convert_audio_to_mp3(filepath, name_output_file, extension)
            if output_format == '.ogg':
                r = conversor_ogg.convert_audio_to_ogg(filepath, name_output_file, extension)

        if extension == '.ogg':
            if output_format == '.mp3':
                r = conversor_mp3.convert_audio_to_mp3(filepath, name_output_file, extension)
            if output_format == '.wav':
                r = conversor_wav.convert_audio_to_wav(filepath, name_output_file, extension)
        
        if extension == '.mp3':
            if output_format == '.wav':
                r = conversor_wav.convert_audio_to_wav(filepath, name_output_file, extension)
                print('res: ', r)
            if output_format == '.ogg':
                r = conversor_ogg.convert_audio_to_ogg(filepath, name_output_file, extension)
        """
        if r['ok']:
            kafka_producer.enviarNotificacion('Notificar', tarea['id'], mensaje)
        else:
            respuesta['estado'] = 'FAILED'

        kafka_producer.enviarRespuesta('Respuesta',tarea['id'],respuesta)
        """
        