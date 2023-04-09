import bpy
import os
import json
from .bl_archiver_properties import Bl_Archiver_PropGroup
from pathlib import Path
import shutil
import os 
import ntpath
import copy

from .archiver_general import equalize_directory, split_filepath, get_directorynumber, contentlist_from_dictionary
  

#from .vse_arch_functions import collect_moviclips, collect_sounds,collect_images, remap_moviclips, remap_sounds, remap_images, remap_fonts, copy_files
from bpy.app.handlers import persistent



#lädt mit jedem 
@persistent
def load_handler(context: bpy.context):#all_filepathes
    all_filepathes = get_all_filepathes()
    json_filepath = get_json_filepath()
    extern_all_filepathes = read_json(json_filepath, all_filepathes) 
    
    print(f'I m open {all_filepathes}')
    print(f'read from json {extern_all_filepathes}')
    own_filepath = bpy.path.abspath('//')
    if extern_all_filepathes["Scan"] != '':
        if extern_all_filepathes["Scan"] == own_filepath:
            print('checking opened blend!!')
            blends_to_check = all_filepathes['blends_to_check']
            
            ###find linked data 
            all_filepathes = get_linked_data(context, all_filepathes)
            all_filepathes = get_linked_blends(context, all_filepathes)
            
            
            ####copy files 
            to_copy, all_filepathes = whats_new(extern_all_filepathes, all_filepathes)
            errorlist = copy_files(to_copy)
            
            ###merge the dictionaries
            all_filepathes.update(extern_all_filepathes)
            
            remap_data(context, all_filepathes)
            
            #remove this blend from blends to check 
            blends_to_check = blends_to_check.remove(own_filepath)
            write_json(json_filepath, all_filepathes)
            bpy.ops.wm.window_close()
   

bpy.app.handlers.load_post.append(load_handler)

#compares the keywords of two all_files with 'filepathes' in it, removes elements from the second and return the dict
def whats_new(extern_all_filepathes, all_filepathes):
    ex_filepathes = extern_all_filepathes['filepathes']
    filepathes = all_filepathes['filepathes']
    
    for e in filepathes.items():
        for i in ex_filepathes:
            if e[0] == i[0]:
                filepathes.pop(e[0])
                
                
    return filepathes, all_filepathes
                
    

def get_pathformat_dict():
    l = ["filepathes", "vid_directories", "audio_directories", "font_directories", "caches_directories", "img_directories", "imgseq_directories", "blends_to_check", "blends_to_copy", "main_filepath"]
    return l

def get_pathformat_lists():
    l = ["blends_to_check"]
    return l

def get_all_filepathes():
    dics= get_pathformat_dict()
    lists = get_pathformat_lists()
    
    
    all_filepathes1 = all_filepathes1 = {"Scan": ""}
    all_filepathes2 = {}
    all_filepathes2 = all_filepathes2.fromkeys(dics,{})
    all_filepathes3 = {}
    all_filepathes3 = all_filepathes3.fromkeys(lists,[])
    all_filepathes = {}
    all_filepathes.update(all_filepathes1)
    all_filepathes.update(all_filepathes2)
    all_filepathes.update(all_filepathes3)
    return all_filepathes

def write_json(json_filepath, all_filepathes):
    data = all_filepathes
    json_filepath = get_json_filepath()
    with open(json_filepath, 'w') as outfile:
        json.dump(all_filepathes, outfile)
    print('I wrote json')

def read_json(json_filepath, all_filepathes):
    #filename = "user_rasps.json"

    #folderpath = FM.appdatafoldername
    json_filepath = 'C:\\Blender\\3.5\\scripts\\addons\\vse_archiver\\blend_archiver.json'

    #my_file = Path("user_rasps.json")
    my_file = Path(json_filepath)
    if my_file.is_file():
        with open(json_filepath) as json_file:
            data = json.load(json_file)
            all_filepathes = data

    else:
        print('No jason unter diser Nummer======================================================') 
    print('Im reading json')
    return all_filepathes

def get_json_filepath():
    json_filepath = "C:\\Blender\\3.5\\scripts\\addons\\vse_archiver\\blend_archiver.json" 
    return json_filepath


