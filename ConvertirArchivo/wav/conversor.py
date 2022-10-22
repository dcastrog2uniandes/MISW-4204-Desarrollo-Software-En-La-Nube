import sys
from pydub import AudioSegment
import datetime
import os

class ConversorWAV:
    def convert_audio_to_wav(self,filepath:str,output_file:str,format:str):
        try:
            if format == '.mp3':
                sound = AudioSegment.from_mp3(filepath)
            if format == '.ogg':
                sound = AudioSegment.from_ogg(filepath)
            
            sound.export(output_file, format='wav')
            print('Se convirtio el archivo: ',output_file, 'hora: ', datetime.datetime.now(), 'archivo original:',filepath, 'tamanio:', str(round(os.path.getsize(filepath)/1024000, 2)) + ' MB')
            sys.stdout.flush()
            return True
        except:
            print('Error al procesar el archivo: ',output_file)
            return False