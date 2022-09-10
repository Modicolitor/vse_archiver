
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
    "version": (3, 2),
    "blender": (3, 2, 0),
    "location": "Sequence Editor > Tools",
    "description": "Save used Footage of a VSE Video project",
    "doc_url": "", ####################
    "category": "Tool"}

# modules = addon_auto_imports.setup_addon_modules(
#    __path__, __name__, ignore_packages=[], ignore_modules=[]
# )
''' hallo'''

from .vse-arch_operators import PP_OT_Collect_VSE_Original
from .vse-arch_operators import PP_OT_Render_VSE_Snippets
from .vse-arch_operators import PP_OT_Initialize_Archiver
from .vse-arch_ui import PP_PT_VSEArchiver_Menu
from .vse-arch_properties import VSE_Archiver_PropGroup
from .bl-arch_properties import Bl_Archiver_PropGroup



# Centerobj Pointer


classes = (    PP_OT_Collect_VSE_Original,
    PP_OT_Render_VSE_Snippets,
    PP_OT_Initialize_Archiver,
       PP_PT_VSEArchiver_Menu,
       VSE_Archiver_PropGroup,
       )
#classes = ()
register, unregister = bpy.utils.register_classes_factory(classes)
