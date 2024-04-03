import bpy 
import shutil ###copy files with python
import os 
import ntpath
import copy
from .vse_arch_definitions import is_audio, is_video

#
def copy_file(src, dst):
    shutil.copy2(src, dst)

def print_list(list):
    for n,l in enumerate(list):
        print(f'{n}     {l}')
        
def has_equal_metas(context):
    ####man muss es von data ziehen und durch alle scene  schauen
    
    #sequences = context.scene.sequence_editor.sequences_all
    
    arch_count = 0
    c = 0
    for sc in bpy.data.scenes:
        for seq in sc.sequence_editor.sequences_all:
            if seq.type == 'META':
                c += 1 
    for sc in bpy.data.scenes:
        arch_metastrips = sc.vse_archiver.metastrips
        arch_count += len(arch_metastrips)
        
    #print(f'sequence count is {c} and archiver metacount {arch_count}')
    return c == arch_count
       
def has_equal_sequences(context):
    arch_count = 0
    c = 0
    for sc in bpy.data.scenes:
        for s in sc.sequence_editor.sequences_all:
            type = get_sequence_type(s)
            if type in ['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']:
                c += 1
                
    for sc in bpy.data.scenes:
        arch_sequences = sc.vse_archiver.sequences
        arch_count += len(arch_sequences)

    return c == arch_count

def check_rendersettings(context):
    is_image = True
    not_ffmpeg = True
    no_audio = False
    no_videocodec = False
    
    #videoformats = ['FFMPEG', 'AVI_RAW', 'AVI_JPEG']
    
    #print(f'{context.scene.render.image_settings.file_format == 'FFMPEG'}')
    file_format = context.scene.render.image_settings.file_format
    if file_format == 'FFMPEG' or file_format == 'AVI_RAW' or file_format == 'AVI_JPEG':
        is_image = False
    if file_format == 'FFMPEG':
        not_ffmpeg = False
    if context.scene.render.ffmpeg.audio_codec == 'NONE' or not_ffmpeg == True:
        no_audio = True
    if context.scene.render.ffmpeg.codec == 'NONE':
        no_videocodec = True
    
    return is_image, not_ffmpeg, no_audio, no_videocodec

def is_target_equ_source(context):
    target_folder = context.scene.vse_archiver.target_folder
    #blend_path = 
    
    return bpy.path.abspath('//') == bpy.path.abspath(target_folder)
    
def get_video_target_path(context, filepath, vid_directories):
    #print(f'In get video path filepath {filepath} directory {directory} vid_directories {vid_directories} ')
    arch_props = context.scene.vse_archiver
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
    arch_props = context.scene.vse_archiver
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
    arch_props = context.scene.vse_archiver
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
    arch_props = context.scene.vse_archiver
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

'''def get_none_numbername(filename):
    forbiddens = ['0','1','2','3','4','5','6','7','8','9','.', ',']
   
    tester = True
    while tester:
        if len(filename) == 0:
            tester = False
        elif filename[-1] in forbiddens:
            #print(filename)
            filename = filename[:-1]
        else:
            tester = False
    return filename'''

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
    


def split_filepath(filepath):
    path, basename = ntpath.split(filepath)
    #print(f'got {filepath} return {path} and {basename}')
    return path, basename

'''def get_target_filepath(filepath, target_folder):
    orifilepath, basename =  split_filepath(filepath)
    return os.path.join(target_folder, basename)'''



def sequence_to_copy(context, seq, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories): 
    type = get_sequence_type(seq)
    print(f'in sequence to copy seq {seq.name} type {type}')
    if type == 'MOVIE': #hasattr(seq, "filepath"): #videosequence
        
        
        ####from different directories 
        directory, basename = os.path.split(seq.filepath)
        #n, vid_directories = get_directorynumber(directory[:-1], vid_directories)
        targetpath, vid_directories = get_video_target_path(context, seq.filepath, vid_directories)
        #vid_directories[directory] = targetpath
     
        
        if seq.filepath not in filepathes:
            print(f'found {seq.filepath} already in filepathes')
            filepathes[seq.filepath] = targetpath 
            #filepathes.append(seq.filepath)
        else:
            print(f'found {seq.filepath} already in filepathes')
    elif type == 'SOUND': #hasattr(seq, "sound"): #audio sequence
        directory, basename = os.path.split(seq.sound.filepath)
        
        targetpath, audio_directories, vid_directories = get_audio_target_path(context, seq.sound.filepath,  audio_directories, vid_directories)
        #audio_directories[directory] = targetpath
        
        if seq.sound.filepath not in filepathes:
            filepathes[seq.sound.filepath] = targetpath
        else:
            print(f'found {seq.sound.filepath} already in filepathes') 
    elif type == 'IMGSEQ' or type == 'IMAGE': #  hasattr(seq, "directory"):#image sequence
        directory = seq.directory
        directory = equalize_directory(directory)
        print(f'########equalized {directory}')
        #n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
        targetpath, imgseq_directories = get_imgseq_target_path(context, seq.elements[0].filename, directory, imgseq_directories)
        #imgseq_directories[directory] = targetpath
        
        for ele in seq.elements:
            filepath = os.path.join(directory, ele.filename) ####function naming confusing
            print(f'Image sequence element {ele.filename} und resulating path {filepath} with imgseq {imgseq_directories}')
            if filepath not in filepathes:
                
                filepathes[filepath] = os.path.join(imgseq_directories[directory], ele.filename)  

    return filepathes, imgseq_directories, vid_directories, audio_directories, font_directories

