import os
from googleStorage.googleStorage import GoogleStorage
from mp3.conversor import ConversorMP3
from ogg.conversor import ConversorOGG
from wav.conversor import ConversorWAV
from messageBroker.message_broker_envio import KafkaProducerRespuestas

ruta_archivo_original = '../Archivos/ArchivoOriginal/'
ruta_archivo_conversor = '../Archivos/ArchivoConversion/'

class ConvertirAudio:
    def convert_manage(self, object):
        conversor_wav = ConversorWAV()
        conversor_mp3 = ConversorMP3()
        conversor_ogg = ConversorOGG()

        tarea = object['tarea']
        usuario = object['usuario']

        googleStorage = GoogleStorage()
        googleStorage.download_file_from_bucket(tarea['fileOriginal'], ruta_archivo_original + tarea['fileOriginal'].split('/')[-1])
        
        output_format = tarea['newFormat']
        filepath = ruta_archivo_original + tarea['fileOriginal'].split('/')[-1]
        root, extension = os.path.splitext(filepath)
        name_output_file = ruta_archivo_conversor + tarea['fileConvertido'].split('/')[-1]

        mensaje = {
            "user": usuario['id'],
            "email_user": usuario['email'],
            "new_format": tarea['newFormat'],
            "file": tarea['fileOriginal'],
            "file_output": tarea['fileConvertido'],
            "tarea": tarea['id']     
            }

        r = None

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
            if output_format == '.ogg':
                r = conversor_ogg.convert_audio_to_ogg(filepath, name_output_file, extension)
        
        kafka_producer = KafkaProducerRespuestas()
        if r:
            tarea['status'] = 'PROCESSED'
            kafka_producer.enviarNotificacion(str(tarea['id']), mensaje)
        else:
            tarea['status'] = 'FAILED'

        kafka_producer.enviarRespuesta(str(tarea['id']), tarea)

        googleStorage.upload_to_bucket(tarea['fileConvertido'], name_output_file)

        os.remove(filepath)
        os.remove(name_output_file)


        
        