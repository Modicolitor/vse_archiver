import bpy
from .vse_arch_functions import get_sequence_type, print_list, get_seq_render_tag
from .vse_arch_functions import  has_equal_sequences, has_equal_metas, check_rendersettings, is_target_equ_source




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
            if arch_props.is_archiv:
                subcol.label(text='You are in the archived blendfile!')
                subcol.operator("varch.rmvarchivetag", text="Allow Archiving",
                                    icon="RESTRICT_RENDER_OFF")
            else:  
                ######not the archive == Main section of ui
                subcol = col.column()
                
                subcol.prop(arch_props, "target_folder")
                subcol.prop(arch_props, "mode")
                subcol.prop(arch_props, "rebuild", text='Rebuild Blend')
                subcol.prop(arch_props, "use_blend_data", text='Include Blend Data')

                if arch_props.mode == '1':
                    #####collect originals
                    
                    subcol.operator("varch.coloriginal", text="Archiv Originals",
                                    icon="COPYDOWN")
                    
                    #####WARNING####
                    #test for target path
                    has_targetpath = False
                    if context.scene.vse_archiver.target_folder != '':
                        has_targetpath = True

                    same_dir = is_target_equ_source(context)
                    
                    if not has_targetpath or same_dir:
                        subcol =  col.box() 
                        subcol.label(text="Warning")
                    
                    if not has_targetpath:
                        #subcol =  col.box() 
                        #subcol.label(text="Warning")
                        subcol.label(text="No Target Folder selected!")
                    
                    if same_dir:
                        subcol.label(text="Target and Blendfile have the same path. Blend will be overwriten.")
                
                if arch_props.mode == '2':
                    subcol.prop(arch_props, "remove_fade", text = 'Full opacity during render')
                    subcol.operator("varch.colsnippets", text="Archiv Snippets",
                                    icon="RESTRICT_RENDER_OFF")
                    
                    
                    
                    
                    
                    
                    box = subcol.box()
                    #box.alignment = 'RIGHT'
                    box.label(text='Settings by Type')
                    '''box.label(text='General Settings')
                    box.prop(arch_props, "render_image")
                    box.prop(arch_props, "render_imagesequence")
                    box.prop(arch_props, "render_scenestrip")
                    box.prop(arch_props, "render_sound")
                    box.prop(arch_props, "render_metastrip")
                    box.prop(arch_props, "render_movie")'''
                    
                    row = box.row(heading='Images')
                    #row1 = row.split(factor=0.6)
                    row.label(text='Images               ')#'    
                    
                    if arch_props.render_image:
                                
                        row.operator("varch.imgoff",
                                    icon="UNPINNED", text="Copy", depress=False)
                        row.operator("varch.imgoff",
                                    icon="PINNED", text="Render", depress=True)
                    else:
                        row.operator("varch.imgoff",
                                    icon="UNPINNED", text="Copy", depress=True)
                        row.operator("varch.imgon",
                                    icon="PINNED", text="Render", depress=False)
                    
                    row = box.row()
                    row.label(text='Imagesequences')
                    if arch_props.render_imagesequence:
                                
                        row.operator("varch.imgseqoff",
                                    icon="UNPINNED", text="Copy", depress=False)
                        row.operator("varch.imgseqon",
                                    icon="PINNED", text="Render", depress=True)
                    else:
                        row.operator("varch.imgseqoff",
                                    icon="UNPINNED", text="Copy", depress=True)
                        row.operator("varch.imgseqon",
                                    icon="PINNED", text="Render", depress=False)
                    
                    row = box.row()
                    row.label(text='Movie                  ')
                    if arch_props.render_movie:
                                
                        row.operator("varch.movieoff",
                                    icon="UNPINNED", text="Copy", depress=False)
                        row.operator("varch.movieon",
                                    icon="PINNED", text="Render", depress=True)
                    else:
                        row.operator("varch.movieoff",
                                    icon="UNPINNED", text="Copy", depress=True)
                        row.operator("varch.movieon",
                                    icon="PINNED", text="Render", depress=False)   
                        
                        
                    row = box.row()
                    row.label(text='Audio                  ')
                    if arch_props.render_sound:
                                
                        row.operator("varch.soundoff",
                                    icon="UNPINNED", text="Copy", depress=False)
                        row.operator("varch.soundon",
                                    icon="PINNED", text="Render", depress=True)
                    else:
                        row.operator("varch.soundoff",
                                    icon="UNPINNED", text="Copy", depress=True)
                        row.operator("varch.soundon",
                                    icon="PINNED", text="Render", depress=False)
                    
                    
                    
                    row = box.row()
                    row.label(text='Metastrips           ')
                    if arch_props.render_metastrip:
                                
                        row.operator("varch.gmetaoff",
                                    icon="UNPINNED", text="Inside", depress=False)
                        row.operator("varch.gmetaon",
                                    icon="PINNED", text="Render", depress=True)
                    else:
                        row.operator("varch.gmetaoff",
                                    icon="UNPINNED", text="Inside", depress=True)
                        row.operator("varch.gmetaon",
                                    icon="PINNED", text="Render", depress=False)
                    
                    
                    row = box.row()
                    row.label(text='Scenes                ')
                    if arch_props.render_scenestrip:
                                
                        row.operator("varch.scnoff",
                                    icon="UNPINNED", text="Ignore", depress=False)
                        row.operator("varch.scnon",
                                    icon="PINNED", text="Render", depress=True)
                    else:
                        row.operator("varch.scnoff",
                                    icon="UNPINNED", text="Ignore", depress=True)
                        row.operator("varch.scnon",
                                    icon="PINNED", text="Render", depress=False)    
                        
                     
                    
                    
                    box = col.box() 
                    box.label(text='Individual Settings')
                   
                    
                    row = box.row()
                    #box = col.box() 
                    active = context.active_sequence_strip
                    if active != None:
                        if active.name in arch_props.metastrips:
                            #subcol.prop(arch_props.metastrips[active.name], "render_inside")
                            if get_seq_render_tag(context.scene, active):
                                    row.operator("varch.meton",
                                                icon="PINNED", text="Use Inside", depress=True)
                                    row.operator("varch.metoff",
                                                icon="UNPINNED", text="Render", depress=False)
                                    
                                    
                            else:
                                row.operator("varch.meton",
                                            icon="PINNED", text="Use Inside", depress=False)
                                row.operator("varch.metoff",
                                            icon="UNPINNED", text="Render", depress=True)
                                
                        
                        if active.name in arch_props.sequences:
                            #if active.name not in arch_props.metastrips:
                                
                            #subcol.prop(arch_props.sequences[active.name], "pls_render", text='Render Sequence')
                            
                            if get_seq_render_tag(context.scene, active):
                                
                                row.operator("varch.seqoff",
                                            icon="UNPINNED", text="Copy", depress=False)
                                row.operator("varch.seqon",
                                            icon="PINNED", text="Render", depress=True)
                            else:
                                row.operator("varch.seqoff",
                                            icon="UNPINNED", text="Copy", depress=True)
                                row.operator("varch.seqon",
                                            icon="PINNED", text="Render", depress=False)
                                
                    subcol =  box.column()
                    ###active data set

                    
                    subcol.operator("varch.updmeta", text="Update Sequence Data", icon="FILE_REFRESH")
                    subcol.operator("varch.resetmeta", text="Reset Sequence Data", icon="TRACKING_CLEAR_BACKWARDS")
                    
                    
                    
                    #####WARNING####
                    is_image, not_ffmpeg, no_audio = check_rendersettings(context)
                    has_equal_seq = has_equal_sequences(context)
                    has_equal_met = has_equal_metas(context)
                    same_dir = is_target_equ_source(context)
                    
                    if is_image or not_ffmpeg or no_audio or not has_equal_seq or not has_equal_met or same_dir:
                        subcol =  col.box() 
                        #subcol.alignment = 'CENTER'
                        subcol.label(text="Warning!!")
                    if context.scene.vse_archiver.target_folder == '': #or context.scene.vse_archiver.target_folder == None
                        subcol.label(text="No Target Folder selected!")
                    if same_dir:
                        subcol.label(text="Target and Blendfile have the same path. Blend will be overwriten.")
                    
                    if not has_equal_seq or not has_equal_met:
                        subcol.label(text="Update Data!")
                    
                    if is_image:
                        subcol.label(text="Imageformat selected for render!")
                        #subcol.prop(arch_props, 'render_imag_output', expand = True )
                    if not_ffmpeg:
                        subcol.label(text="FFMpeg Video is recommended!")
                    if no_audio:
                        subcol.label(text="Audio rendering is disabled!")
                        
                        
                    if is_image:
                        subcol =  col.box()
                        subcol.prop(arch_props, 'render_imag_output')
                    #subcol.operator('varch.tester')

        else:

            subcol.operator("varch.init", text="Initialize",
                            icon="PLUS")
            
            