def equalize_directory(directory):
    f = os.path.join(directory, "dump.mp3")
    directory, dump = os.path.split(f)
    return directory

def collect_originals(context):
    arch_props = context.scene.vse_archiver
    
    arch_props.target_folder = bpy.path.abspath(arch_props.target_folder)
    
    print(arch_props.target_folder)
    ###make pathes absolut
    bpy.ops.file.make_paths_absolute()

    
    ###src target in dictionary
    filepathes = {}
    imgseq_directories = {}
    vid_directories = {}
    audio_directories = {}
    font_directories = {}
        
    for scene in bpy.data.scenes:
        sequences = scene.sequence_editor.sequences_all
        # collect filepath of linked vse elements and sort out doubles 
        for seq in sequences[:]: 
            filepathes, imgseq_directories, vid_directories, audio_directories, font_directories = sequence_to_copy(context, seq, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories)

    # check non-vse part for elements to copy 
    if arch_props.use_blend_data:
        filepathes, audio_directories, vid_directories = collect_sounds(context, filepathes, audio_directories, vid_directories) 
        filepathes, vid_directories = collect_moviclips(context, filepathes, vid_directories)
        filepathes, font_directories = collect_fonts(context, filepathes, font_directories)
        filepathes, imgseq_directories = collect_images(context, filepathes, imgseq_directories)

    
    
    errorlist = copy_files(filepathes)
    if len(errorlist) != 0:
        write_texteditor(context, errorlist)

    if arch_props.rebuild:
        build_blend_from_original(context, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories)
        
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
                
def save_blend_file(context):
    arch_props = context.scene.vse_archiver
    from pathlib import Path
    
    orifilepath, basename =  split_filepath(bpy.data.filepath)
    
    #Path(dirname, filename).with_suffix(suffix)
    targetblendfilepath = os.path.join(arch_props.target_folder, basename)
    
    #save as blendfile to new folder
    bpy.ops.wm.save_as_mainfile(filepath=targetblendfilepath) 

def get_rebuildPath_from_filepathes(context, orifilepath, filepathes):
    for path in filepathes:
        if path == orifilepath:
            print(f'######## in get rebuild path found path {path} to return from filepathes {filepathes[path]}')
            return filepathes[path]
    #orifilepath, basename =  split_filepath(orifilepath)
    print(f'#####COULDNT FIND orifilepath {orifilepath} in filepathes , send to basefolder insted ##########!!!!!!!!!!!!!! ')
    #check in targetfolders because
    for target in contentlist_from_dictionary(filepathes):
        if target == orifilepath:
            return orifilepath
        
    print('rebuild failed') ####################### prompt user

def build_blend_from_original(context, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories):
    arch_props = context.scene.vse_archiver
    #save as new blend in the folder 
    save_blend_file(context)
    for sc in bpy.data.scenes:
        sc.vse_archiver.is_archiv = True
        
    sequences = context.scene.sequence_editor.sequences_all
    #pro sequence, strip filename from path, add filename to target folder path and replace filepath in sequence
    
    #print(f'image sequence directories are {filepathes}')
    for scene in bpy.data.scenes:
        sequences = scene.sequence_editor.sequences_all
        
        for seq in sequences: 
            #print(seq.name)
            type = get_sequence_type(seq)
            if type == 'MOVIE': #hasattr(seq, "filepath"):
                seq.filepath = get_rebuildPath_from_filepathes(context, seq.filepath, filepathes)
            elif type == 'SOUND':# hasattr(seq, "sound"):
                seq.sound.filepath = get_rebuildPath_from_filepathes(context, seq.sound.filepath, filepathes)   
            elif type == 'IMGSEQ' or type == 'IMAGE':####is image, not nice
                directory = seq.directory
                directory = equalize_directory(directory)
                #print(f'image sequence directories are {imgseq_directories}')
                #n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                seq.directory = imgseq_directories[directory] 

    if arch_props.use_blend_data:
        remap_moviclips(context, filepathes)
        remap_sounds(context, filepathes)
        remap_images(context, filepathes)
        remap_fonts(context, filepathes)
        
    bpy.ops.file.make_paths_relative()
    save_blend_file(context)
    
    
##### snippets ######################################################################################################################
###main function to started by collect snippets operator ####################################################################################
def collect_snippets(context): 
    arch_props = context.scene.vse_archiver 
    filepathes ={}
    imgseq_directories = {}
    vid_directories = {}
    audio_directories = {}
    font_directories = {}
    
    
    bpy.ops.file.make_paths_absolute()
    
    arch_props.target_folder = bpy.path.abspath(arch_props.target_folder)
    #print(d)
    homogenous_addon_settings_over_scene(context)
    set_rendersettings(context)
    oriscenename = copy.copy(context.window.scene.name)
    oriscenerenderpath = copy.copy(context.window.scene.render.filepath)
    
    #  gehe durch sequences
    for scene in bpy.data.scenes:
        if hasattr(scene, 'vse_archiver'):
            #set scene active 
            context.window.scene = scene

            #in cases user is in metastrip
            find_toplevel(context, scene, context.sequences)
            sequences = get_sequences_4process(context, scene) #scene.sequence_editor.sequences[:] #get_visible_sequences(scene)#
            #print(bb)
            if arch_props.remove_fade:
                #remove memory of old keyframes
                scene.vse_archiver.keys.clear()
                keylist = get_fades(scene, sequences) #all_vis
                remove_fades(scene, sequences)
                #print(bb)
            
            all_vis_seqs = get_all_visible_sequences(scene)
            #print(f'scene {scene.name} sequences found {sequences}')
            
            filepathes, imgseq_directories, vid_directories, audio_directories, font_directories, new_seqs = copy_render_decider(context, scene, filepathes, imgseq_directories, sequences, vid_directories, audio_directories, font_directories)
            print(f'seems to be done with all sequences of {scene}')   
            all_vis_seqs.extend(new_seqs)
            
            set_sequences_visibility(all_vis_seqs, scene)
    
    #go to original scene
    context.window.scene = bpy.data.scenes[oriscenename]
    context.window.scene.render.filepath = oriscenerenderpath
    
    if arch_props.use_blend_data:
        filepathes, audio_directories, vid_directories = collect_sounds(context, filepathes, audio_directories, vid_directories) 
        filepathes, vid_directories = collect_moviclips(context, filepathes, vid_directories)
        filepathes, font_directories = collect_fonts(context, filepathes, font_directories)
        filepathes, imgseq_directories = collect_images(context, filepathes, imgseq_directories)
        
    copy_files(filepathes)
                
    if context.scene.vse_archiver.rebuild:
        build_blend_from_original(context, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories)
        #save_blend_file(context)

