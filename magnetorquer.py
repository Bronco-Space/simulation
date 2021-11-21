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
    return dCycle * 0.8

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

    dir_magx = True
    dir_magy = True
    dir_magz = True
    
    print("torque dimensions", torque.shape)
    Ixx = (1/12)*(m)*((cubesat.dimensions.y)**2 + (cubesat.dimensions.z)**2)
    Iyy = (1/12)*(m)*((cubesat.dimensions.x)**2 + (cubesat.dimensions.z)**2)
    Izz = (1/12)*(m)*((cubesat.dimensions.x)**2 + (cubesat.dimensions.y)**2)

  

    time = 1 #timestep
    t = sympy.symbols("t")

    Ix, Iy, Iz = sympy.symbols("Ix Iy Iz")
    
    wx, wy, wz = sympy.symbols("wx wy wz")
    

    ax, ay, az = sympy.symbols("ax, ay, az")
    
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


    ans = sympy.solve([eq_wx, eq_wy, eq_wz], (wx,wy,wz), dict = True)
    print("these are the rads", ans)

    if dir_magx == True: -ans[0][wx]
    if dir_magy == True: -ans[0][wy]
    if dir_magz == True: -ans[0][wz]

    qx = q.Quaternion(axis=(1.0, 0.0, 0.0), radians = ans[0][wx]).normalised
    qy = q.Quaternion(axis=(0.0, 1.0, 0.0), radians = ans[0][wy]).normalised
    qz = q.Quaternion(axis=(0.0, 0.0, 1.0), radians = ans[0][wz]).normalised
        
    omegaQ = (qx*qy*qz).normalised 
    print("print", omegaQ)
    return omegaQ

