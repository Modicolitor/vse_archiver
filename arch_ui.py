import bpy



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

            subcol.operator("varch.archive", text="Archiv",
                            icon="PLUS")  # zeige button an
            subcol.property(arch_props, "remove_fade")
            subcol.property(arch_props, "new_folder_name")

        else:

            subcol.operator("varch.init", text="Initialize",
                            icon="PLUS")