def start_archiving(context):
    
    #set controll bool to indentify main file
    context.scene.bl_archiver.is_main_file = True
    all_filepathes = get_all_filepathes()
    json_filepath = get_json_filepath()
    write_json(json_filepath, all_filepathes)
    
       
    #blends_to_check = all_filepathes['blends_to_check']
    
    all_filepathes = get_linked_data(context, all_filepathes)
    all_filepathes = get_linked_blends(context, all_filepathes)
    
    
    
    #it should be a while loop until all to check are worked through
    while len(all_filepathes['blends_to_check']) != 0: 
        all_filepathes = get_filepathes_from_blend(all_filepathes)


    print(all_filepathes['blends_to_check'])
    #print(filepathes)
    #print(imgseq_directories)
    
def get_linked_data(context, all_filepathes):
    ####use blenddata collector von vse archiver
    print('here I should get all linked nonblendfiles ')
    all_filepathes['filepathes'], all_filepathes['imgseq_directories'] = collect_images(context, all_filepathes['filepathes'], all_filepathes['imgseq_directories'])
    #collect_moviclips
    #collect_sounds
    #collect_images
    
    return all_filepathes

def get_linked_blends(context, all_filepathes):
    #find all blender libaries
    
    for lib in bpy.data.libraries:
        if hasattr(lib, 'filepath'):
            if lib.filepath not in all_filepathes['blends_to_check']:
                all_filepathes['blends_to_check'].append(lib.filepath)
    print(f'found libaries ')
    print(all_filepathes['blends_to_check'])
    return all_filepathes


def remap_data(context, all_filepathes):
    filepathes = all_filepathes['filepathes']
    remap_moviclips(context, filepathes)
    remap_sounds(context, filepathes)
    remap_images(context, filepathes)
    remap_fonts(context, filepathes)
    

def gen_properties(context):
    bpy.types.Scene.bl_archiver = bpy.props.PointerProperty(type=Bl_Archiver_PropGroup)

#checks first item of filepath and removes it afterwards
def get_filepathes_from_blend(all_filepathes):
    
    blends_to_check = all_filepathes['blends_to_check']
    #blends_to_copy = all_filepathes['blends_to_copy']
    #filepathes = all_filepathes['filepathes']
    #imgseq_directories = all_filepathes['imgseq_directories']
    
    filepath = blends_to_check[0]
    
    

    #filepathes, imgseq_directories = open_new_blend(filepath, filepathes, imgseq_directories)
    print(f'before start{all_filepathes}')
    #print(f'I"m mains own_filepath {all_filepathes}')
    
    use_instance = True
    
    import subprocess
    #try:
    #settings["linked_file"] = os.path.abspath(bpy.path.abspath(targetpath))
    print(f'starting sub file {filepath}')
    #p = subprocess.Popen([bpy.app.binary_path, os.path.abspath(bpy.path.abspath(filepath)), '-b']) # , all_filepathes
    #all_filepathes["linked_file"] = os.path.abspath(bpy.path.abspath(filepath))
    all_filepathes['Scan'] = os.path.abspath(bpy.path.abspath(filepath))
    write_json(get_json_filepath, all_filepathes)
    
    print(f'starting sub file {filepath}')
    p = subprocess.Popen([bpy.app.binary_path, '-b', filepath ])  
    
    #subprocess.Popen([bpy.app.binary_path, settings["linked_file"]])
    #
    out, err = p.communicate()
    #print(f'out of subprocess {out}')
    #print(f'error of subprocess {err}')

        
    read_json(get_json_filepath, all_filepathes)
    ###important for stoping the while loop 
    blends_to_check.remove(filepath)
    return all_filepathes # blends_to_check, filepathes, imgseq_directories








def collect_moviclips(context, filepathes, vid_directories):
    data = bpy.data 
    for mc in data.movieclips:
        if mc.filepath  not in filepathes:
            directory, basename = os.path.split(mc.filepath)
            filepathes[mc.filepath], vid_directories = get_video_target_path(context, mc.filepath, vid_directories)
    return filepathes, vid_directories

def collect_sounds(context, filepathes, audio_directories, vid_directories):
    data = bpy.data 
    for sound in data.sounds:
        if sound.filepath  not in filepathes:
            filepathes[sound.filepath], audio_directories, vid_directories = get_audio_target_path(context, sound.filepath, audio_directories, vid_directories)
    return filepathes, audio_directories, vid_directories

def collect_fonts(context, filepathes, font_directories):
    data = bpy.data 
    for font in data.fonts:
        if font.filepath  not in filepathes:
            directory, basename = os.path.split(font.filepath)
            filepathes[font.filepath], font_directories = get_font_target_path(context, font.filepath, font_directories)
    return filepathes, font_directories