def get_sequences_4process(context, scene):
    seqs = []
    sequences = scene.sequence_editor.sequences 
    for seq in sequences:
        answer = copy_or_render(context, scene, seq)
        if answer == 'META' or answer == 'RENDER' or answer == 'COPY':
            seqs.append(seq)
    print(f'seqs 4 processing {seqs}')
    return seqs



def homogenous_addon_settings_over_scene(context):
    
    
    for sc in bpy.data.scenes:
        va = sc.vse_archiver
        va.rebuild = context.scene.vse_archiver.rebuild
        va.remove_fade = context.scene.vse_archiver.remove_fade
        va.render_sound = context.scene.vse_archiver.render_sound
        va.render_image = context.scene.vse_archiver.render_image
        va.render_imagesequence = context.scene.vse_archiver.render_imagesequence
        va.render_metastrip = context.scene.vse_archiver.render_metastrip
        va.render_movie = context.scene.vse_archiver.render_movie
        va.render_scenestrip = context.scene.vse_archiver.render_scenestrip
        
        va.target_audio_folder = context.scene.vse_archiver.target_audio_folder
        va.target_folder = context.scene.vse_archiver.target_folder
        va.target_font_folder = context.scene.vse_archiver.target_font_folder
        va.target_image_folder = context.scene.vse_archiver.target_image_folder
        va.target_imgseq_folder = context.scene.vse_archiver.target_imgseq_folder
        va.target_snippet_folder = context.scene.vse_archiver.target_snippet_folder
        va.target_video_folder = context.scene.vse_archiver.target_video_folder
        
        va.use_blend_data = context.scene.vse_archiver.use_blend_data
                
def copy_render_decider(context, scene, filepathes, imgseq_directories, sequences, vid_directories, audio_directories, font_directories):
    #percent = len(sequences+1)/10
    #context.window_manager.progress_begin(0,len(sequences)+1)
    new_seqs=[]
    for seq in sequences[:]:
        print(f'START PROCESSING SEQuence {seq.name}------------------------------------------------')
        #context.window_manager.progress_update(n)
        answer = copy_or_render(context, scene, seq)
        print(f'for seq {seq.name} got answer {answer}')
        
        if answer == 'COPY':
            filepathes, imgseq_directories, vid_directories, audio_directories, font_directories = sequence_to_copy(context, seq, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories)
        elif answer == 'RENDER':
            filepathes, vid_directories, new_seqes, imgseq_directories = render_sequence(context, seq, scene, False, filepathes, vid_directories, imgseq_directories)
            new_seqs.extend(new_seqes)
        elif answer == 'META':
            filepathes, imgseq_directories, vid_directories, audio_directories, font_directories, new_seqes = render_meta_snipets(context, scene, seq, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories)
            new_seqs.extend(new_seqes)
        elif answer == 'IGNORE':
            print(f'ignored sequence {seq.name}')
        else:
            print(f'weird answer {answer}')
    
    context.window_manager.progress_end()
    print(f'after copy_render_decider new seqs {new_seqs}')
    
    return filepathes, imgseq_directories, vid_directories, audio_directories, font_directories, new_seqs
                
#supposed to toggle meta strips to the toplevel, but bugged when sequences kein meta_parent()            
def find_toplevel(context, scene, sequences):
    #print(sequences)
    if len(sequences) != 0:
        if sequences[0].parent_meta() != None:
            #deselect all 
            for s in scene.sequence_editor.sequences_all:
                s.select = False 
            #toogle 
            bpy.ops.sequencer.meta_toggle()

            #test again
            sequences = context.sequences #get_visible_sequences(scene)
            find_toplevel(context, scene, sequences)
    
def get_visible_sequences(scene):
    vis = []
    ###used to identify start condition, don't use _all
    for seq in scene.sequence_editor.sequences:
        if not seq.mute:
            vis.append(seq)
    return vis

def get_all_visible_sequences(scene):
    vis = []
    ###used to identify start condition, don't use _all
    for seq in scene.sequence_editor.sequences_all:
        if not seq.mute:
            vis.append(seq)
    return vis

def set_sequences_visibility(vis_seqs, scene):
    for seqvis in vis_seqs:
        #print(f'visible sequences after render are {vis_seqs}')
        for seq in scene.sequence_editor.sequences_all:
            if seq == seqvis:
                seq.mute = False
                break
            #else:    
             #   print(f'*********************found none fitting seq  in seq_all , {seqvis}')

