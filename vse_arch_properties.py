import bpy
#from bpy.types import Scene, Image, Object
class VSE_Archiver_MetaStrip(bpy.types.PropertyGroup):
    name:bpy.props.StringProperty(
        name="Video Folder Name", default = 'Video')
    render_inside:bpy.props.BoolProperty(
        name="Render Inside", default=False)

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
        name="Rebuild", default=True, description = 'Saves the blend file in the Archive and remaps all links in sequences and external data.')

    use_blend_data: bpy.props.BoolProperty(
        name="Include Blend Data", default=True)

    target_video_folder: bpy.props.StringProperty(
        name="Video Folder Name", default = 'Video')
    
    target_audio_folder: bpy.props.StringProperty(
        name="Audio Folder Name", default = 'Audio')
    
    target_image_folder: bpy.props.StringProperty(
        name="Single Image Folder Name", default = 'SingleImg')

    target_imgseq_folder: bpy.props.StringProperty(
        name="Image Sequence Folder Name", default = 'ImgSequences')
    
    target_font_folder: bpy.props.StringProperty(
        name="Fonts Folder Name", default = 'Fonts')
    
    target_snippet_folder: bpy.props.StringProperty(
        name="Snippets Folder Name", default = 'Snippets')

    mode: bpy.props.EnumProperty(
        name='',  # SingleCoupltypes
        description='List of forms avaiable in single connector mode',
        default='2',
        items=[('1', 'Collect Original', ''),
               ('2', 'Collect Snippets', ''),
               ('3', 'Collect Blend Elements', ''),
               ]
    )

    render_imagesequence: bpy.props.BoolProperty(
        name="Render Image Sequence", default=True, description='When checked Imagesequences will be rendered out, rather than copied')

    render_image: bpy.props.BoolProperty(
        name="Render Image", default=False, description='When checked single images will be rendered out, rather than copied')

    render_scenestrip: bpy.props.BoolProperty(
        name="Render Scene Strip", default=True, description='When checked Scenestrip will be rendered out and the result will replace this strip, rather than copied and remaped')

    render_audio: bpy.props.BoolProperty(
        name="Render Audio Strip", default=True, description='When checked Scenestrip will be rendered out and the result will replace this strip, rather than copied and remaped')

    render_metastrip: bpy.props.BoolProperty(
        name="Render Meta Strip", default=True, description='When checked each Metastrip is handled will be rendered out and the result will replace this strip, rather than copied and remaped')
    
    render_movie: bpy.props.BoolProperty(
        name="Render Movie", default=True, description='When checked each Movie is handled will be rendered out and the result will replace this strip, rather than copied and remaped')


    #meta_strip_depth: bpy.props.IntProperty(
    #    name="Meta Strip Depth", default=0, min=0)
    
    metastrips:bpy.props.CollectionProperty(type=VSE_Archiver_MetaStrip)