import sys
from pydub import AudioSegment

class ConversorOGG:
    def convert_audio_to_ogg(self,filepath:str,output_file:str, format):
        try:
            if format == '.wav':
                sound = AudioSegment.from_wav(filepath)
            if format == '.mp3':
                sound = AudioSegment.from_mp3(filepath)
            
            sound.export(output_file, format='ogg')
            print('Se proceso el archivo: ',output_file)
            sys.stdout.flush()
            return True
        except:
            print('Error al procesar el archivo: ',output_file)
            return False