def reactWhl(Tm): 
    #time step
    time = 1
    t = sympy.Symbol("t")
    m = 1.75 #kg
    #Ixx, Iyy, Izz pull data from the cubesat object, and assuming a rectangular prism for moment of inertia calculations
    
    dir_reactx = True
    dir_reacty = True
    dir_reactz = True
    
    Ixx = (1/12)*(m)*((cubesat.dimensions.y)**2 + (cubesat.dimensions.z)**2)
    Iyy = (1/12)*(m)*((cubesat.dimensions.x)**2 + (cubesat.dimensions.z)**2)
    Izz = (1/12)*(m)*((cubesat.dimensions.x)**2 + (cubesat.dimensions.y)**2)

    #board properties
    board_current = 0.8
    max_angvel = 12000

    #duty cycle for wheels
    dc_x = convertDutyCycle(cubesat.get("dWx"))
    dc_y = convertDutyCycle(cubesat.get("dWy"))
    dc_z = convertDutyCycle(cubesat.get("dWz"))

    #wheel specs
    i_x = 1 #average current going into x-axis motor [A]
    i_y = 1 #average current going through y-axis motor [A]
    i_z = 1 #average current going through z-axis motor [A]
    Kt = 0.001 #torque constant of wheel (Nm) at nominal momentum (0.01Nms)
    m = 0.120 #mass of wheel (kg)
    r = 0.025 #radius of wheel (m)
    d = 0.005 #wheel density

    #moment of inertia of satellite's body (diagonal)
    Ix, Iy, Iz = sympy.symbols("Ix Iy Iz")

    #reaction wheel angular momentum
    hw_x, hw_y, hw_z = sympy.symbols("hw_x hw_y hw_z")

    #applied reaction wheel torques
    Tw_x, Tw_y, Tw_z = sympy.symbols("Tw_x Tw_y Tw_z")

    #magnetic torque vector induced by magnetorquers
    Tm_x, Tm_y, Tm_z = sympy.symbols("Tw_x Tw_y Tw_z")

    #total torque
    Tx, Ty, Tz = sympy.symbols("Tx Ty Tz")

    #angular velocity
    wx, wy, wz = sympy.symbols("wx wy wz")

    #calculate current from duty cycle
    i_x = (dc_x*board_current)
    i_y = (dc_y*board_current)
    i_z = (dc_z*board_current)

    #calculate Tw
    Tw_x = Kt*i_x
    Tw_y = Kt*i_y
    Tw_z = Kt*i_z

    #calculate wheel angular velocity 
    
    #RPM to rad/s -> multiply by pi/30
    ww_x = (dc_x*max_angvel)*np.pi/30
    ww_y = (dc_y*max_angvel)*np.pi/30
    ww_z = (dc_z*max_angvel)*np.pi/30

    #calculate hw
    hw_x =  (((0.5)*m*(r**2)) + (m*(d**2)))*ww_x
    hw_y =  (((0.5)*m*(r**2)) + (m*(d**2)))*ww_y
    hw_z =  (((0.5)*m*(r**2)) + (m*(d**2)))*ww_z

    #T = Tm - Tw
    Tx = Tm_x - Tw_x
    Ty = Tm_y - Tw_y
    Tz = Tm_z - Tw_z

    Tx = Tx.subs([(Tm_x, Tm[0]), (Tw_x, Tw_x)])
    Ty = Ty.subs([(Tm_y, Tm[1]), (Tw_y, Tw_y)])
    Tz = Tz.subs([(Tm_z, Tm[2]), (Tw_z, Tw_z)])
    
    
    ax = (Tx - ((Iy - Iz)*wz*wy) + (hw_z*wy) - (hw_y*wz))/Ix
    ay = (Ty - ((Iz - Ix)*wx*wz) + (hw_x*wz) - (hw_z*wx))/Iy
    az = (Tz - ((Ix - Iy)*wy*wx) + (hw_y*wx) - (hw_x*wy))/Iz

    ax = ax.subs([(Tx, Tx), (Iy, Iyy), (Iz, Izz), (wz, ww_z), (wy, ww_y), (hw_z, hw_z), (hw_y, hw_y), (Ix, Ixx)])
    ay = ay.subs([(Ty, Ty), (Iz, Izz), (Ix, Ixx), (wx, ww_x), (wz, ww_z), (hw_x, hw_x), (hw_z, hw_z), (Iy, Iyy)])
    az = az.subs([(Tz, Tz), (Iy, Iyy), (Ix, Ixx), (wy, ww_y), (wx, ww_x), (hw_y, hw_y), (hw_x, hw_x), (Iz, Izz)])

    eq_wx = sympy.integrate(ax, (t, 0, time))
    eq_wy = sympy.integrate(ay, (t, 0, time))
    eq_wz = sympy.integrate(az, (t, 0, time))

    eq_wx = sympy.Eq(eq_wx, wx)
    eq_wy = sympy.Eq(eq_wy, wy)
    eq_wz = sympy.Eq(eq_wz, wz)
    
    ans = sympy.solve([eq_wx, eq_wy, eq_wz], (wx,wy,wz), dict = True)
    print("ans:", ans)

    if dir_reactx == True: -ans[0][wx]
    if dir_reacty == True: -ans[0][wy]
    if dir_reactz == True: -ans[0][wz]

    qx = q.Quaternion(axis=(1.0, 0.0, 0.0), radians = ans[0][wx]).normalised
    qy = q.Quaternion(axis=(0.0, 1.0, 0.0), radians = ans[0][wy]).normalised
    qz = q.Quaternion(axis=(0.0, 0.0, 1.0), radians = ans[0][wz]).normalised
    omegaQ = (qx*qy*qz).normalised 
    return omegaQ

def controlSysMag(torque, omega):                                           #direction is a true/false value determined by the ai
    if (cubesat.get("magX")) > 0 or (cubesat.get("magY")) > 0 or (cubesat.get("magZ")) > 0:
        omegaT = velCtrl(torque)            
        omegaNF = omega + omegaT #nf = new frame    
    else:         
        omegaNF = omega      
    return omegaNF       

def controlSysReact(torque, omega):                                           #direction is a true/false value determined by the ai
    if (cubesat.get("dWx")) > 0 or (cubesat.get("dWy")) > 0 or (cubesat.get("dWz")) > 0:
        omegaRW = reactWhl(torque)             
        omegaNF = omega + omegaRW #nf = new frame    
    else:         
        omegaNF = omega      
    return omegaNF       