def get_effectstrip_cascade(seq, seqs):
    #print(f'seq {seq} at start of effecstrip cascade seqs {seqs}')
    if hasattr(seq, 'input_1'):
        if seq.input_1 != None:
            #ist in input der Renderrelevanter strip
            if seq.input_1 in seqs:
                if seq not in seqs:
                    seqs.append(seq)
            else:
                ### wenn nicht direkt rendererelevant, 
                # hat es dann vielleicht effekt strips untersich die gerendert werd
                seqs = get_effectstrip_cascade(seq.input_1, seqs)
            
    
    return seqs

def set_vis_for_render(seqs, scene):
    
    #adjust for metastrip
    print(f'seqs before everything {seqs}')
    for m_seq in seqs:
        type = get_sequence_type(m_seq)
        
        if type == 'META':
            print(f'mseqs type {type}')
            for se in m_seq.sequences:
                print(f'se {se.name}')
                if se.mute == False:
                    print(f'is false {se.name}')
                    if se not in seqs:
                        seqs.append(se)
                    #print(bb)
            
    print(f'seqs plus meta {seqs}')
    
    #find effect strips 
    for a_seq in scene.sequence_editor.sequences_all:
        seqs = get_effectstrip_cascade(a_seq, seqs)
    print(f'seqs before parent {seqs}')
    
    #parent case sequence in meta --> vis meta true
    for p_seq in seqs:
        parent = p_seq.parent_meta()
        if parent != None: 
            if parent.mute == False:###richtig???
                if parent not in seqs:
                    seqs.append(parent)
    print(f'seqs after effectstrip cascade {seqs}')
            
    #####don't set vis false when its a speed track or other effect strip 
    for sequ in scene.sequence_editor.sequences_all:
        sequ.mute = True
    for seq in seqs:    
        seq.mute = False
    #print('necessary seq muted')
    #print(brak)
    
def set_rendersettings(context):
    for sc in bpy.data.scenes:
        sc.render.image_settings.file_format = context.scene.render.image_settings.file_format #'FFMPEG'
        sc.render.ffmpeg.format = context.scene.render.ffmpeg.format  #'MPEG4'
        sc.render.ffmpeg.audio_codec = context.scene.render.ffmpeg.audio_codec #'AAC'
        sc.render.ffmpeg.use_autosplit = context.scene.render.ffmpeg.use_autosplit
        sc.render.ffmpeg.codec = context.scene.render.ffmpeg.codec
        sc.render.ffmpeg.constant_rate_factor = context.scene.render.ffmpeg.constant_rate_factor
        sc.render.ffmpeg.ffmpeg_preset = context.scene.render.ffmpeg.ffmpeg_preset
        sc.render.ffmpeg.gopsize = context.scene.render.ffmpeg.gopsize
        sc.render.ffmpeg.max_b_frames = context.scene.render.ffmpeg.max_b_frames
        sc.render.ffmpeg.audio_codec = context.scene.render.ffmpeg.audio_codec
        sc.render.ffmpeg.audio_channels = context.scene.render.ffmpeg.audio_channels
        sc.render.ffmpeg.audio_mixrate = context.scene.render.ffmpeg.audio_mixrate
        sc.render.ffmpeg.audio_bitrate = context.scene.render.ffmpeg.audio_bitrate
        sc.render.ffmpeg.audio_volume = context.scene.render.ffmpeg.audio_volume
        
        sc.render.image_settings.color_mode = context.scene.render.image_settings.color_mode
        sc.render.image_settings.color_depth = context.scene.render.image_settings.color_depth
        sc.render.image_settings.quality = context.scene.render.image_settings.quality
        sc.render.image_settings.compression = context.scene.render.image_settings.compression
        sc.render.image_settings.jpeg2k_codec = context.scene.render.image_settings.jpeg2k_codec
        sc.render.image_settings.use_jpeg2k_cinema_preset = context.scene.render.image_settings.use_jpeg2k_cinema_preset
        sc.render.image_settings.use_jpeg2k_cinema_48 = context.scene.render.image_settings.use_jpeg2k_cinema_48
        sc.render.image_settings.use_jpeg2k_ycc = context.scene.render.image_settings.use_jpeg2k_ycc
        sc.render.image_settings.exr_codec = context.scene.render.image_settings.exr_codec
        #sc.render.image_settings.use_zbuffer = context.scene.render.image_settings.use_zbuffer
        sc.render.image_settings.use_preview = context.scene.render.image_settings.use_preview
        sc.render.image_settings.tiff_codec = context.scene.render.image_settings.tiff_codec
        
        
