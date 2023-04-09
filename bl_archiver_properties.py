import bpy



class Bl_Archiver_PropGroup(bpy.types.PropertyGroup):
   # CenterObj: bpy.props.PointerProperty(name="Object", type=Object)

    target_folder: bpy.props.StringProperty(
        name="Target Folder", subtype = "DIR_PATH")

    use_blend_data: bpy.props.BoolProperty(
        name="Include Blend Data", default=True)
    
    is_main_file: bpy.props.BoolProperty(
        name="Is Main File", default=False, description="used to close the right files and not the main")
    
    json_filepath:bpy.props.StringProperty(
        name="Json Path", subtype = "DIR_PATH")
    
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