import bpy 
import shutil ###copy files with python


#
def copy_file(src, dst):
    shutil.copy2(src, dst)



def collect_originals(context):
    arch_props = context.scene.vse_archiver
    sequences = context.sequences
    # collect filepath of linked vse elements and sort out doubles 
    print("i'm in")
    filepathes = []
    for seq in sequences: 
        print(seq.name)
        if hasattr(seq, "filepath"):
            print(f'this has filepath: {seq.name}')
            if seq.filepath not in filepathes:
                filepathes.append(seq.filepath)


    print(filepathes)

    for srcpath in filepathes:
        copy_file(srcpath, arch_props.target_folder)



def build_blend_from_original(context):
    arch_props = context.scene.vse_archiver
    #save as new blend in the folder 
    from pathlib import Path
    
    
    dirname = '/home/reports'
    filename = 'daily'
    suffix = '.pdf'
    Path(dirname, filename).with_suffix(suffix)
    os.path.join(arch_props.target_folder, base_filename + '.' + filename_suffix)
    filepath =  
    bpy.ops.wm.save_as_mainfile(filepath=filepath) 


    sequences = context.sequences
    #pro sequence, strip filename from path, add filename to target folder path and replace filepath in sequence
    for seq in sequences: 
        if hasattr(seq, "filepath"):
            print(f'this has filepath: {seq.name}')



    #
