import bpy


class VSE_Archiver_PropGroup(bpy.types.PropertyGroup):
   # CenterObj: bpy.props.PointerProperty(name="Object", type=Object)

    target_folder: bpy.props.StringProperty(
        name="Target Folder", subtype = "DIR_PATH")