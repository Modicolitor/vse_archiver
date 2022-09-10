import bpy
from .bl_archiver_properties import Bl_Archiver_PropGroup

class BA_OT_Initialize_Bl_Archiver(bpy.types.Operator):
    '''Archiv Project with the chosen Setting'''

    bl_label = "Add Single Couplings"
    bl_idname = "blarch.init"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
       
        return True

    def execute(self, context):
        bpy.types.Scene.bl_archiver = bpy.props.PointerProperty(type=Bl_Archiver_PropGroup)
        #bpy.types.Sequences.render_to_archive = bpy.props.BoolProperty(name='RenderThisStrip', default=False)
        return{"FINISHED"}