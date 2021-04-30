import bpy
import mathutils
def sunSensorRead():
    ###line of slight data to determine if code should run.
    ###earth needs to not be rotated and the scale needs to be reset
    ###for face check on satelite, offset rays by one unit or so to sit directly behind face and then draw to see if it hits satellite body
    ref = bpy.data.objects["EarthSurface"]
    cube = bpy.data.objects["cubesat"]
    sun = bpy.data.objects["Point"]
    
    mw = ref.matrix_world
    mwi = mw.inverted()
    
    cubeL =   mwi @ cube.matrix_world.translation #origin
    sunL = mwi @ sun.matrix_world.translation #destination
    direction = (sunL-cubeL).normalized() #destination - origin
    
    result, loc, normal, index = ref.ray_cast(cubeL,direction)
    
    
    #can see ray projection and ray length with this code
    bpy.ops.object.empty_add(location = loc)
    #distance = mw @ loc
    #if result == false:
        #do not run code
sunSensorRead()