import bpy
#from bpy.types import Scene, Image, Object

class VSE_Archiver_PropGroup(bpy.types.PropertyGroup):
   # CenterObj: bpy.props.PointerProperty(name="Object", type=Object)

    target_folder: bpy.props.StringProperty(
        name="Target Folder", subtype = "DIR_PATH")
    #CutThickness: bpy.props.FloatProperty(
    #    name="Maintcut Thickness", default=0.04, min=0.0)
    
    #LineCount: bpy.props.IntProperty(
    #    name="Linecount", default=1, min=0)
    remove_fade: bpy.props.BoolProperty(
        name="Remove Fade", default=True)

    rebuild: bpy.props.BoolProperty(
        name="Rebuild", default=True)

    target_video_folder: bpy.props.StringProperty(
        name="Video Folder Name", default = 'Video')
    
    target_audio_folder: bpy.props.StringProperty(
        name="Audio Folder Name", default = 'Audio')

    target_imgseq_folder: bpy.props.StringProperty(
        name="Image Sequence Folder Name", default = 'ImgSequences')