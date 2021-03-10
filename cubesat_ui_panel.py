import bpy
import os
import sys

#needed to locate file containing functions
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import gravity_calc as grav
import mag_calc as mag


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
        force = grav.gravForce()
        acc = grav.gravAccel()
        col = layout.column(align=True)
        col.label(text= "Grav Force Experienced (N):")
        col.label(text=f'x:{round(force.x, 3)} y:{round(force.y, 3)} z:{round(force.z, 3)}')
        col.label(text= "Grav Acc Experienced (m/sec^2):")
        col.label(text=f'x:{round(acc.x, 3)} y:{round(acc.y, 3)} z:{round(acc.z, 3)}')

        # Readout of magnetic properties
        magf = mag.get_magnetic_force(bpy.data.objects['cubesat'].location)
        col = layout.column(align=True)
        col.label(text= "North component:")
        col.label(text='{:>+10.3f}'.format(magf[0]))
        col.label(text= "East component:")
        col.label(text='{:>+10.3f}'.format(magf[1]))
        col.label(text= "Vertical component (+ve down):")
        col.label(text='{:>+10.3f}'.format(magf[2]))
        col.label(text= "Total intensity:")
        col.label(text='{:>+10.3f} nT'.format(magf[3]))
        
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