def render_sequence(context, seq, scene, is_meta, filepathes, vid_directories, imgseq_directories):
    arch_props = scene.vse_archiver
    #remember fade 
    #remember frame range 
    init_start = copy.copy(scene.frame_start)
    init_end = copy.copy(scene.frame_end)

    ##!!!!!!!!!!!! problems when negativ !!!!!!!!!!!
    render_start = seq.frame_final_start
    render_end = seq.frame_final_end
    
    # set new frame range 
    scene.frame_start = render_start
    scene.frame_end = render_end
    # copy list of visible sequences 
    ori_vis_seqs = get_all_visible_sequences(scene) #get_visible_sequences(scene)
    
    
    #hide_all sequences but the active and effect
    if not is_meta:
        set_vis_for_render([seq], scene)
    
    ###handle fade
    
    
    #generate a fade keyframes from the visible sequences
    all_vis = get_all_visible_sequences(scene)
    
    oldname=copy.copy(seq.name)
    print(f' oldname {oldname} seq {seq.name}')
    #print(bb)
    
    # set new name and folder rendering
    filepath = os.path.join(arch_props.target_folder, context.scene.name)
    filepath = os.path.join(filepath, arch_props.target_snippet_folder)
    FakeOrifilepath = os.path.join(filepath, seq.name)
    #actually filepath, try how split reachts to a simple name
    renderpath, vid_directories = get_video_target_path(context, FakeOrifilepath, vid_directories) 
    
    
    ###render to image case 
    is_image, not_ffmpeg, no_audio, no_videocodec = check_rendersettings(context)
    
    if not is_image:    
        renderpath = renderpath + get_extension(context)
    else:
        dirpath, basename = os.path.split(renderpath)
        if dirpath not in imgseq_directories:
            imgseq_directories[dirpath] = dirpath
            #basename += str(render_start)

    scene.render.filepath = renderpath
    context.scene.render.filepath = renderpath
    
    
    
    
    
    # render sequence 
    bpy.ops.render.render(animation=True)

    
    # reset 
    scene.frame_start = init_start
    scene.frame_end = init_end
    
    if not is_meta:
        set_sequences_visibility(ori_vis_seqs, scene)
    
    if arch_props.rebuild:
        new_seqes = replace_sequence_w_rendered(context, scene, seq, renderpath)
    
    
    
    
    
    
    ##filepathes only meant for copying original files
    target_directory, basename = os.path.split(renderpath)
    filepathes[os.path.join(target_directory, basename)] = os.path.join(target_directory, basename)
    #print(f'rendered {new_seq.name} and saved oripath {FakeOrifilepath}  render path {renderpath}')
    
    return filepathes, vid_directories, new_seqes, imgseq_directories
        
def replace_sequence_w_rendered(context, scene, seq, newfilepath):
    parent = seq.parent_meta()
    newseqes = []
    
    #####warum gehts in parent? 
    if parent == None: 
        sequences = scene.sequence_editor.sequences    
    else: 
        sequences = parent.sequences
    
    ##new sequence 
    type = get_sequence_type(seq)
    is_image, not_ffmpeg, no_audio, no_videocodec = check_rendersettings(context)
    if not is_image:
        if type == 'META':# or  type == 'SCENE':
            #make meta
            newseq = sequences.new_meta(seq.name+'replaced', channel = seq.channel, frame_start = seq.frame_final_start)
            newseq.frame_final_end = seq.frame_final_end
            
            #
            newmovie = newseq.sequences.new_movie(seq.name+'movreplaced', newfilepath, channel = seq.channel+1, frame_start = seq.frame_final_start)
            newsound = newseq.sequences.new_sound(seq.name+'audreplaced', newfilepath, channel = seq.channel, frame_start = seq.frame_final_start)
            newseqes = [newseq, newmovie, newsound] ### fade take the first of this list
        elif type == 'SOUND':
            newseq = sequences.new_sound(seq.name+'replaced', newfilepath, channel = seq.channel, frame_start = seq.frame_final_start)
            newseqes = [newseq]
            newseq.frame_final_end = newseq.frame_final_end - 1
        elif  type == 'SCENE':
            newseq = sequences.new_meta(seq.name+'replaced', channel = seq.channel, frame_start = seq.frame_final_start)
            newseq.frame_final_end = seq.frame_final_end
            newmovie = newseq.sequences.new_movie(seq.name+'movreplaced', newfilepath, channel = seq.channel+1, frame_start = seq.frame_final_start)
            newsound = newseq.sequences.new_sound(seq.name+'audreplaced', newfilepath, channel = seq.channel, frame_start = seq.frame_final_start)
        else:
            newseq = sequences.new_movie(seq.name+'replaced', newfilepath, channel = seq.channel, frame_start = seq.frame_final_start)
            newseqes = [newseq]
            newseq.frame_final_end = newseq.frame_final_end - 1
    else: 
        
        ######needs a zero when smaller 1000
        #print(len(str(seq.frame_final_start)))
        #zero = str(seq.frame_final_start).zfill(4) ###could be blenders internal number for this thing
        #newfilepath += zero + str(seq.frame_final_start) + get_extension(context)
        path, basename = os.path.split(newfilepath)
        
        
        # rendering image sequences 
        newseq = sequences.new_image(seq.name+'replaced', newfilepath+ str(seq.frame_final_start).zfill(4)+get_extension(context), channel = seq.channel, frame_start = seq.frame_final_start)
        
            
        append_img_elements(context, newseq, basename, seq.frame_final_start+1, seq.frame_final_end) 
        #newseq.elements.pop(0) 
        
        if type == 'META':
            newseq.frame_final_end -= 1 
        elif  type == 'SCENE':
            newseq.frame_final_end -= 1 
        elif type == 'IMAGE':
            newseq.frame_final_end -= 1 
        elif type == 'IMGSEQ':
            newseq.frame_final_end -= 1 
        elif type == 'Movie':
            newseq.frame_final_end -= 1 
        else:
            newseq.frame_final_end -= 1 
        
    if scene.vse_archiver.remove_fade:
        reset_fade_keyframes(scene, seq.name, newseq)
    
    channel = copy.copy(seq.channel)
    #if not type == 'META':
    for seq_cont in sequences:
        if seq == seq_cont:
            sequences.remove(seq)

    newseq.channel = channel
        
    return newseqes