def collect_images(context, filepathes, imgseq_directories):
    data = bpy.data 
    for img in data.images:
        if img.type == 'IMAGE':
            if img.filepath  not in filepathes:
                print(f'img.filepath {img.filepath}')
                directory, basename = os.path.split(img.filepath)
                #n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                print(f'directory,{directory}, basename {basename}')
                
                targetpath, imgseq_directories = get_imgseq_target_path(context, basename, directory, imgseq_directories)
                
                print(f'targetpath is weird {targetpath}')
                imgseq_directories[directory] = targetpath
                
                if img.filepath not in filepathes:
                        filepathes[img.filepath] = os.path.join(imgseq_directories[directory], basename) 
                
    return filepathes, imgseq_directories







def remap_moviclips(context, filepathes):
    data = bpy.data 
    for mc in data.movieclips:
        if mc.filepath  in filepathes:
            mc.filepath = filepathes[mc.filepath]
        else:
            print(f'couldnt find {mc.name} with filepath {mc.filepath} in filepathes dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def remap_sounds(context, filepathes):
    data = bpy.data 
    for sound in data.sounds:
        if sound.filepath  in filepathes:
            sound.filepath = filepathes[sound.filepath] 
        else:
            print(f'couldnt find {sound.name} with filepath {sound.filepath} in filepathes dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
def remap_fonts(context, filepathes):
    data = bpy.data 
    for font in data.fonts:
        if font.filepath  in filepathes:
            font.filepath = filepathes[font.filepath]
        else:
            print(f'couldnt find {font.name} with filepath {font.filepath} in filepathes dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

def remap_images(context, filepathes):
    data = bpy.data 
    for img in data.images:
        if img.type == 'IMAGE':
            if img.filepath  in filepathes:
                img.filepath = filepathes[img.filepath]
            else:
                print(f'couldnt find {img.name} with filepath {img.filepath} in filepathes dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')





def get_video_target_path(context, filepath, vid_directories):
    #print(f'In get video path filepath {filepath} directory {directory} vid_directories {vid_directories} ')
    arch_props = context.scene.bl_archiver
    targetfolder = arch_props.target_folder
    videofolder = arch_props.target_video_folder
    
    directory, basename = split_filepath(filepath)
    #print(f'audio target path beginning dir {directory} basename {basename}')
    #'target_folder'\videofolder\basename 
    targetpath = os.path.join(targetfolder, videofolder)
    
    
    if directory in vid_directories:
        #already got that folder
        targetpath = vid_directories[directory]
        #targetpath, wrongbasename = os.path.split(targetpathOtherfile)
        #print(f'targetpathOtherfile')
        video_targetpath = os.path.join(targetpath, basename) 
        print(f'al/found in vid dict path {filepath} aud target path {video_targetpath}')
    else:   
        ignore, subfoldername = os.path.split(directory)
        #print(f'subfolder name is {subfoldername}')
        n, vid_directories = get_directorynumber(directory, vid_directories)
        subfoldername = subfoldername + "_" + str(n)
        targetpath = os.path.join(targetpath, subfoldername)
        video_targetpath = os.path.join(targetpath, basename)
        #print(f'new in vid folder path {filepath} aud target path {video_targetpath}')
        
    vid_directories[directory] = targetpath
    #print(f'after processing {filepath} vid_directories {vid_directories}')
    return video_targetpath, vid_directories
    



def get_audio_target_path(context, filepath, audio_directories, video_directories): 
    arch_props = context.scene.bl_archiver
    targetfolder = arch_props.target_folder
    directory, basename = split_filepath(filepath)
    print(f'audio target path beginning dir {directory} basename {basename}')
    if is_audio(filepath):
        audiofolder = arch_props.target_audio_folder
        if directory in audio_directories:
            #already got that folder
            targetpath = audio_directories[directory]
            #targetpath, wrongbasename = os.path.split(targetpathOtherfile)
            audio_target_path = os.path.join(targetpath, basename)
            
            print(f'path {filepath} aud target path {audio_target_path}')
        else:
            path, basename = os.path.split(filepath)
            targetfolder = os.path.join(targetfolder, audiofolder)
            n, audio_directories = get_directorynumber(directory, audio_directories)
            ignore, subfoldername = os.path.split(directory)
            #print(f'subfolder name is {subfoldername}')
            subfoldername =subfoldername + "_" + str(n)
           
            target_folder = os.path.join(targetfolder, subfoldername)
            audio_target_path = os.path.join(target_folder, basename)
            print(f'path {filepath} aud target path {audio_target_path}')
            audio_directories[directory] = target_folder
    #not audio
    else:
        videofolder = arch_props.target_video_folder
        
        if directory in video_directories :
            #already got that folder
            targetpathOtherfile = video_directories[directory]
            targetpath, wrongbasename = os.path.split(targetpathOtherfile)
            audio_target_path = os.path.join(targetpath, basename)
            print(f'al/in vide dict path {filepath} aud target path {audio_target_path}')
        else:   
            targetpath = os.path.join(targetfolder, videofolder)
            #targetfolder = os.path.join(targetfolder, audiofolder)
            n, video_directories = get_directorynumber(directory, video_directories)
            ignore, subfoldername = os.path.split(directory)
            #print(f'subfolder name is {subfoldername}')
            subfoldername =subfoldername + "_" + str(n)
            target_folder = os.path.join(targetpath, subfoldername)
            audio_target_path = os.path.join(target_folder, basename)
            #imgseq_targetpath = targetpath 
            
            video_directories[directory] = target_folder
            print(f'In New vid dcgt path {filepath} aud target path {audio_target_path}')
            
    return audio_target_path, audio_directories, video_directories

def get_font_target_path(context, filepath, font_directories ):
    arch_props = context.scene.bl_archiver
    targetfolder = arch_props.target_folder
    fontfolder = arch_props.target_font_folder
    directory, basename = split_filepath(filepath)

    #'target_folder'\videofolder\basename 
    #targetpath = os.path.join(targetfolder, fontfolder)
    
    
    
    if directory in font_directories:
        #already got that folder
        font_target_path = os.path.join(font_directories[directory], basename)
    else:
        n, font_directories = get_directorynumber(directory, font_directories)
        target_fontfolder = os.path.join(targetfolder, fontfolder)
        ignore, subfoldername = os.path.split(directory)
        subfoldername =subfoldername + "_" + str(n)
        target_folder = os.path.join(target_fontfolder,subfoldername)
        font_target_path = os.path.join(target_folder, basename)
        
        font_directories[directory] = target_folder
    

    return font_target_path, font_directories

def get_imgseq_target_path(context, filename, directory, imgseq_directories):
    arch_props = context.scene.bl_archiver
    targetfolder = arch_props.target_folder
    imgseqfolder = arch_props.target_imgseq_folder

    #'target_folder'maintarget\imgseqfolder\
    targetpath = os.path.join(targetfolder, imgseqfolder)
    print(f'++++++in get target parth {filename}')
    if directory in imgseq_directories:
        #already got that folder
        print(f'imseq_targetpathes  at {filename} are {imgseqfolder}')
        imgseq_targetpath = imgseq_directories[directory]
        
    else:
        directory = equalize_directory(directory)
        ignore, subfoldername = os.path.split(directory)
        ####correction for different filepath sources: blender filepathes / or \ ending (result in ''), os.path.join produces path without slashes 
        '''if subfoldername == '':
            directory = directory[:-1]
            ignore, subfoldername = os.path.split(directory[:-1])'''
        #print(f'subfolder name is {subfoldername}')
        n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
        subfoldername =subfoldername + "_" + str(n)
        target_folder = os.path.join(targetpath, subfoldername)
        imgseq_targetpath = target_folder 
    
        imgseq_directories[directory]= target_folder
        print(f'get imseq path for subfolder {subfoldername}  filename {filename} imgseq_directories {imgseq_directories}')
    return imgseq_targetpath, imgseq_directories



def copy_files(filepathes):
    print(f'filepathes before copying:  ' )
    #easy read print
    #for d in filepathes:
    #    print(f' {d} : {filepathes[d]} ')
    ###
    errorlist = []
    for srcpath in filepathes.items():
        if srcpath[0] != srcpath[1]:
            targetpath, basename = split_filepath(srcpath[1])
            os.makedirs(targetpath, exist_ok=True)
            try:
                copy_file(srcpath[0], targetpath)
            except:
                errorlist.append(f'Error copying from {srcpath[0]} to {targetpath}. Probably source file missing or no writing rights.')
        else:
            print(f'ignored copying file {srcpath[0]}; target path equals sourcepath ')
            
    return errorlist

def copy_file(src, dst):
    shutil.copy2(src, dst)