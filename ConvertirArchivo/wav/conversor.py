from pydub import AudioSegment

def convert_audio_to_wav(filepath:str,output_file:str,format:str):
    try:
        if format == '.mp3':
            sound = AudioSegment.from_mp3(filepath)
        if format == '.ogg':
            sound = AudioSegment.from_ogg(filepath)
        
        sound.export(output_file + '.wav', format='wav')
        return {"ok": True}
    except:
        return {"ok": False}