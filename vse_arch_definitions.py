import os 
import ntpath

def is_audio(filepath):
    filename, extension =os.path.splitext(filepath)
    if len(extension) != 0:
        extension =   extension[1:]
    #print(f'extension {extension} of filepath {filepath}')
    audiotypes = ['AAC','aac', 'AC3', 'ac3', 'FLAC','flac', 'MP2', 'mp2', 'MP3', 'mp3', 'Opus', 'opus', 'OPUS', 'PCM', 'pcm', 'AIF', 'aif', 'Aac', 'Ac3', 'Flac', 'Mp2', 'Mp3', 'Opus', 'Pcm', 'Aif', 'wav', 'WAV', 'Wav'] #can be video as well 'OGG', 'ogg' added wav
    #print(f'found to be audio {extension in audiotypes} ')
    return extension in audiotypes
        
        
        
def is_video(filepath):
    filename, extension =os.path.splitext(filepath)
    audiotypes = ['mpg', 'mpeg', 'dvd', 'vob', 'mp4', 'avi', 'mov', 'dv', 'ogg', 'ogv', 'mkv', 'flv', 'webm', 'MPG', 'MPEG', 'DVD', 'VOB', 'MP4', 'AVI', 'MOV', 'DV', 'OGG', 'OGV', 'MKV', 'FLV', 'WEBM', 'Mpg', 'Mpeg', 'Dvd', 'Vob', 'Mp4', 'Avi', 'Mov', 'Dv', 'Ogg', 'Ogv', 'Mkv', 'Flv', 'Webm']
    return extension in audiotypes