def append_img_elements(context, newseq, basename, start, end):
    ext = get_extension(context)
    
    i = start
    while i <= end:
        name = basename + str(i).zfill(4)
        name += ext
        newseq.elements.append(name)
        i += 1
    #dsf     
        

def get_extension(context):
    format = context.scene.render.image_settings.file_format # 'FFMPEG', 'AVI_RAW', 'AVI_JPEG', 'WEBP', 'TIFF', 'HDR', 'OPEN_EXR', 'OPEN_EXR_MULTILAYER', 'DPX', 'CINEON', 'TARGA_RAW', 'TARGA', 'JPEG2000', 'JPEG2000', 'PNG', 'IRIS', 'BMP'
    
    if format =='FFMPEG':
        ffmpegformat =  context.scene.render.ffmpeg.format
        if ffmpegformat == 'MPEG1': 
            return '.mpg'
        if ffmpegformat == 'MPEG2': 
            return '.dvd'
        if ffmpegformat == 'MPEG4': 
            return '.mp4'
        if ffmpegformat == 'MPEG4': 
            return '.mp4'
        if ffmpegformat == 'AVI': 
            return '.avi'
        if ffmpegformat == 'QUICKTIME': 
            return '.mov'
        if ffmpegformat == 'DV': 
            return '.dv' #?????????????????????????????????
        if ffmpegformat == 'OGG': 
            return '.ogv'
        if ffmpegformat == 'MKV': 
            return '.mkv'
        if ffmpegformat == 'FLASH': 
            return '.flv'
        if ffmpegformat == 'WEBM': 
            return '.webm'
        
    if format =='AVI_RAW':
        return '.avi'
    if format =='AVI_JPEG':
        return '.avi'
    if format =='WEBP':
        return '.webp'
    if format =='TIFF':
        return '.tif'
    if format =='HDR':
        return '.hdr'
    if format =='OPEN_EXR':
        return '.exr'
    if format =='OPEN_EXR_MULTILAYER':
        return '.exr'
    if format =='DPX':
        return 'dpx'
    if format =='CINEON':
        return '.cin'
    if format =='TARGA_RAW':
        return '.tga'
    if format =='TARGA':
        return '.tga'
    if format =='JPEG':
        return '.jpg'
    if format =='JPEG2000':
        return '.jp2'
    if format =='PNG':
        return '.png'
    if format =='IRIS':
        return '.rgb'
    if format =='BMP':
        return '.bmp'
    else: 
        return '.mp4'

def get_seqdata_from_seq(context, seq):
    
    for ele in context.scene.vse_archiver.sequences:
        if ele.name == seq.name:
            return ele
        
def get_metadata_from_seq(context, seq):
    for ele in context.scene.vse_archiver.metastrips:
        if ele.name == seq.name:
            return ele

def copy_or_render(context, scene, seq):
    arch_props = scene.vse_archiver 

    type = get_sequence_type(seq)
    if type == 'IGNORE':
        #print(f'Ignored Sequence {seq.name} type {seq.type}')
        return 'IGNORE'

    
    if type == 'IMAGE':
        #print(f'found image {seq.name} render_image {arch_props.render_image}')
        if get_seq_render_tag(scene, seq): #arch_props.render_image and
            return 'RENDER'
        else:
            return 'COPY'
    
    if type == 'IMGSEQ':
        #print(f'found Imgseq {seq.name} render_imageseq {arch_props.render_imagesequence}')
        if get_seq_render_tag(scene, seq):
            return 'RENDER'
        else:
            return 'COPY'        

    if type == 'SCENE':
        #print(f'found scene {seq.name} render_scenestrip {arch_props.render_scenestrip}')
        if get_seq_render_tag(scene, seq):
            return 'RENDER'
        else:
            return 'COPY'
        
    if type =='SOUND':
        if get_seq_render_tag(scene, seq): #arch_props.render_sound and 
            #dont render audio
            is_image, not_ffmpeg, no_audio, no_videocodec = check_rendersettings(context)
            if not  is_image:
                return 'RENDER'
            else:
                return 'COPY'
        else:
            return 'COPY'
    if type == 'META':
        return 'META'

    if type == 'MOVIE':
        if get_seq_render_tag(scene, seq):  #arch_props.render_movie and
            return 'RENDER'
        else:
            return 'COPY'
    
def get_seq_render_tag(scene, seq):
    for s in scene.vse_archiver.sequences:
        if s.name == seq.name:
            return s.pls_render
        
        
    for s in scene.vse_archiver.metastrips:
        if s.name == seq.name:
            return s.render_inside
    
    print('!!!!!!!!!!!!!!!!!! No RENDER TAG FOUND!!!!!!!!!!!') 


def get_sequence_type(seq): 
    #print(f'get sequence bug seq.name {seq.name}')
    
    if seq.type == 'MOVIE': #hasattr(seq, "filepath"): #videosequence
       return 'MOVIE'  
    elif seq.type == 'SOUND': # hasattr(seq, "sound"): #audio sequence
        return 'SOUND'
    elif seq.type == 'IMAGE': #hasattr(seq, "directory"):#image sequence
        if len(seq.elements) == 1:
            return 'IMAGE'
        elif len(seq.elements) == 0:
            return 'IGNORE'
        else:
            return 'IMGSEQ'
    elif seq.type == 'META':
        return 'META'
    elif seq.type == 'SCENE':
        return 'SCENE'
    else:
        return seq.type
    
    
    
