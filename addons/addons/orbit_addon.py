bl_info = {
    "name": "Orbit",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

# Operator used to set new altitude
class operator_set_altitude(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "myops.set_altitude"
    bl_label = "Set Altitude"

    #This function is called when the button is clicked
    def execute(self, context):
        orbitRadius = (bpy.data.objects['Orbit'].data.splines[0].bezier_points[0].co - bpy.data.objects['Orbit'].data.splines[0].bezier_points[2].co).length / 2
        earthRadius = (bpy.data.objects['EarthSurface'].data.vertices[205].co - bpy.data.objects['EarthSurface'].data.vertices[296].co).length / 2
        val = bpy.context.scene['orbit_props']['altitude'] + earthRadius
        print(val)
        bpy.data.objects['Orbit'].data.splines[0].bezier_points[0].co.x = -val
        bpy.data.objects['Orbit'].data.splines[0].bezier_points[2].co.x = val
        bpy.data.objects['Orbit'].data.splines[0].bezier_points[3].co.y = -val
        bpy.data.objects['Orbit'].data.splines[0].bezier_points[1].co.y = val
        return {'FINISHED'}

# Custom Properties for orbit
# Accessible from bpy.context.scene['orbit_props']
class orbit_property_group(PropertyGroup):
    # Accessible from bpy.data.scenes['Scene'].orbit_props.logging
    period : IntProperty(
        name="period",
        description = "Period of Orbit",
        default = 100,
        min = 0
    )
    altitude : FloatProperty(
        name="altitude",
        description="Altitude of Orbit",
        default = 0.0,
        subtype = 'DISTANCE',
        unit = 'LENGTH',
        min = 0.0
    )
    angle : FloatProperty(
        name="angle",
        description="Angle of Orbit",
        default = 0.0,
        subtype = 'ANGLE',
        unit = 'ROTATION',
        min = -1.57,        # Angles are in radians
        max = 1.57
    )

# Orbit panel
class VIEW3D_PT_orbit(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Orbit Sim Controls" #Visual full name of menu
    bl_idname = "SCENE_PT_layout2" #Name of menu on the backend
    bl_space_type = "VIEW_3D"   #Viewable ONLY in the 3d view port
    bl_region_type = "UI" #Specifies that it appears in the tools bar
    bl_category = "Orbit" #Name on the side bar of the tools bar
    bl_context = "objectmode" #Viewable ONLY in object mode

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        orbit_props = scene.orbit_props

        # Logging checkbox
        row = layout.row()
        row.prop(orbit_props, "period", text="Orbit Period (min)")

        # Controls Orbit's altitude
        col = layout.column(align=True)
        orbitRadius = (bpy.data.objects['Orbit'].data.splines[0].bezier_points[0].co - bpy.data.objects['Orbit'].data.splines[0].bezier_points[2].co).length / 2    # bezier_points 0 and 2 are opposing points on the circle
        earthRadius = (bpy.data.objects['EarthSurface'].data.vertices[205].co - bpy.data.objects['EarthSurface'].data.vertices[296].co).length / 2                  # Vertices 205 and 296 are the poles of a default UV sphere
        col.label(text='Current Altitude: {:>10.3f}'.format(orbitRadius - earthRadius)) # Display current actual altitude

        col.prop(orbit_props, "altitude", text="New Altitude")                        # Allow selecting of new altitude

        col.operator("myops.set_altitude")                                             # Set new altitude

        # Control Orbit's angle. Just pass through rotation_euler
        col = layout.column(align=True)
        col.label(text="Orbit Angle")
        col.prop(bpy.data.objects['Orbit'], "rotation_euler")

        #bpy.data.objects['Orbit'].rotation_euler.x = orbit_props['angle'] * 3.14159265 / 180
        

def addDrivers(self, context):
    # Add driver for angle based on bpy.context.scene.orbit_props.angle
    # EX: https://blenderartists.org/t/create-a-driver-for-an-object-via-python-2-5/499701/3
    d = bpy.data.objects["Orbit"].data.driver_add('path_duration')   # Adds new driver based on "Orbit's" rotation_euler. Index of 0 indicates X rotation per XYZ format
    v = d.driver.variables.new()                                    # Create new variable for use within driver
    v.name = 'frames'                                             # Name new variable 'rotation
    v.type = 'SINGLE_PROP'                                          # Define type of new variable to 'SINGLE_PROP'. Valid values include ('SINGLE_PROP', 'TRANSFORMS', 'ROTATION_DIFF', 'LOC_DIFF') (Found by giving v.type an invalid type)
    v.targets[0].id_type = 'SCENE'                                  # Set type of variable property to SCENE. index 0 here selects the variable contained within the driver. Unfortunately cannot use targets['rotation']. Valid values include ('ACTION', 'ARMATURE', 'BRUSH', 'CAMERA', 'CACHEFILE', 'CURVE', 'FONT', 'GREASEPENCIL', 'COLLECTION', 'IMAGE', 'KEY', 'LIGHT', 'LIBRARY', 'LINESTYLE', 'LATTICE', 'MASK', 'MATERIAL', 'META', 'MESH', 'MOVIECLIP', 'NODETREE', 'OBJECT', 'PAINTCURVE', 'PALETTE', 'PARTICLE', 'LIGHT_PROBE', 'SCENE', 'SIMULATION', 'SOUND', 'SPEAKER', 'TEXT', 'TEXTURE', 'HAIR', 'POINTCLOUD', 'VOLUME', 'WINDOWMANAGER', 'WORLD', 'WORKSPACE')
    v.targets[0].id = bpy.context.scene                             # Set the scene as the selected scene the property is within
    v.targets[0].data_path = 'orbit_props.period'                    # Set the scene property the variable should reference
    d.driver.expression = v.name                                    # The driver expression, in this case just a 1-1 mapping of the orbit_props.angle to the Orbit objects rotation
    
    if addDrivers in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(addDrivers)    
    
#Stuff that is required for the script to work
def register():
    bpy.utils.register_class(orbit_property_group)
    bpy.utils.register_class(VIEW3D_PT_orbit)
    bpy.utils.register_class(operator_set_altitude)

    bpy.types.Scene.orbit_props = PointerProperty(type=orbit_property_group)

    if not addDrivers in bpy.app.handlers.depsgraph_update_post:    # https://blenderartists.org/t/restrictdata-object-has-no-attribute-scenes-how-to-avoid-it/579885/5
        bpy.app.handlers.depsgraph_update_post.append(addDrivers)
    


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_orbit)
    bpy.utils.unregister_class(orbit_property_group)
    bpy.utils.unregister_class(operator_set_altitude)

    #Remvoe driver for angle
    bpy.data.objects["Orbit"].data.driver_remove('path_duration')
    
    del bpy.types.Scene.orbit_props

