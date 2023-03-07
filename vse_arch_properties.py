import bpy
#from bpy.types import Scene, Image, Object

class VSE_Archiver_SequenceStrip(bpy.types.PropertyGroup):
    name:bpy.props.StringProperty(
        name="Video Folder Name", default = 'Video')
    type:bpy.props.StringProperty(
        name="seqType", default = '')
    pls_render:bpy.props.BoolProperty(
        name="Render Sequence", default=False)
    
class VSE_Archiver_MetaStrip(bpy.types.PropertyGroup):
    name:bpy.props.StringProperty(
        name="Meta Name", default = 'Meta')
    type:bpy.props.StringProperty(
        name="seqType", default = 'META')
    render_inside:bpy.props.BoolProperty(
        name="Render Inside", default=False)
    
class VSE_Archiver_Keys(bpy.types.PropertyGroup):
    seq_name:bpy.props.StringProperty(
        name="name", default = 'name')
    data_path: bpy.props.StringProperty(
        name="Datapath", default = 'blend_alpha')
    frame:bpy.props.FloatProperty(
        default = 1)
    value:bpy.props.FloatProperty(
        default = 1)
    interpolation:bpy.props.StringProperty(
        name="Datapath", default = 'inter')
    handle_right_type:bpy.props.StringProperty(
        name="htype", default = 'type')
    handle_left_type:bpy.props.StringProperty(
        name="htype", default = 'typeleft')
    attr:bpy.props.StringProperty(
        name="finalelement", default = 'blend_alpha')
    
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
        name="Rebuild", default=True, description = 'Saves the blend file in the Archive Folder and remaps all sequences and Blend data.')
    is_archiv: bpy.props.BoolProperty(
        name="New Archive", default=False, description = 'Set True when when file is the result of Archiving')

    use_blend_data: bpy.props.BoolProperty(
        name="Include Blend Data", default=True, description='Archiv Images, Imagesequences, Movies, Sounds and Fonts present in the blend data.')

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
        name='',  
        description='List of forms avaiable in single connector mode',
        default='1',
        items=[('1', 'Collect Sources', ''),
               ('2', 'Collect Snippets', ''),
               #('3', 'Collect Blend Elements', ''),
               ]
    )
    render_imag_output: bpy.props.BoolProperty(
        name="Render as images anyway", default=False, description='Overwrite blocking of rendering into image sequences (see renderoutput)')
    
    #sequences:bpy.props.CollectionProperty(type=VSE_Archiver_SequenceStrip)

    render_imagesequence: bpy.props.BoolProperty(
        name="Render Image Sequence", default=True, description='When checked Imagesequences will be rendered out, rather than copied')

    render_image: bpy.props.BoolProperty(
        name="Render Image", default=False, description='When checked single images will be rendered out, rather than copied')

    render_scenestrip: bpy.props.BoolProperty(
        name="Render Scene Strip", default=True, description='When checked Scenestrip will be rendered out and the result will replace this strip, rather than copied and remaped')

    render_sound: bpy.props.BoolProperty(
        name="Render Audio Strip", default=True, description='When checked Scenestrip will be rendered out and the result will replace this strip, rather than copied and remaped')

    render_metastrip: bpy.props.BoolProperty(
        name="Render Meta Strip", default=True, description='When checked each Metastrip is handled will be rendered out and the result will replace this strip, rather than copied and remaped')
    
    render_movie: bpy.props.BoolProperty(
        name="Render Movie", default=True, description='When checked each Movie is handled will be rendered out and the result will replace this strip, rather than copied and remaped')


   
    metastrips: bpy.props.CollectionProperty(type=VSE_Archiver_MetaStrip)
    #sequences:bpy.props.CollectionProperty(type=VSE_Archiver_MetaStrip)
    
    sequences:  bpy.props.CollectionProperty(type=VSE_Archiver_SequenceStrip)
    
    keys:  bpy.props.CollectionProperty(type=VSE_Archiver_Keys)