def render_meta_snipets(context, scene, seq, filepathes, imgseq_directories, vid_directories, audio_directories, font_directories):
    new_seqs = []
    ##for rendering only the inside stuff 
    print(f'For MEtastrip {seq.name} in render meta snippets is_render_elements {is_render_elements(context, scene, seq)}')
    vis_seqs = get_all_visible_sequences(scene)
    # should the elements be rendered individually? 
    if is_render_elements(context, scene, seq):
        filepathes, imgseq_directories, vid_directories, audio_directories, font_directories, new_seqs = copy_render_decider(context, scene, filepathes, imgseq_directories, seq.sequences, vid_directories, audio_directories, font_directories) 
        vis_seqs.extend(new_seqs)
        set_sequences_visibility(vis_seqs,scene)
    #   yes: send individual elements to be rendered render_sequence(context, seq, scene, is_meta) 
    #   NO: send this meta strip to render_sequence(context, seq, scene, is_meta)
    else: 
        #get metastrip elements 
        #print(f'-------------------------- who is the transform guide {seq}')
        elements =[seq]
        for subseq in seq.sequences:
            if subseq not in elements:
                if subseq.mute == False:
                    elements.append(subseq)
        
        ##find effekt strips
        
        
        #set visibility for elements (careful will be set in render_sequences again)
        set_vis_for_render(elements, scene)
        #print(bb)
        filepathes, vid_directories, new_seqes, imgseq_directories = render_sequence(context, seq, scene, True, filepathes, vid_directories, imgseq_directories)
        
        vis_seqs.extend(new_seqes)
        new_seqs.extend(new_seqes)
        
        
        print(f'vis_seqs after meta strip render {vis_seqs}')
    set_sequences_visibility(vis_seqs,scene)
    #print(bb)
    return filepathes, imgseq_directories, vid_directories, audio_directories, font_directories, new_seqs


def is_render_elements(context, scene, seq): 
    arch_metastrips = scene.vse_archiver.metastrips
    for ele in arch_metastrips:
        if ele.name == seq.name:
            return ele.render_inside
    print('couldnt finds render element')


def reset_metastrips(context):
    for sc in bpy.data.scenes:
        #sequences = sc.sequence_editor.sequences_all
        arch_metastrips = sc.vse_archiver.metastrips
        
        
        arch_metastrips.clear()
    update_metastrips(context)

####adds metastrips that are not present yet in the list ; renaming strips,  after making   
def update_metastrips(context):
    print('in updates ') 

    ######################PROBLEM In verschiedenen Scenen können Strips den gleich namen haben, nur nicht innerhalb der scene, aber es ist ja eh per scene gespeichert 
    for sc in bpy.data.scenes:
        sequences = sc.sequence_editor.sequences_all
        arch_metastrips = sc.vse_archiver.metastrips
        
        for seq in sequences:
            #print(f'seq {seq.name} ')
            if seq.type == 'META':
                if seq.name not in arch_metastrips:
                    print(f'ele {seq.name} ')
                    ele = arch_metastrips.add()
                    ele.name = seq.name 
    
        ####looks for old metastrip data with no counter part in the current state  
        for n,ele in enumerate(arch_metastrips[:]):
            if ele.name not in sequences:
                arch_metastrips.remove(n)
               
               
def reset_sequences_data(context):
    for sc in bpy.data.scenes:
        vse_archiver = sc.vse_archiver
        vse_archiver.sequences.clear()
    
    update_sequences_data(context)

##resets all sequence data for a specific type
def reset_seq_by_type(context, type):
    vse_archiver = context.scene.vse_archiver
    if type != 'META':
        for sc in bpy.data.scenes:
            seqs = sc.vse_archiver.sequences
            for seq in seqs:
                if seq.type == type:
                    if type == 'MOVIE':
                        seq.pls_render = vse_archiver.render_movie
                        #sc.vse_archiver.render_movie = vse_archiver.render_movie
                    elif type == 'SOUND':
                        seq.pls_render = vse_archiver.render_sound
                        #sc.vse_archiver.render_sound = vse_archiver.render_sound
                    elif type == 'IMAGE':
                        seq.pls_render = vse_archiver.render_image
                        #sc.vse_archiver.render_image = vse_archiver.render_image
                    elif type == 'IMGSEQ':
                        seq.pls_render = vse_archiver.render_imagesequence
                        #sc.vse_archiver.render_imagesequence = vse_archiver.render_imagesequence
                    elif type == 'SCENE':
                        seq.pls_render = vse_archiver.render_scenestrip
                        #sc.vse_archiver.render_scenestrip = vse_archiver.render_scenestrip
    else:
        for sc in bpy.data.scenes:
            seqs = sc.vse_archiver.metastrips
            for seq in seqs:
                if seq.type == 'META':
                    seq.render_inside = not vse_archiver.render_metastrip


####adds metastrips that are not present yet in the list ; renaming strips,  after making   
def update_sequences_data(context):
    print('in update sequences') 

    ######################PROBLEM In verschiedenen Scenen können Strips den gleich namen haben, nur nicht innerhalb der scene, aber es ist ja eh per scene gespeichert 
    for sc in bpy.data.scenes:
        sequences = sc.sequence_editor.sequences_all
        vse_archiver = sc.vse_archiver
        arch_sequences = sc.vse_archiver.sequences
        
        for seq in sequences:
            #print(f'seq {seq.name} ')
            
            if seq.name not in arch_sequences:
                type = get_sequence_type(seq)
                if type in ['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']:
                    print(f'ele {seq.name} ')
                    ele = arch_sequences.add()
                    ele.name = seq.name 
                    ele.type = type
                    if type == 'MOVIE':
                        ele.pls_render = vse_archiver.render_movie
                    elif type == 'SOUND':
                        ele.pls_render = vse_archiver.render_sound
                    elif type == 'IMAGE':
                        ele.pls_render = vse_archiver.render_image
                    elif type == 'IMGSEQ':
                        ele.pls_render = vse_archiver.render_imagesequence
                    elif type == 'SCENE':
                        ele.pls_render = vse_archiver.render_scenestrip
                
                
                
    
        ####looks for old metastrip data with no counter part in the current state  
        for n,ele in enumerate(arch_sequences[:]):
            if ele.name not in sequences:
                arch_sequences.remove(n)
                
                
