import bpy 
import shutil ###copy files with python
import os 
import ntpath

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
    video_target_path = os.path.join(targetpath, filename)
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

'''def get_subfolder_path(seq, target_folder, n):
    #use filename as subfolder name
    # problem when data from different sources is called the same like the blend standard 001 002.... from different sources 
    # tried to solve problem by adding the sequence order number which is unique per scene (problemes can arise when several scenes with vse use)
    filename = seq.filename #+ str(n)
    return os.path.join(target_folder, filename)'''

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
            if hasattr(seq, "filepath"): #videosequence
                #print(f'this has filepath: {seq.name}')
                if seq.filepath not in filepathes:
                    filepathes[seq.filepath] = get_video_target_path(context, seq.filepath)
                    #filepathes.append(seq.filepath)
            elif hasattr(seq, "sound"): #audio sequence
                if seq.sound.filepath not in filepathes:
                    #filepathes.append(seq.sound.filepath)
                    filepathes[seq.sound.filepath] = get_audio_target_path(context, seq.sound.filepath)
            elif hasattr(seq, "directory"):#image sequence
                directory = seq.directory
                print('directory')
                n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                targetpath = get_imgseq_target_path(context, seq.elements[0].filename,n, directory)
                
                imgseq_directories[directory] = targetpath
                for ele in seq.elements:
                    filepath = os.path.join(directory, ele.filename) ####function naming confusing
                    print(f'Image sequence element {ele.filename} und resulating path {filepath}')
                    if filepath not in filepathes:
                        filepathes[os.path.join(directory, ele.filename)] = os.path.join(imgseq_directories[directory], ele.filename)  ##get_imgseq_target_path(context, ele.filename, n, directory)
                        
                        #filepathes.append(filepath)



    print(filepathes)

    for srcpath in filepathes.items():
        
        targetpath, basename = split_filepath(srcpath[1])
        os.makedirs(targetpath, exist_ok=True)
        copy_file(srcpath[0], targetpath)


    if arch_props.rebuild:
        build_blend_from_original(context, filepathes, imgseq_directories)





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
        for n,seq in enumerate(sequences): 
            print(seq.name)
            if hasattr(seq, "filepath"):
                print(f'has filepath: {seq.name}')
                seq.filepath = get_video_target_path(context, seq.filepath) #get_target_filepath(seq.filepath, arch_props.target_folder)
            elif hasattr(seq, "sound"):
                seq.sound.filepath = get_audio_target_path(context, seq.sound.filepath) #get_target_filepath(seq.sound.filepath, arch_props.target_folder)
            #image sequences 
            elif hasattr(seq, "directory"):
                
                directory = seq.directory
                
                #n, imgseq_directories = get_directorynumber(directory, imgseq_directories)
                seq.directory = imgseq_directories[directory]
                print(f'found img sequence with directory {directory}, and new directory {imgseq_directories}')
                
                '''for ele in seq.elements:
                    filepath = os.path.join(directory, ele.filename) ####function naming confusing
                    print(f'Image sequence element {ele.filename} und resulating path {filepath}')
                    if filepath not in filepathes:
                        filepathes[os.path.join(directory, ele.filename)] = get_imgseq_target_path(context, ele.filename, n, directory)'''
                        #filepathes.append(filepath)
    ###generate node "you are in the new Blend file now"
    #
