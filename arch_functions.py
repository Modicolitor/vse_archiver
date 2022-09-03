import bpy 
import shutil ###copy files with python
import os 
import ntpath
import copy


#
def copy_file(src, dst):
    shutil.copy2(src, dst)

def get_video_target_path(context, filepath):
    arch_props = context.scene.vse_archiver
    targetfolder = arch_props.target_folder
    videofolder = arch_props.target_video_folder
    path, basename = split_filepath(filepath)

    #'target_folder'\videofolder\basename 
    targetpath = os.path.join(targetfolder, videofolder)
    video_target_path = os.path.join(targetpath, basename)
    return video_target_path

def get_audio_target_path(context, filepath):
    arch_props = context.scene.vse_archiver
    targetfolder = arch_props.target_folder
    videofolder = arch_props.target_audio_folder
    path, basename = split_filepath(filepath)

    #'target_folder'\videofolder\basename 
    targetpath = os.path.join(targetfolder, videofolder)
    video_target_path = os.path.join(targetpath, basename)
    return video_target_path

def get_imgseq_target_path(context, filename, n, directory):
    arch_props = context.scene.vse_archiver
    targetfolder = arch_props.target_folder
    imgseqfolder = arch_props.target_imgseq_folder
    #path, basename = split_filepath(filepath)

    #'target_folder'\videofolder\basename 
    targetpath = os.path.join(targetfolder, imgseqfolder)
    print(f'in get target parth {filename}')
    filename, extension = os.path.splitext(filename)
    subfoldername = get_none_numbername(filename) + str(n)
    targetpath = os.path.join(targetpath, subfoldername)
    video_target_path = targetpath 
    return video_target_path

def get_none_numbername(filename):
    forbiddens = ['0','1','2','3','4','5','6','7','8','9','.', ',']
   
    tester = True
    while tester:
        if len(filename) == 0:
            tester = False
        elif filename[-1] in forbiddens:
            print(filename)
            filename = filename[:-1]
        else:
            tester = False
    return filename

def list_from_dictionary(dict):
    list = []
    for ele in dict.keys():
        list.append(ele)
    return list 
    
def get_directorynumber(directory, imgdirectories):
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

def get_target_filepath(filepath, target_folder):
    orifilepath, basename =  split_filepath(filepath)
    return os.path.join(target_folder, basename)



def sequence_to_copy(context, seq, filepathes, imgseq_directories): 
    type = get_sequence_type(context, seq)
    if type == 'MOVIE': #hasattr(seq, "filepath"): #videosequence
        #print(f'this has filepath: {seq.name}')
        if seq.filepath not in filepathes:
            filepathes[seq.filepath] = get_video_target_path(context, seq.filepath)
            #filepathes.append(seq.filepath)
    elif type == 'SOUND': #hasattr(seq, "sound"): #audio sequence
        if seq.sound.filepath not in filepathes:
            #filepathes.append(seq.sound.filepath)
            filepathes[seq.sound.filepath] = get_audio_target_path(context, seq.sound.filepath)
    elif type == 'IMGSEQ': #  hasattr(seq, "directory"):#image sequence
        directory = seq.directory
        n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
        targetpath = get_imgseq_target_path(context, seq.elements[0].filename,n, directory)
        imgseq_directories[directory] = targetpath
        for ele in seq.elements:
            filepath = os.path.join(directory, ele.filename) ####function naming confusing
            print(f'Image sequence element {ele.filename} und resulating path {filepath}')
            if filepath not in filepathes:
                filepathes[os.path.join(directory, ele.filename)] = os.path.join(imgseq_directories[directory], ele.filename)  ##get_imgseq_target_path(context, ele.filename, n, directory)

    return filepathes, imgseq_directories

