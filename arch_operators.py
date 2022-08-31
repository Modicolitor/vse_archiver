import bpy 

from .arch_properties import VSE_Archiver_PropGroup
from .arch_functions import collect_originals

class PP_OT_Initialize_Archiver(bpy.types.Operator):
    '''Archiv Project with the chosen Setting'''

    bl_label = "Add Single Couplings"
    bl_idname = "varch.init"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
       
        return True

    def execute(self, context):
        bpy.types.Scene.vse_archiver = bpy.props.PointerProperty(type=VSE_Archiver_PropGroup)
        
        return{"FINISHED"}

class PP_OT_Archiv_VSE(bpy.types.Operator):
    '''Archiv Project with the chosen Setting'''

    bl_label = "Add Single Couplings"
    bl_idname = "varch.archive"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        target_folder = arch_props
       
        return target_folder != None or target_folder[0] == '/' and target_folder[1] == '/'

    def execute(self, context):
        print('start operator')
        collect_originals(context)
        
        self.report(
                {'WARNING'}, "You are in the new archived blend file, now!!!")
        return{"FINISHED"}