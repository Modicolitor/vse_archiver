import bpy

from .bl_archiver_functions import start_archiving, gen_properties

class BA_OT_Initialize_Bl_Archiver(bpy.types.Operator):
    '''Archiv Project with the chosen Setting'''

    bl_label = "Add Single Couplings"
    bl_idname = "blarch.init"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
       
        return True

    def execute(self, context):
        gen_properties(context)
        #bpy.types.Scene.bl_archiver = bpy.props.PointerProperty(type=Bl_Archiver_PropGroup)
        #bpy.types.Sequences.render_to_archive = bpy.props.BoolProperty(name='RenderThisStrip', default=False)
        return{"FINISHED"}


class BA_OT_Blend_Network(bpy.types.Operator):
    '''Archiv Project with the chosen Setting'''

    bl_label = "Collect All Connected Files"
    bl_idname = "blarch.colfilenetwork"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.bl_archiver
        target_folder = arch_props
       
        return target_folder != None or target_folder[0] == '/' and target_folder[1] == '/'

    def execute(self, context):
        print('start operator')
        start_archiving(context)
        
        self.report(
                {'WARNING'}, "You are in the new archived blend file, now!!!")
        return{"FINISHED"}
