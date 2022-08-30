import bpy
#from bpy.types import Scene, Image, Object

class VSE_Archiver_PropGroup(bpy.types.PropertyGroup):
   # CenterObj: bpy.props.PointerProperty(name="Object", type=Object)

    new_folder_name: bpy.props.StringProperty(
        name="NewFolder", default="BackUp")
    #CutThickness: bpy.props.FloatProperty(
    #    name="Maintcut Thickness", default=0.04, min=0.0)
    
    #LineCount: bpy.props.IntProperty(
    #    name="Linecount", default=1, min=0)
    remove_fade: bpy.props.BoolProperty(
        name="Remove Fade", default=True)
    