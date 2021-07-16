import bpy
import os
import sys
import numpy
import mag_calc as mag
import mathutils
import time

# These are general notes and points of reference
#https://blenderartists.org/t/global-to-local-coordinates/506907/2
#https://stackoverflow.com/questions/7132018/how-to-convert-global-to-local-coordinates-in-blender-2-5
#https://blender.stackexchange.com/questions/14137/converting-global-object-location-to-local-location-in-python
#refPoint = bpy.data.objects['magRef']
#global_coord = refPoint.matrix_world.translation
##local_coord = refPoint.matrix_world.inverted() @ global_coord # Strictly speaking unnecessary because REF will always be at 0,0,0 locally, figure out how to avoid this later
#vector_local_coord = mathutils.Vector((local_coord.x + east, local_coord.y + north, local_coord.z + up)) # Could just be Vector(east, north, up)
#vector_global_coord = refPoint.matrix_world @ vector_local_coord

# TODO: Change to use more accurate conversions. This is based on the general estimation Chris gave in discord
def convertDutyCycle(axis, dCycle):
    return dCycle * 8


def calcTorque(magf):
    #This is just to make it obvious that a new line in the console has been printed
    print(time.time() % 100)
    magComp = {
        "north": magf[0],
        "east": magf[1],
        "down": magf[2],
        "intensity": magf[3]
    }
    
    cubesat = bpy.data.objects['cubesat']
    magRef = bpy.data.objects['magRef']

    # pyIGRF seems to return these as nT, make sure units are consistent and scale is good
    vector_ref_local_point = mathutils.Vector((magComp["north"], magComp["east"], magComp["down"])) #The point in magRef's local space the vector points to
    vector_global_point = magRef.matrix_world @ vector_ref_local_point#The point in global space the vector points to
    vector_cube_local_point = cubesat.matrix_world.inverted() @ vector_global_point #The point in cubesat's local space the vector points to

    # m = nIA - 
    # TODO: Ask Matteo for clarification on more detailed formula, he mentioned something about cores. Also ask about more accurate N and A
    x_mag_dipole = convertDutyCycle("x", cubesat.get("magX")) * cubesat.get("magX_Turns") * cubesat.get("magX_A")
    y_mag_dipole = convertDutyCycle("y", cubesat.get("magY")) * cubesat.get("magY_Turns") * cubesat.get("magY_A")
    z_mag_dipole = convertDutyCycle("z", cubesat.get("magZ")) * cubesat.get("magZ_Turns") * cubesat.get("magZ_A")

    magnetorquer_vector = mathutils.Vector((x_mag_dipole, y_mag_dipole, z_mag_dipole))
    torque_vector = vector_cube_local_point.cross(magnetorquer_vector)
    print(f'vector_global_point {vector_global_point}')
    print(f'vector_cube_local {vector_cube_local_point}')
    print(f'mag {cubesat.matrix_world @ magnetorquer_vector}')
    print(f'torque vector {cubesat.matrix_world @ torque_vector}')
    return torque_vector
    # bpy.ops.object.select_all(action = 'DESELECT')
    # magVectorPoint.select = True
    # bpy.context.scene.objects.active = magVectorPoint
    # bpy.ops.transform.translate(value = vector_global_point)
    #magVectorPoint.location = vector_global_point #Solely for illustration purposes set an empty at the global coordinates of the vector end. An empty in the simulation is set to track magVectorPoint