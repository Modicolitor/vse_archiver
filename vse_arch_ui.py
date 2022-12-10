import bpy
from .vse_arch_functions import get_sequence_type, print_list



def has_equal_metas(context):
    ####man muss es von data ziehen und durch alle scene  schauen
    
    #sequences = context.scene.sequence_editor.sequences_all
    
    arch_count = 0
    c = 0
    for sc in bpy.data.scenes:
        for seq in sc.sequence_editor.sequences_all:
            if seq.type == 'META':
                c += 1 
    for sc in bpy.data.scenes:
        arch_metastrips = sc.vse_archiver.metastrips
        arch_count += len(arch_metastrips)
        
    #print(f'sequence count is {c} and archiver metacount {arch_count}')
    return c == arch_count
       
def has_equal_sequences(context):
    ####man muss es von data ziehen und durch alle scene  schauen
    
    #sequences = context.scene.sequence_editor.sequences_all
    
    arch_count = 0
    c = 0
    for sc in bpy.data.scenes:
        for s in sc.sequence_editor.sequences_all:
            type = get_sequence_type(context, s)
            if type in ['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ']:
                c += 1
            
                
    for sc in bpy.data.scenes:
        arch_sequences = sc.vse_archiver.sequences
        arch_count += len(arch_sequences)
        
    print(f'sequence count is {c} and archiver metacount {arch_count}')
    print_list(sc.vse_archiver.sequences)
    
    return c == arch_count

class PP_PT_VSEArchiver_Menu(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Archiver Modes"
    bl_category = "VSE Archiver"

    def draw(self, context):
        data = bpy.data
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        flow = layout.grid_flow(row_major=True, columns=0,
                                even_columns=False, even_rows=False, align=True)
        col = flow.column()
        row = layout.row()

        subcol = col.column()

        if hasattr(context.scene, "vse_archiver"):  # "PuzzleUrPrint" in data.collections and
            arch_props = context.scene.vse_archiver
            subcol = col.column()

            subcol.prop(arch_props, "mode")
            subcol.prop(arch_props, "target_folder")
            subcol.prop(arch_props, "rebuild", text='Rebuild Blend')

            if arch_props.mode == '1':
                
                subcol.operator("varch.coloriginal", text="Archiv Originals",
                                icon="COPYDOWN")
            
            if arch_props.mode == '2':
                subcol.prop(arch_props, "remove_fade")
                subcol.operator("varch.colsnippets", text="Archiv Snippets",
                                icon="RESTRICT_RENDER_OFF")
                
                
                
                if not has_equal_sequences(context) or not has_equal_metas(context):
                    subcol.label(text="Update Data!")
                
                
                subcol.operator("varch.updmeta", text="Update Sequence Data", icon="FILE_REFRESH")
                subcol.operator("varch.resetmeta", text="Reset Sequence Data", icon="TRACKING_CLEAR_BACKWARDS")
                
                ###active data set
                active = context.active_sequence_strip
                if active != None:
                    if active.name in arch_props.metastrips:
                        subcol.prop(arch_props.metastrips[active.name], "render_inside")
                    if active.name in arch_props.sequences:
                        if active.name not in arch_props.metastrips:
                            subcol.prop(arch_props.sequences[active.name], "pls_render", text='Render Sequence')
                    
                
                box = col.box()
                box.prop(arch_props, "render_image")
                box.prop(arch_props, "render_imagesequence")
                box.prop(arch_props, "render_scenestrip")
                box.prop(arch_props, "render_sound")
                box.prop(arch_props, "render_metastrip")
                box.prop(arch_props, "render_movie")


        else:

            subcol.operator("varch.init", text="Initialize",
                            icon="PLUS")
            
            
