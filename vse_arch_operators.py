import bpy 

from .vse_arch_properties import VSE_Archiver_PropGroup
from .vse_arch_functions import collect_originals, collect_snippets, update_metastrips, reset_metastrips, update_sequences_data, reset_sequences_data, get_seqdata_from_seq, get_metadata_from_seq

from .vse_arch_functions import  has_equal_sequences, has_equal_metas, check_rendersettings, reset_seq_by_type


def is_everythingpoll(context):
    has_props= hasattr(context.scene, 'vse_archiver')
    #return False
    #print('test')
    if has_props:
        needsupd = True
        needs_target = True
        if not has_equal_sequences(context) or not has_equal_metas(context):
            needsupd = False
        if context.scene.vse_archiver.target_folder == '': 
            needs_target = False
        is_image, not_ffmpeg, no_audio, no_videocodec = check_rendersettings(context)
        
        if is_image:
            if context.scene.vse_archiver.render_imag_output:
                is_image = False
        
        #print(f'needsupd {needs_target}  needs_target {needs_target}')
        return needsupd and needs_target and not is_image
    return False

    


class PP_OT_Initialize_Archiver(bpy.types.Operator):
    '''Initialize VSE Archiver Addon'''

    bl_label = "Add Single Couplings"
    bl_idname = "varch.init"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        return True

    def execute(self, context):
        bpy.types.Scene.vse_archiver = bpy.props.PointerProperty(type=VSE_Archiver_PropGroup)
        #bpy.types.Sequences.render_to_archive = bpy.props.BoolProperty(name='RenderThisStrip', default=False)
        update_metastrips(context)
        update_sequences_data(context)
        return{"FINISHED"}

class PP_OT_Collect_VSE_Original(bpy.types.Operator):
    '''Archiv Project by copying the source files to the target folder'''

    bl_label = "Add Single Couplings"
    bl_idname = "varch.coloriginal"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        has_props= hasattr(context.scene, 'vse_archiver')
        if has_props:
            if context.scene.vse_archiver.target_folder != '': 
                return True
        return False
    
    def execute(self, context):
        print('start operator')
        collect_originals(context)
        
        self.report(
                {'WARNING'}, "You are in the new archived blend file, now!!!")
        return{"FINISHED"}


class PP_OT_Render_VSE_Snippets(bpy.types.Operator):
    '''Archiv Project by rendering or copying the sequences into the target folder'''

    bl_label = "Add Single Couplings"
    bl_idname = "varch.colsnippets"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        return is_everythingpoll(context)

    def execute(self, context):
        print('start operator')
        collect_snippets(context)
        
        self.report(
                {'INFO'}, "You are in the new archived blend file, now!!!")
        return{"FINISHED"}
    
    
    
class PP_OT_Arch_UpdateMetastrip(bpy.types.Operator):
    '''Update internal sequence list to track the individuel settings'''

    bl_label = "Update Metastrip list"
    bl_idname = "varch.updmeta"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        #arch_props = context.scene.vse_archiver
        #target_folder = arch_props
       
        return True

    def execute(self, context):
        #print('start operator')
        #collect_snippets(context)
        update_metastrips(context)
        update_sequences_data(context)
        #self.report(
        #        {'INFO'}, "You are in the new archived blend file, now!!!")
        return{"FINISHED"}
    

class PP_OT_Arch_ResetMetastrip(bpy.types.Operator):
    '''Reset individual settings to the type settings'''

    bl_label = "Update Metastrip list"
    bl_idname = "varch.resetmeta"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        target_folder = arch_props
       
        return True

    def execute(self, context):
        #print('start operator')
        #collect_snippets(context)
        reset_metastrips(context)
        reset_sequences_data(context)
        #self.report(
        #        {'INFO'}, "You are in the new archived blend file, now!!!")
        return{"FINISHED"}
    

#switch
class PP_OT_Arch_RenderSeq_On(bpy.types.Operator):
    '''Render the active sequence'''

    bl_label = "Switch On Render for Active"
    bl_idname = "varch.seqon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):
        active = context.active_sequence_strip
        
        if active != None:
            seqdata = get_seqdata_from_seq(context, active)
            seqdata.pls_render = True

        return{"FINISHED"}


class PP_OT_Arch_RenderSeq_Off(bpy.types.Operator):
    '''Copy the source of the active sequence'''

    bl_label = "Switch On Render for Active"
    bl_idname = "varch.seqoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        active = context.active_sequence_strip
        
        if active != None:
            seqdata = get_seqdata_from_seq(context, active)
            seqdata.pls_render = False
        
        return{"FINISHED"}



class PP_OT_Arch_RenderMeta_On(bpy.types.Operator):
    '''Render active meta strip'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.meton"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):
        active = context.active_sequence_strip
        
        if active != None:
            seqdata = get_metadata_from_seq(context, active)
            seqdata.render_inside = True

        
        return{"FINISHED"}


class PP_OT_Arch_RenderMeta_Off(bpy.types.Operator):
    '''Handle the insides of the active metastrip. Don't render'''

    bl_label = "Switch Off Render Inside for Active"
    bl_idname = "varch.metoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        active = context.active_sequence_strip
        
        if active != None:
            seqdata = get_metadata_from_seq(context, active)
            seqdata.render_inside= False
        
        
        return{"FINISHED"}
    
    
    
    
    #-------------------------------------------------
    #type switches 
    

