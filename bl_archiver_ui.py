import bpy

class BA_PT_BlArchiver_Menu(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_label = "Archiver Modes"
    bl_context = "render"
    bl_category = "Blender Archiver"

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

        if hasattr(context.scene, "bl_archiver"):  # "PuzzleUrPrint" in data.collections and
            arch_props = context.scene.bl_archiver
            subcol = col.column()

            #subcol.prop(arch_props, "mode")
            subcol.prop(arch_props, "use_blend_data")
            #subcol.prop(arch_props, "rebuild", text='Rebuild Blend')

            

        else:

            subcol.operator("blarch.init", text="Initialize",
                            icon="PLUS")