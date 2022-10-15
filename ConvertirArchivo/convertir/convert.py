import os
import pathlib

from ..mp3 import convert_audio_to_mp3
from ..ogg import convert_audio_to_ogg
from ..wav import convert_audio_to_wav

def convert_validator(filepath:str,name_output_file:str,output_format:str):
    #ruta_absoluta = str(pathlib.Path(__file__).parent.absolute())

    formats = ['.wav','.ogg','.mp3']
    root, extension = os.path.splitext(filepath)

    if output_format not in formats:
        return 'Formato de salida no disponible'

    if extension in formats:
        if extension == '.wav':
            if output_format == '.mp3':
                convert_audio_to_mp3(filepath, name_output_file, extension)
            if output_format == '.ogg':
                convert_audio_to_ogg(filepath, name_output_file, extension)

        if extension == '.ogg':
            if output_format == '.mp3':
                convert_audio_to_mp3(filepath, name_output_file, extension)
            if output_format == '.wav':
                convert_audio_to_wav(filepath, name_output_file, extension)
        
        if extension == '.mp3':
            if output_format == '.wav':
                convert_audio_to_wav(filepath, name_output_file, extension)
            if output_format == '.ogg':
                convert_audio_to_ogg(filepath, name_output_file, extension)
    else:
        return 'Formato de archivo no soportado'