def collect_originals(context):
    arch_props = context.scene.vse_archiver
    
    ###src target in dictionary
    filepathes = {}
    imgseq_directories = {}
    for scene in bpy.data.scenes:
        sequences = scene.sequence_editor.sequences_all
        # collect filepath of linked vse elements and sort out doubles 
        for seq in sequences: 
            print(seq.name)
            filepathes, imgseq_directories = sequence_to_copy(context, seq, filepathes, imgseq_directories)


    if arch_props.use_blend_data:
                filepathes = collect_moviclips(context, filepathes)
                filepathes = collect_sounds(context, filepathes)
                filepathes, imgseq_directories = collect_images(context, filepathes, imgseq_directories)

    print(filepathes)

    for srcpath in filepathes.items():
        
        targetpath, basename = split_filepath(srcpath[1])
        os.makedirs(targetpath, exist_ok=True)
        copy_file(srcpath[0], targetpath)


    if arch_props.rebuild:
        build_blend_from_original(context, filepathes, imgseq_directories)


def collect_moviclips(context, filepathes):
    data = bpy.data 
    for mc in data.movieclips:
        if mc.filepath  not in filepathes:
            filepathes[mc.filepath] = get_video_target_path(context, mc.filepath)
    return filepathes

def collect_sounds(context, filepathes):
    data = bpy.data 
    for sound in data.sounds:
        if sound.filepath  not in filepathes:
            filepathes[sound.filepath] = get_audio_target_path(context, sound.filepath)
    return filepathes

def collect_images(context, filepathes, imgseq_directories):
    data = bpy.data 
    for img in data.images:
        if img.type == 'IMAGE':
            if img.filepath  not in filepathes:
                directory, basename = os.path.split(img.filepath)
                n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                targetpath = get_imgseq_target_path(context, basename, n, directory)
                imgseq_directories[directory] = targetpath
                
                if img.filepath not in filepathes:
                        filepathes[img.filepath] = os.path.join(imgseq_directories[directory], basename)  ##get_imgseq_target_path(context, ele.filename, n, directory)
                
    return filepathes, imgseq_directories
                #filepathes[img.filepath] = get_video_target_path(context, img.filepath)



def remap_moviclips(context, filepathes):
    data = bpy.data 
    for mc in data.movieclips:
        if mc.filepath  in filepathes:
            mc.filepath = filepathes[mc.filepath] 

def remap_sounds(context, filepathes):
    data = bpy.data 
    for sound in data.sounds:
        if sound.filepath  in filepathes:
            sound.filepath = filepathes[sound.filepath] 

def remap_images(context, filepathes):
    data = bpy.data 
    for img in data.images:
        if img.type == 'IMAGE':
            if img.filepath  in filepathes:
                img.filepath = filepathes[img.filepath]
                
                
                


def build_blend_from_original(context, filepathes, imgseq_directories):
    arch_props = context.scene.vse_archiver
    #save as new blend in the folder 
    from pathlib import Path
    
    orifilepath, basename =  split_filepath(bpy.data.filepath)
    
    #Path(dirname, filename).with_suffix(suffix)
    targetblendfilepath = os.path.join(arch_props.target_folder, basename)
    
    #save as blendfile to new folder
    bpy.ops.wm.save_as_mainfile(filepath=targetblendfilepath) 



    sequences = context.scene.sequence_editor.sequences_all
    #pro sequence, strip filename from path, add filename to target folder path and replace filepath in sequence
    print(f'image sequence directories are {imgseq_directories}')
    print(f'image sequence directories are {filepathes}')
    for scene in bpy.data.scenes:
        sequences = scene.sequence_editor.sequences_all
        
        for seq in sequences: 
            print(seq.name)
            type = get_sequence_type(context, seq)
            if type == 'MOVIE': #hasattr(seq, "filepath"):
                print(f'has filepath: {seq.name}')
                seq.filepath = get_video_target_path(context, seq.filepath) 
            elif type == 'SOUND':# hasattr(seq, "sound"):
                seq.sound.filepath = get_audio_target_path(context, seq.sound.filepath) 
            #image sequences 
            elif type==   hasattr(seq, "directory"):
                
                directory = seq.directory
                
                #n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                seq.directory = imgseq_directories[directory]

    if arch_props.use_blend_data:
        remap_moviclips(context, filepathes)
        remap_sounds(context, filepathes)
        remap_images(context, filepathes)

