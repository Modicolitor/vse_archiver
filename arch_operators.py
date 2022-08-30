import bpy 

from .arch_properties import VSE_Archiver_PropGroup


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
        
       
        return True

    def execute(self, context):
        
        return{"FINISHED"}