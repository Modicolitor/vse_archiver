
#
# Copyright (C) 2020 by Modicolitor
#
# This file is part of PuzzleUrPrint.
#
# License Text
#
# You should have received a copy of the GNU General Public License along with PuzzleUrPrint. If
# not, see <https://www.gnu.org/licenses/>.


import bpy


bl_info = {  # für export als addon
    "name": "VSE Archiver",
    "author": "Modicolitor",
    "version": (3, 50),
    "blender": (3, 5, 0),
    "location": "Sequence Editor > Tools",
    "description": "Collects all Footage used in a VSE Video project to a Folder.",
    "doc_url": "http://vse-archiver.modicolitor.com/Dokumentation.html", ####################
    "category": "Tool"}

# modules = addon_auto_imports.setup_addon_modules(
#    __path__, __name__, ignore_packages=[], ignore_modules=[]
# )


from .vse_arch_operators import PP_OT_Collect_VSE_Original 
from .vse_arch_operators import PP_OT_Render_VSE_Snippets
from .vse_arch_operators import PP_OT_Initialize_Archiver
from .vse_arch_operators import PP_OT_Arch_ResetMetastrip, PP_OT_Arch_UpdateMetastrip
from .vse_arch_operators import PP_OT_Arch_RenderSeq_On
from .vse_arch_operators import PP_OT_Arch_RenderSeq_Off
from .vse_arch_operators import PP_OT_Arch_RenderMeta_On
from .vse_arch_operators import PP_OT_Arch_RenderMeta_Off
from .vse_arch_operators import PP_OT_Arch_RenderMovie_On
from .vse_arch_operators import PP_OT_Arch_RenderMovie_Off
from .vse_arch_operators import PP_OT_Arch_RenderGMeta_On
from .vse_arch_operators import PP_OT_Arch_RenderGMeta_Off
from .vse_arch_operators import PP_OT_Arch_RenderSound_On
from .vse_arch_operators import PP_OT_Arch_RenderSound_Off
from .vse_arch_operators import PP_OT_Arch_RenderScene_On
from .vse_arch_operators import PP_OT_Arch_RenderScene_Off
from .vse_arch_operators import PP_OT_Arch_RenderImgSeq_On
from .vse_arch_operators import PP_OT_Arch_RenderImgSeq_Off
from .vse_arch_operators import PP_OT_Arch_RenderImage_On
from .vse_arch_operators import PP_OT_Arch_RenderImage_Off
from .vse_arch_operators import PP_OT_Arch_RemoveArchivetag
from .vse_arch_operators import PP_OT_Arch_TestButton

from .vse_arch_ui import PP_PT_VSEArchiver_Menu
from .vse_arch_properties import VSE_Archiver_MetaStrip
from .vse_arch_properties import VSE_Archiver_SequenceStrip
from .vse_arch_properties import VSE_Archiver_Keys
from .vse_arch_properties import VSE_Archiver_PropGroup
'''from .bl_archiver_properties import Bl_Archiver_PropGroup
from .bl_archiver_operators import BA_OT_Initialize_Bl_Archiver
from .bl_archiver_ui import BA_PT_BlArchiver_Menu
from .bl_archiver_operators import BA_OT_Blend_Network'''




# Centerobj Pointer


classes = (    PP_OT_Collect_VSE_Original,
    PP_OT_Render_VSE_Snippets,
    PP_OT_Initialize_Archiver,
       PP_PT_VSEArchiver_Menu,
       VSE_Archiver_MetaStrip,
       VSE_Archiver_SequenceStrip,
       VSE_Archiver_Keys,
       VSE_Archiver_PropGroup,
       #Bl_Archiver_PropGroup,
       #BA_PT_BlArchiver_Menu,
       #BA_OT_Initialize_Bl_Archiver,
    #BA_OT_Blend_Network,
    PP_OT_Arch_ResetMetastrip, 
    PP_OT_Arch_UpdateMetastrip,
    PP_OT_Arch_RenderSeq_Off,
    PP_OT_Arch_RenderSeq_On,
    PP_OT_Arch_RenderMeta_On,
    PP_OT_Arch_RenderMeta_Off,
    PP_OT_Arch_RenderMovie_On,
    PP_OT_Arch_RenderMovie_Off,
    PP_OT_Arch_RenderGMeta_On,
    PP_OT_Arch_RenderGMeta_Off,
    PP_OT_Arch_RenderSound_On,
    PP_OT_Arch_RenderSound_Off,
    PP_OT_Arch_RenderScene_On,
    PP_OT_Arch_RenderScene_Off,
    PP_OT_Arch_RenderImgSeq_On,
    PP_OT_Arch_RenderImgSeq_Off,
    PP_OT_Arch_RenderImage_On,
    PP_OT_Arch_RenderImage_Off,
    PP_OT_Arch_RemoveArchivetag,
    #PP_OT_Arch_TestButton,
       )
#classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)