##### snippets 
###main function to started by collect snippets operator 
def collect_snippets(context): 
    filepathes ={}
    imgseq_directories = {}
    #  gehe durch sequences
    for scene in bpy.data.scenes:
        sequences = scene.sequence_editor.sequences_all
        for seq in sequences:
            answer = copy_or_render(context, seq)
            if answer == 'COPY':
                filepathes, imgseq_directories = sequence_to_copy(context, seq, filepathes, imgseq_directories)
            elif answer == 'RENDER':
                render_sequence(context, seq, scene)
            elif answer == 'IGNORE':
                print(f'ignored sequence {seq.name}')
            else:
                print(f'weird answer {answer}')

    # entscheide render or collect
    # wenn render send to render part 
        
    # wenn collect send to collect system 
    
def get_visible_sequences(scene):
    vis = []
    for seq in scene.sequence_editor.sequences_all:
        if not seq.mute:
            vis.append(seq)
    return vis

def set_sequences_visibility(vis_seq, scene):
    for seqvis in vis_seq:
        for seq in scene.sequence_editor.sequences_all:
            if seq == seqvis:
                seq.mute = False

def set_vis_for_render(seq, scene):
    for seq in scene.sequence_editor.sequences_all:
        seq.mute = True
    seq.mute = False

def render_sequence(context, seq, scene):
    arch_props = context.scene.vse_archiver
    print(f'fake Render ')
    #remember fade 
    #remember frame range 
    init_start = copy.copy(context.scene.frame_start)
    init_end = copy.copy(context.scene.frame_end)

    ##!!!!!!!!!!!! problems when negativ !!!!!!!!!!!
    render_start = seq.frame_start
    render_end = seq.frame_final_duration #end
    
    # set new frame range 
    context.scene.frame_start = render_start
    context.scene.frame_end = render_end
    # copy list of visible sequences 
    vis_seqs = get_visible_sequences(scene)
    #hide_all sequences but the active 
    set_vis_for_render(seq, scene)
    
    #set video render
    context.scene.render.image_settings.file_format = 'FFMPEG'
    context.scene.render.ffmpeg.format = 'MPEG4'

    # set new name and folder rendering
    #actually filepath, try how split reachts to a simple name
    renderpath = get_video_target_path(context, seq.name)
    print(renderpath)
    bpy.data.scenes["Scene"].render.filepath = renderpath
    # render sequence 
    bpy.ops.render.render(animation=True)

    
    # reset 
    context.scene.frame_start = init_start
    context.scene.frame_end = init_end
    set_sequences_visibility(vis_seqs, scene)

def copy_or_render(context, seq):
    arch_props = context.scene.vse_archiver 

    type = get_sequence_type(context, seq)
    if type == 'IGNORE':
        print(f'Ignored Sequence {seq.name} type {seq.type}')
        return 'IGNORE'
    if type == 'IMGSEQ':
        if arch_props.render_imagesequence:
            return 'RENDER'
        else:
            return 'COPY'
    if type == 'IMAGE':
        if arch_props.render_image:
            return 'RENDER'
        else:
            return 'COPY'
    if type == 'SCENE':
        if arch_props.render_scenestrip:
            return 'RENDER'
        else:
            return 'COPY'
    if type =='SOUND':
        if arch_props.render_audio:
            return 'RENDER'
        else:
            return 'COPY'
    
    
    ###needs levels 
    if type == 'META':
        if arch_props.render_metastrip:
            return 'RENDER'
        else:
            return 'COPY'

    if type == 'MOVIE':
        if arch_props.render_movie: 
            return 'RENDER'
        else:
            return 'COPY'
    
   

def get_sequence_type(context, seq): 
    
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
    else:
        return seq.type
    