def remove_fades(scene, seqs):
    print('in remove fades')
    print_list(seqs)
    for seq in seqs:
        fcs = fade_fcs(scene, seq)
        print_list(fcs)
        if len(fcs) !=  0:
            for fc in fcs[:]:
                print(f'removed fc {fc.data_path}')
                s = get_attr_from_string(scene, fc.data_path)
                scene.animation_data.action.fcurves.remove(fc)
                if hasattr(s, 'volume'):
                    s.volume = 1.0
                elif hasattr(s, 'blend_alpha'):
                    s.blend_alpha = 1.0
                


def get_attr_from_string(scene, txt):
    #from operator import attrgetter
    #return attrgetter(txt)(ob)
    '''path_ele = txt.split('.')
    print(path_ele)
     
    for ele in path_ele:
        print(ele)
        ob = getattr(ob, ele) 
        
    return ob'''
     
    scan = False
    for n, t in enumerate(txt):
        #print(t)
        ##ignore strings 
        if t == "'" or t == '"':
            if not scan:
                start = n 
                scan = not scan
            else:
                end = n
                break
    seq_name = txt[start+1:end]
    seq = scene.sequence_editor.sequences_all[seq_name]
    
    #attribute
    #eles= txt.split('.')
    #attr = getattr(seq, eles[-1])
    
    return seq  

    
    
                
def get_fades(scene, seqs):
    #find fade data 
    keylist = []
    for seq in seqs:
        fcs = fade_fcs(scene, seq)
        if len(fcs) !=  0:
            for fc in fcs:
                keylist.extend(get_fade_keydatalist(scene, seq, fc))
    return keylist
            


def fade_fcs(scene, seq):
    fcs = []
    if hasattr(scene.animation_data, 'action'):
        if hasattr(scene.animation_data.action, 'fcurves'):
            for fc in scene.animation_data.action.fcurves:
                print(f'fc data path {fc.data_path}')
                if fadetypes_in_datapath(fc.data_path):
                    print(f'check1 seq name {seq.name}')
                    l = fc.data_path.split('"')
                    namefromDatapath = l[-2]
                    if seq.name == namefromDatapath:
                        print('check2')
                        print(f'found fcurve of seq {seq.name} with data path {fc.data_path} check {namefromDatapath}')
                        
                        fcs.append(fc)            
    return fcs
    #return None
            

def fadetypes_in_datapath(data_path):
    if 'blend_alpha' in data_path:
        return True
    if 'volume' in data_path:
        return True

    return False


#get the keydata 
def get_fade_keydatalist(scene, seq, fc):
    keys = scene.vse_archiver.keys
    keylist = []
    for key in fc.keyframe_points:
        new = keys.add()
        new.seq_name = seq.name
        new.data_path= fc.data_path
        new.frame = key.co[0]
        new.value = key.co[1]
        new.handle_right_type=key.handle_right_type
        new.handle_left_type=key.handle_left_type
        l = fc.data_path.split('.')
        new.attr = l[-1]
        keylist.append(new)
    return keylist



def reset_fade_keyframes(scene, oldname, newseq):
    print('in reset fade')
    #keys = scene.vse_archiver.keys
    #print_list(keys)
    print(f'{newseq.name} fade stuff')
    keys = scene.vse_archiver.keys
    
    for key in keys:
        if key.seq_name == oldname:
            print(f'data path {key.data_path}')
            print(f'old name {oldname}')
            data_path = key.data_path.replace(oldname, newseq.name)
            newkey = scene.keyframe_insert(data_path)
            print(f'odl name {oldname} data path {data_path}') 
            set_keyframes(scene, newseq, key.attr,  key.value, key.frame)
            #newkey.co = (key.frame, key.value)
            
    
    
    
    '''context.scene.frame_current = start[0]
    mod.time = start[1]
    mod.keyframe_insert(data_path="time")

    context.scene.frame_current = end[0]
    mod.time = end[1]
    mod.keyframe_insert(data_path="time")

    if hasattr(ocean.animation_data, 'action'):
        for fcu in ocean.animation_data.action.fcurves:
            for keyframe in fcu.keyframe_points:
                keyframe.interpolation = 'LINEAR'''
                
                
def set_keyframes(scene, path, target,  value, frame):
    oriframe = copy.copy(scene.frame_current)
    scene.frame_current = int(frame)
    setattr(path, target, value)

    path.keyframe_insert(data_path=target)

    scene.frame_current = oriframe
    

def open_txt_editor(context,txt):
    context.area.type = 'TEXT_EDITOR'

    context.area.spaces[0].text = txt # make loaded text file visible
    context.area.spaces[0].top = 0
    
def write_texteditor(context,contentlist):

    #make log file
    txt = bpy.data.texts.new(name='VSE_Archiver_log')
    
    for txtelement in contentlist:
        txt.write(txtelement + '\n')
        
    ##
    open_txt_editor(context, txt)
    