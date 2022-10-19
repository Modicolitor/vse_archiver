import bpy
import os
from .bl_archiver_properties import Bl_Archiver_PropGroup

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

all_filepathes = {"filepathes": {}, 
    "imgseq_directories": {},
    "blends_to_check": [], 
    "blends_to_copy": {},
    "main_filepath": "",
    }

@persistent
def load_handler(context: bpy.context):#all_filepathes
    blends_to_check = all_filepathes['blends_to_check']
    #gen_properties(context)
    #print(f'in new file all filepathes {all_filepathes}')
    #blends_to_check = all_filepathes['blends_to_check']
    #blends_to_copy = all_filepathes['blends_to_copy']
    #filepathes = all_filepathes['filepathes']
    #imgseq_directories = all_filepathes['imgseq_directories']
    
    
    
    
    #filepathes = collect_moviclips(context, filepathes)
    #filepathes = collect_sounds(context, filepathes)
    #filepathes, imgseq_directories = collect_images(context, filepathes, imgseq_directories)
    #print(f'In other file {filepathes}')
    print("some result in ")
    res = [665+1]
    
    
    own_filepath = bpy.path.abspath('//') # os.path.abspath(bpy.path.abspath('//'))
    print(f'I"m subs own_filepath {own_filepath}')
    print(f'blends to check in sub {blends_to_check}')
    #if not bpy.context.scene.bl_archiver.is_main_file:
    if own_filepath in blends_to_check:
        bpy.ops.wm.window_close()
    return res # all_filepathes

bpy.app.handlers.load_post.append(load_handler)




def start_archiving(context):
    
    #set controll bool to indentify main file
    context.scene.bl_archiver.is_main_file = True
    
    own_filepath = bpy.path.abspath('//')
    all_filepathes['main_filepath'] = own_filepath
    
    '''all_filepathes = {"filepathes": {}, 
    "imgseq_directories": {},
    "blends_to_check": [], 
    "blends_to_copy": {},
    }'''
    
    blends_to_check = all_filepathes['blends_to_check']
    
    ###find linked objects 
    for lib in bpy.data.libraries:
        if hasattr(lib, 'filepath'):
            if lib.filepath not in blends_to_check:
                blends_to_check.append(lib.filepath)
    print(f'found libaries {blends_to_check}')
    #it should be a while loop until all to check are worked through
    while len(blends_to_check) != 0: 
        get_filepathes_from_blends()


    print(blends_to_check)
    #print(filepathes)
    #print(imgseq_directories)

def gen_properties(context):
    bpy.types.Scene.bl_archiver = bpy.props.PointerProperty(type=Bl_Archiver_PropGroup)

#checks first item of filepath and removes it afterwards
def get_filepathes_from_blends():
    blends_to_check = all_filepathes['blends_to_check']
    blends_to_copy = all_filepathes['blends_to_copy']
    filepathes = all_filepathes['filepathes']
    imgseq_directories = all_filepathes['imgseq_directories']
    
    filepath = blends_to_check[0]

    #filepathes, imgseq_directories = open_new_blend(filepath, filepathes, imgseq_directories)
    print(f'before start{all_filepathes}')
    print(f'I"m mains own_filepath {all_filepathes}')
    
    use_instance = True
    if use_instance:
        import subprocess
        #try:
        #settings["linked_file"] = os.path.abspath(bpy.path.abspath(targetpath))
        print(f'starting sub file {filepath}')
        p = subprocess.Popen([bpy.app.binary_path, os.path.abspath(bpy.path.abspath(filepath)), '-b']) # , all_filepathes
        #
        out, err = p.communicate()
        #print(f'out of subprocess {out}')
        #print(f'error of subprocess {err}')
        '''except:
            print('Error') ### needs better error handling
            #logger.error("Error on the new Blender instance")
            #import traceback
            #logger.error(traceback.print_exc())'''
    #else:
        #bpy.ops.wm.open_mainfile(filepath=filepath)

    ###important for stoping the while loop 
    blends_to_check.remove(filepath)
    return all_filepathes # blends_to_check, filepathes, imgseq_directories