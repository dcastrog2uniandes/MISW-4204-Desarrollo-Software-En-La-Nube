from pydub import AudioSegment

def convert_audio_to_mp3(filepath:str,output_file:str, format:str):
    try: 
        if format == '.ogg':
            sound = AudioSegment.from_ogg(filepath)
        if format == '.wav':
            sound = AudioSegment.from_wav(filepath)
    
        sound.export(output_file + '.mp3', format='mp3')
        return {"ok": True}
    except:
        return {"ok": False}
        