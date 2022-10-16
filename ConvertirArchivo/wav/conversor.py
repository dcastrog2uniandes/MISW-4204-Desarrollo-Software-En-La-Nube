from pydub import AudioSegment


class ConversorWAV:
    def convert_audio_to_wav(self,filepath:str,output_file:str,format:str):
        print('file: ',filepath)
        print('outpurfile: ',output_file)
        print('format: ',format)
        try:
            if format == '.mp3':
                sound = AudioSegment.from_mp3(filepath)
            if format == '.ogg':
                sound = AudioSegment.from_ogg(filepath)
            
            sound.export(output_file + '.wav', format='wav')
            return {"ok": True}
        except:
            return {"ok": False}