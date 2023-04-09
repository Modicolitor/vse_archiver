import os 
import ntpath
import copy


def equalize_directory(directory):
    f = os.path.join(directory, "dump.mp3")
    directory, dump = os.path.split(f)
    return directory


def split_filepath(filepath):
    path, basename = ntpath.split(filepath)
    #print(f'got {filepath} return {path} and {basename}')
    return path, basename


def get_directorynumber(directory, imgdirectories):
    print(f'in direcory number got directory {directory} and directories {imgdirectories}')
    keyslist = list_from_dictionary(imgdirectories)

    if directory in imgdirectories:
        n = keyslist.index(directory)
        return n, imgdirectories
    else:
        imgdirectories[directory] = 'targetpath' #append(directory)

        n = len(keyslist) # last new element
        return n, imgdirectories
    
    
def list_from_dictionary(dict):
    list = []
    for ele in dict.keys():
        list.append(ele)
    return list 

def contentlist_from_dictionary(dict):
    list = []
    for ele in dict:
        list.append(dict[ele])
    return list 