from pydub import AudioSegment


class ConversorWAV:
    def convert_audio_to_wav(self,filepath:str,output_file:str,format:str):
        try:
            if format == '.mp3':
                sound = AudioSegment.from_mp3(filepath)
            if format == '.ogg':
                sound = AudioSegment.from_ogg(filepath)
            
            sound.export(output_file, format='wav')
            print('Se proceso el archivo: ',output_file)
            return True
        except:
            print('Error al procesar el archivo: ',output_file)
            return False