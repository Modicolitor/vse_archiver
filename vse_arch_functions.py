import bpy 
import shutil ###copy files with python
import os 
import ntpath
import copy
from .vse_arch_definitions import is_audio, is_video

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

'''def has_vid_connected_audio(context, filepath):
    
    sequences = context.scene.sequence_editor.sequences_all
    for seq in sequences:
        typ =  get_sequence_type(context, seq)
        if typ == 'MOVIE':
            if seq.filepath == filepath:
                print('******* found Audio with filepath {filepath} to originate from a video')
                return True
    print('*******NOT found Audio with filepath {filepath} to originate from a video')
    return False'''

def get_audio_target_path(context, filepath):
    
    
    arch_props = context.scene.vse_archiver
    targetfolder = arch_props.target_folder
    if is_audio(filepath):
        folder = arch_props.target_audio_folder
    else:
        folder = arch_props.target_video_folder
    
    path, basename = split_filepath(filepath)

    #'target_folder'\videofolder\basename 
    targetpath = os.path.join(targetfolder, folder)
    video_target_path = os.path.join(targetpath, basename)
    return video_target_path

def get_font_target_path(context, filepath):
    arch_props = context.scene.vse_archiver
    targetfolder = arch_props.target_folder
    fontfolder = arch_props.target_font_folder
    path, basename = split_filepath(filepath)

    #'target_folder'\videofolder\basename 
    targetpath = os.path.join(targetfolder, fontfolder)
    font_target_path = os.path.join(targetpath, basename)
    return font_target_path

def get_image_target_path(context, filepath, directory):
    arch_props = context.scene.vse_archiver
    targetfolder = arch_props.target_folder
    videofolder = arch_props.target_image_folder
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

    
    
    #'target_folder'maintarget\imgseqfolder\
    targetpath = os.path.join(targetfolder, imgseqfolder)
    #print(f'in get target parth {filename}')
    if directory in imgseqfolder:
        #already got that folder
        imgseq_targetpath = imgseqfolder[directory]
    else:   
        #old filename, extension = os.path.splitext(filename)
        #old subfoldername = get_none_numbername(filename) + str(n)
        ''
        ignore, subfoldername = os.path.split(directory[:-1])
        #print(f'subfolder name is {subfoldername}')
        subfoldername =subfoldername + str(n)
        targetpath = os.path.join(targetpath, subfoldername)
        imgseq_targetpath = targetpath 
    return imgseq_targetpath

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
            filepathes[seq.sound.filepath] = get_audio_target_path(context, seq.sound.filepath)
    #elif type == 'IMAGE':
    #    print(f'Found IMAGE {seq.name}----------------------------------------------------------------------------------')
    #    directory = seq.directory
    #    filename = seq.elements[0].filename
    #    filepath = os.path.join(directory, filename)
    #    if filepath not in filepathes:
    #        n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
    #        targetpath = get_imgseq_target_path(context, seq.elements[0].filename, directory) 
    #        filepathes[filepath] = targetpath
    elif type == 'IMGSEQ' or type == 'IMAGE': #  hasattr(seq, "directory"):#image sequence
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
    
    ###make pathes absolut
    bpy.ops.file.make_paths_absolute()

    
    ###src target in dictionary
    filepathes = {}
    imgseq_directories = {}
    for scene in bpy.data.scenes:
        sequences = scene.sequence_editor.sequences_all
        # collect filepath of linked vse elements and sort out doubles 
        for seq in sequences: 
            #print(seq.name)
            filepathes, imgseq_directories = sequence_to_copy(context, seq, filepathes, imgseq_directories)

    # check non-vse part for elements to copy 
    if arch_props.use_blend_data:
        filepathes = collect_sounds(context, filepathes) ###sounds before movie important (and hacky); sounds look for movie seq with same filepath
        filepathes = collect_moviclips(context, filepathes)
        filepathes = collect_fonts(context, filepathes)
        filepathes, imgseq_directories = collect_images(context, filepathes, imgseq_directories)

    print(filepathes)

    for srcpath in filepathes.items():
        
        targetpath, basename = split_filepath(srcpath[1])
        os.makedirs(targetpath, exist_ok=True)
        copy_file(srcpath[0], targetpath)


    if arch_props.rebuild:
        build_blend_from_original(context, filepathes, imgseq_directories)
        bpy.ops.file.make_paths_relative()



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