class PP_OT_Arch_RenderImage_On(bpy.types.Operator):
    '''Render image strips'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.imgon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):
        
        if hasattr(context.scene, 'vse_archiver'):
            #archiver = context.scene.vse_archiver
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_image = True
            reset_seq_by_type(context, 'IMAGE') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        
        return{"FINISHED"}


class PP_OT_Arch_RenderImage_Off(bpy.types.Operator):
    '''Copy image source files'''

    bl_label = "Switch Off Render Inside for Active"
    bl_idname = "varch.imgoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        
        
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_image = False
            
            reset_seq_by_type(context, 'IMAGE') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        
        return{"FINISHED"}
    
    
    
#-----



class PP_OT_Arch_RenderImgSeq_On(bpy.types.Operator):
    '''Render image sequence strips'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.imgseqon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):

        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_imagesequence = True
            
        
            reset_seq_by_type(context, 'IMGSEQ') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        return{"FINISHED"}


class PP_OT_Arch_RenderImgSeq_Off(bpy.types.Operator):
    '''Copy image sequence strips source files'''

    bl_label = "Switch Off Render Inside for Active"
    bl_idname = "varch.imgseqoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_imagesequence = False
            reset_seq_by_type(context, 'IMGSEQ') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        
        return{"FINISHED"}
    
    
#------------------

class PP_OT_Arch_RenderScene_On(bpy.types.Operator):
    '''Render scene strips'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.scnon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):

        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_scenestrip = True
            
            reset_seq_by_type(context, 'SCENE') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        
        return{"FINISHED"}


class PP_OT_Arch_RenderScene_Off(bpy.types.Operator):
    '''Ignore Scene Strips. Sources might get copied via blend data!?'''

    bl_label = "Ignore Scene Strip"
    bl_idname = "varch.scnoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_scenestrip = False
            reset_seq_by_type(context, 'SCENE') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        return{"FINISHED"}
    
    
#------------------

class PP_OT_Arch_RenderSound_On(bpy.types.Operator):
    '''Render audio strips (as videofiles :-( )'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.soundon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        return True

    def execute(self, context):

        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_sound = True
            
        
            reset_seq_by_type(context, 'SOUND') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        return{"FINISHED"}


class PP_OT_Arch_RenderSound_Off(bpy.types.Operator):
    '''Copy source files of the Audio'''

    bl_label = "Switch Off Render Inside for Active"
    bl_idname = "varch.soundoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        return True

    def execute(self, context):
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_sound = False
            reset_seq_by_type(context, 'SOUND') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        return{"FINISHED"}
    
    
#------------------

class PP_OT_Arch_RenderGMeta_On(bpy.types.Operator):
    '''Render meta strips'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.gmetaon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):

        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_metastrip = True
            
            reset_seq_by_type(context, 'META') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        
        return{"FINISHED"}


class PP_OT_Arch_RenderGMeta_Off(bpy.types.Operator):
    '''Handle the insides of Metastrips. Don't render'''

    bl_label = "Switch Off Render Inside for Active"
    bl_idname = "varch.gmetaoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):

        return True

    def execute(self, context):
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_metastrip = False
            reset_seq_by_type(context, 'META') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
            
        
        
        return{"FINISHED"}
    
    
#------------------

class PP_OT_Arch_RenderMovie_On(bpy.types.Operator):
    '''Render movie strips'''

    bl_label = "Switch On Render Inside for Active"
    bl_idname = "varch.movieon"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        arch_props = context.scene.vse_archiver
        return True

    def execute(self, context):

        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_movie = True
            
            reset_seq_by_type(context, 'MOVIE') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
        
        return{"FINISHED"}


class PP_OT_Arch_RenderMovie_Off(bpy.types.Operator):
    '''Copy source files of movie strips'''

    bl_label = "Switch Off Render Inside for Active"
    bl_idname = "varch.movieoff"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.render_movie = False
            
            reset_seq_by_type(context, 'MOVIE') #['MOVIE', 'SOUND', 'IMAGE', 'IMGSEQ', 'SCENE']
            
        
        
        return{"FINISHED"}

class PP_OT_Arch_RemoveArchivetag(bpy.types.Operator):
    '''Get Archiver Options Back'''

    bl_label = "Allow Archiving"
    bl_idname = "varch.rmvarchivetag"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        
        arch_props = context.scene.vse_archiver
      
        return True

    def execute(self, context):
        if hasattr(context.scene, 'vse_archiver'):
            for sc in bpy.data.scenes:
                archiver = sc.vse_archiver
                archiver.is_archiv = False
        return{"FINISHED"}



class PP_OT_Arch_TestButton(bpy.types.Operator):
    '''Test Button'''

    bl_label = "Test"
    bl_idname = "varch.tester"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):

        return True

    def execute(self, context):
        from .vse_arch_functions import write_texteditor
        write_texteditor(context,['hallo', 'world', 'error copying files'])

        return{"FINISHED"}