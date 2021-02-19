import bpy
import os
import sys

#needed to locate file containing functions
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import gravity_calc as grav


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

        # Cubesat readout. Note: assumes cubesats name is 'cubesat'
        col = layout.column(align=True)
        col.label(text="Cubesat")
        col.prop(bpy.data.objects['cubesat'], "location")
        
	    # Center of mass readout. Note: assumes center of mass's name is 'centerofmass'
        col = layout.column(align=True)
        col.label(text="Center of Mass")
        col.prop(bpy.data.objects['centerofmass'], "location")
        
        # Readout of gravitational properties
        a = str(grav.gravForce())
        b = str(grav.gravAccel())
        layout.label(text= "Gravitational Force Experienced (MicroNewtons):")
        layout.label(text= a)
        layout.label(text= "Gravitational Acceletation Experienced (Micrometers/sec^2):")
        layout.label(text = b)

	#Reload scripts
        row = layout.row()
        row.operator("myops.reload_scripts")

#Stuff that is required for the script to work
def register():
    bpy.utils.register_class(VIEW3D_PT_cubesat)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_cubesat)


if __name__ == "__main__":
    register()
