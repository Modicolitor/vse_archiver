import bpy

from .vse_arch_functions import collect_moviclips, collect_sounds,collect_images
'''
def open_new_blend(filepath):
    use_instance = True 
    if use_instance:
        import subprocess
        try:
            subprocess.Popen([bpy.app.binary_path, filepath, ])
        except:
            print('Error') ### needs better error handling
            #logger.error("Error on the new Blender instance")
            #import traceback
            #logger.error(traceback.print_exc())
    else:
        bpy.ops.wm.open_mainfile(filepath=filepath)
'''

    
from bpy.app.handlers import persistent

'''filepathes = {}
imgseq_directories = {}
blends_to_check = {}'''

@persistent
def load_handler(context: bpy.context, all_filepathes):
    print(f'in new file all filepathes {all_filepathes}')
    blends_to_check = all_filepathes['blends_to_check']
    blends_to_copy = all_filepathes['blends_to_copy']
    filepathes = all_filepathes['filepathes']
    imgseq_directories = all_filepathes['imgseq_directories']
    
    
    
    
    filepathes = collect_moviclips(context, filepathes)
    filepathes = collect_sounds(context, filepathes)
    filepathes, imgseq_directories = collect_images(context, filepathes, imgseq_directories)
    print(f'In other file {filepathes}')
   
    return all_filepathes

bpy.app.handlers.load_post.append(load_handler)




def start_archiving(context):
    all_filepathes = {"filepathes": {}, 
    "imgseq_directories": {},
    "blends_to_check": [], 
    "blends_to_copy": {},
    }
    
    blends_to_check = all_filepathes['blends_to_check']
    
    ###find linked objects 
    for lib in bpy.data.libraries:
        if hasattr(lib, 'filepath'):
            if lib.filepath not in blends_to_check:
                blends_to_check.append(lib.filepath)

    #it should be a while loop until all to check are worked through
    while len(blends_to_check) != 0: 
        all_filepathes = get_filepathes_from_blends(all_filepathes)


    print(blends_to_check)
    #print(filepathes)
    #print(imgseq_directories)


#checks first item of filepath and removes it afterwards
def get_filepathes_from_blends(all_filepathes):
    blends_to_check = all_filepathes['blends_to_check']
    blends_to_copy = all_filepathes['blends_to_copy']
    filepathes = all_filepathes['filepathes']
    imgseq_directories = all_filepathes['imgseq_directories']
    
    filepath = blends_to_check[0]

    #filepathes, imgseq_directories = open_new_blend(filepath, filepathes, imgseq_directories)
    print(f'before start{all_filepathes}')
    use_instance = True
    if use_instance:
        import subprocess
        try:
            subprocess.Popen(bpy.app.binary_path, filepath, all_filepathes)
        except:
            print('Error') ### needs better error handling
            #logger.error("Error on the new Blender instance")
            #import traceback
            #logger.error(traceback.print_exc())
    else:
        bpy.ops.wm.open_mainfile(filepath=filepath)

    ###important for stoping the while loop 
    blends_to_check.remove(filepath)
    return blends_to_check, filepathes, imgseq_directories