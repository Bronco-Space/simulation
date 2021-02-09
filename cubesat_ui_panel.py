import bpy


class VIEW3D_PT_cubesat(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "CubeSat Sim Controls" #Visual full name of menu
    bl_idname = "SCENE_PT_layout" #Name of menu on the backend
    bl_space_type = "VIEW_3D"   #Viewable ONLY in the 3d view port
    bl_region_type = "UI" #Specifies that it appears in the tools bar
    bl_category = "CubeSat" #Name on the side bar of the tools bar
    bl_context = "objectmode" #Viewable ONLY in object mode

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Second column, aligned
        col = layout.column(align=True)
        col.prop(bpy.data.objects['cubesat'], "location")



#Stuff that is required for the script to work
def register():
    bpy.utils.register_class(VIEW3D_PT_cubesat)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_cubesat)


if __name__ == "__main__":
    register()
