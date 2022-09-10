import bpy



class Bl_Archiver_PropGroup(bpy.types.PropertyGroup):
   # CenterObj: bpy.props.PointerProperty(name="Object", type=Object)

    target_folder: bpy.props.StringProperty(
        name="Target Folder", subtype = "DIR_PATH")

    use_blend_data: bpy.props.BoolProperty(
        name="Include Blend Data", default=True)