def collect_fonts(context, filepathes):
    data = bpy.data 
    for font in data.fonts:
        if font.filepath  not in filepathes:
            filepathes[font.filepath] = get_font_target_path(context, font.filepath)
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




def build_blend_from_original(context, filepathes, imgseq_directories):
    arch_props = context.scene.vse_archiver
    #save as new blend in the folder 
    save_blend_file(context)

    sequences = context.scene.sequence_editor.sequences_all
    #pro sequence, strip filename from path, add filename to target folder path and replace filepath in sequence
    
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
                print(f'exchange audio reached seq {seq.sound.filepath} got from get_audio_target_path {get_audio_target_path(context, seq.sound.filepath)} ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            #elif type == 'IMAGE':
            #    filepath = get_image_target_path(context, seq.elements[0].filename, seq.directory) 
            #    directory, filename = os.path.split(filepath) 
            #    seq.directory = directory
                #seq.elements[0].filename = filename gar nicht nötig weil der name bleibt
                
            #image sequences
                                
            elif hasattr(seq, "directory"):####is image, not nice
                directory = seq.directory
                print(f'image sequence directories are {imgseq_directories}')
                #n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                seq.directory = imgseq_directories[directory] # get_imgseq_target_path(context, seq.elements[0].filename, get_directorynumber(seq.directory, imgseq_directories), seq.directory)

    if arch_props.use_blend_data:
        remap_moviclips(context, filepathes)
        remap_sounds(context, filepathes)
        remap_images(context, filepathes)
        remap_fonts(context, filepathes)

##### snippets 
###main function to started by collect snippets operator 
def collect_snippets(context): 
    #  gehe durch sequences
    for scene in bpy.data.scenes:
        if hasattr(scene, 'vse_archiver'):
            context.window.scene = scene
            filepathes ={}
            imgseq_directories = {}
            sequences = get_visible_sequences(scene)#  scene.sequence_editor.sequences_all)
            print(f'scene {scene.name} sequences found {sequences}')
            
            filepathes, imgseq_directories = copy_render_decider(context, scene, filepathes, imgseq_directories, sequences)
                
                
            if context.scene.vse_archiver.rebuild:
                build_blend_from_original(context, filepathes, imgseq_directories)
                #save_blend_file(context)
                
def copy_render_decider(context, scene, filepathes, imgseq_directories, sequences):
    for seq in sequences:
        answer = copy_or_render(context, scene, seq)
        print(f'for seq {seq.name} got answer {answer}')
        if answer == 'COPY':
            filepathes, imgseq_directories = sequence_to_copy(context, seq, filepathes, imgseq_directories)
        elif answer == 'RENDER':
            render_sequence(context, seq, scene, False)
        elif answer == 'META':
            filepathes, imgseq_directories = render_meta_snipets(context, scene, seq)
        elif answer == 'IGNORE':
            print(f'ignored sequence {seq.name}')
        else:
            print(f'weird answer {answer}')
            
        return filepathes, imgseq_directories
                
            

    # entscheide render or collect
    # wenn render send to render part 
        
    # wenn collect send to collect system 
    
def get_visible_sequences(scene):
    vis = []
    for seq in scene.sequence_editor.sequences: #_all
        if not seq.mute:
            vis.append(seq)
    return vis

def set_sequences_visibility(vis_seq, scene):
    for seqvis in vis_seq:
        print(f'visible sequences after render are {vis_seq}')
        for seq in scene.sequence_editor.sequences_all:
            if seq == seqvis:
                seq.mute = False

def set_vis_for_render(seqs, scene):
    for sequ in scene.sequence_editor.sequences_all:
        sequ.mute = True
    for seq in seqs:    
        seq.mute = False
    print('necessary seq muted')
    #print(brak)
    
def render_sequence(context, seq, scene, is_meta):
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
    vis_seqs = get_visible_sequences(scene)
    
    
    #hide_all sequences but the active 
    if not is_meta:
        set_vis_for_render([seq], scene)
    
    #set video render (seems to need the setting in the active scene and not the processed scene)
    scene.render.image_settings.file_format = 'FFMPEG'
    context.scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    context.scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.audio_codec = 'AAC'
    context.scene.render.ffmpeg.audio_codec = 'AAC'

    
    # set new name and folder rendering
    #actually filepath, try how split reachts to a simple name
    renderpath = get_video_target_path(context, seq.name) 
    renderpath = renderpath + '.mp4'
    print(renderpath)
    scene.render.filepath = renderpath
    context.scene.render.filepath = renderpath
    
    #if seq.type == "META":
    #    print(bb)
    # render sequence 
    bpy.ops.render.render(animation=True)

    
    # reset 
    scene.frame_start = init_start
    scene.frame_end = init_end
    if not is_meta:
        set_sequences_visibility(vis_seqs, scene)
    
    if arch_props.rebuild:
        replace_sequence_w_rendered(scene, seq, renderpath)
        
def replace_sequence_w_rendered(scene, seq, newfilepath):
    ##new sequence 
    scene.sequence_editor.sequences.new_movie(seq.name+'replaced', newfilepath, channel = seq.channel, frame_start = seq.frame_final_start)
    for seq_cont in scene.sequence_editor.sequences:
        if seq == seq_cont:
            scene.sequence_editor.sequences.remove(seq)
   
   

def copy_or_render(context, scene, seq):
    arch_props = scene.vse_archiver 

    type = get_sequence_type(context, seq)
    if type == 'IGNORE':
        print(f'Ignored Sequence {seq.name} type {seq.type}')
        return 'IGNORE'

    
    if type == 'IMAGE':
        print(f'found image {seq.name} render_image {arch_props.render_image}')
        if arch_props.render_image:
            return 'RENDER'
        else:
            return 'COPY'
    
    if type == 'IMGSEQ':
        print(f'found Imgseq {seq.name} render_imageseq {arch_props.render_imagesequence}')
        if arch_props.render_imagesequence:
            return 'RENDER'
        else:
            return 'COPY'        

    if type == 'SCENE':
        print(f'found scene {seq.name} render_scenestrip {arch_props.render_scenestrip}')
        if arch_props.render_scenestrip:
            return 'RENDER'
        else:
            return 'COPY'
    if type =='SOUND':
        if arch_props.render_audio:
            return 'RENDER'
        else:
            return 'COPY'
    
    
    
    if type == 'META':
        return 'META'

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
    
    
    
def render_meta_snipets(context, scene, seq, filepathes, imgseq_directories):
    
    #get metastrip elements 
    elements = seq.sequences
    
    vis_seqs = get_visible_sequences(scene)
    #set visibility for elements (careful will be set in render_sequences again)
    set_vis_for_render (elements, scene)
    
    # should the elements be rendered individually? 
    if is_render_elements(seq):
        filepathes, imgseq_directories = copy_render_decider(context, scene, filepathes, imgseq_directories, sequences) 
    #   yes: send individual elements to be rendered render_sequence(context, seq, scene, is_meta) 
    #   NO: send this meta strip to render_sequence(context, seq, scene, is_meta)
    else: 
        render_sequence(context, seq, scene, True)
        
    set_sequences_visibility(vis_seqs,scene)
    return filepathes, imgseq_directories


def is_render_elements(context, scene, seq): 
    arch_metastrips = scene.vse_archiver.metastrips
    for ele in arch_metastrips:
            if ele.name == seq.name:
                return ele.render_inside


def reset_metastrips(context):
    for sc in bpy.data.scenes:
        #sequences = sc.sequence_editor.sequences_all
        arch_metastrips = sc.vse_archiver.metastrips
        
        for n,ele in enumerate(arch_metastrips):
            arch_metastrips.remove(n)
    update_metastrips(context)

####adds metastrips that are not present yet in the list ; renaming strips,  after making   
def update_metastrips(context):
    print('in updates ')
    
    ######################PROBLEM In verschiedenen Scenen können Strips den gleich namen haben, nur nicht innerhalb der scene, aber es ist ja eh per scene gespeichert 
    for sc in bpy.data.scenes:
        sequences = sc.sequence_editor.sequences_all
        arch_metastrips = sc.vse_archiver.metastrips
        
        for seq in sequences:
            print(f'seq {seq.name} ')
            if seq.type == 'META':
                if seq.name not in arch_metastrips:
                    print(f'ele {seq.name} ')
                    ele = arch_metastrips.add()
                    ele.name = seq.name 
    
        ####looks for old metastrip data with no counter part in the current state  
        for ele in arch_metastrips:
            if ele.name not in sequences:
                arch_metastrips.remove(ele.name)
               