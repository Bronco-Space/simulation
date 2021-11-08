import bpy
import os
import sys
import numpy
import mag_calc as mag
import mathutils
import time
import numpy as np
import pyquaternion as q
import sympy



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

    
cubesat = bpy.data.objects['cubesat']
def convertDutyCycle(dCycle):
    return dCycle * 0.05

def calcTorque(magf):
    #This is just to make it obvious that a new line in the console has been printed
    
    magf = [item * (10**(-9)) for item in magf] #converts from microtesla to tesla
    print("magf", magf)
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
    x_mag_dipole = convertDutyCycle(cubesat.get("magX")) * cubesat.get("magX_Turns") * cubesat.get("magX_A")
    y_mag_dipole = convertDutyCycle(cubesat.get("magY")) * cubesat.get("magY_Turns") * cubesat.get("magY_A")
    z_mag_dipole = convertDutyCycle(cubesat.get("magZ")) * cubesat.get("magZ_Turns") * cubesat.get("magZ_A")
    print("xdipole", x_mag_dipole)
    print("ydipole", y_mag_dipole)
    print("zdipole", z_mag_dipole)
    
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

def velCtrl(torque):
    #Cubesat Properties
    cubesat = bpy.data.objects['cubesat']
    m = 1.75 #kg
    #Ixx, Iyy, Izz pull data from the cubesat object, and assuming a rectangular prism for moment of inertia calculations
    
    print("torque dimensions", torque.shape)
    Ixx = (1/12)*(m)*((cubesat.dimensions.y)**2 + (cubesat.dimensions.z)**2)
    Iyy = (1/12)*(m)*((cubesat.dimensions.x)**2 + (cubesat.dimensions.z)**2)
    Izz = (1/12)*(m)*((cubesat.dimensions.x)**2 + (cubesat.dimensions.y)**2)

  

    time = 1 #timestep
    t = sympy.symbols("t")

    Ix, Iy, Iz = sympy.symbols("Ix Iy Iz")
    
    wx, wy, wz = sympy.symbols("wx wy wz")
    

    alx, aly, alz = sympy.symbols("alx, aly, alz")
    
    Tx, Ty, Tz = sympy.symbols("Tx, Ty, Tz")
    

    ax = (Tx - ((Iy-Iz)*wy*wz))/Ix
    ay = (Ty - ((Ix-Iz)*wx*wz))/Iy
    az = (Tz - ((Iy-Ix)*wx*wy))/Iz

    ax = ax.subs([(Tx, torque[0]), (Iy, Iyy), (Iz, Izz), (Ix, Ixx)])
    ay = ay.subs([(Ty, torque[1]), (Iy, Iyy), (Iz, Izz), (Ix, Ixx)])
    az = az.subs([(Tz, torque[2]), (Iy, Iyy), (Iz, Izz), (Ix, Ixx)])

    eq_wx = sympy.integrate(ax, (t, 0, time))
    eq_wy = sympy.integrate(ay, (t, 0, time))
    eq_wz = sympy.integrate(az, (t, 0, time))

    eq_wx = sympy.Eq(eq_wx, wx)
    eq_wy = sympy.Eq(eq_wy, wy)
    eq_wz = sympy.Eq(eq_wz, wz)


    ans = sympy.solve([eq_wx, eq_wy, eq_wz], (wx,wy,wz))

    qx = q.Quaternion(axis=(1.0, 0.0, 0.0), radians = ans[0][0]).normalised
    qy = q.Quaternion(axis=(0.0, 1.0, 0.0), radians = ans[0][1]).normalised
    qz = q.Quaternion(axis=(0.0, 0.0, 1.0), radians = ans[0][2]).normalised
        
    omegaQ = (qx*qy*qz).normalised 
    return omegaQ


def controlSys(torque, omega, direction):                                           #direction is a true/false value determined by the ai
    if (cubesat.get("magX")) > 0 or (cubesat.get("magY")) > 0 or (cubesat.get("magZ")) > 0:
       
        omegaT = velCtrl(torque)    
        
        if direction == True:          
            omegaNF = omega - omegaT #nf = new frame    
        else:
            omegaNF = omega + omegaT
    else:         
        omegaNF = omega      #return omegaNF       