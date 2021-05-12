import bpy
from math import sqrt
import numpy as np
from scipy.spatial.transform import Rotation, RotationSpline
from threading import Timer
#gravitational force vector between Earth and Cubesat

def gravForce():
    
    cube = bpy.data.objects["cubesat"].location * 10000
    cubeR = sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2)) #in m
    massC = 1.75 # in kg
    
    
    earthDim = bpy.data.objects["EarthSurface"].dimensions * 10000
    earthR = earthDim[1]/2
    dens = 5515 #kg/m^3
    volE = (4/3)*(3.14159)* (earthR)**3 #m^3
    massE = dens * volE #kg
    

    gravC = (6.67408 * 10**(-11))
    unitVectR = cube / cubeR
    
    force = -((gravC * massE *massC) / (cubeR**2)) * unitVectR  #newtons
    
    return force

#gravitational acceleration experienced by satellite
def gravAccel():
    
    cube = bpy.data.objects["cubesat"].location * 10000
    cubeR = sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2)) #in m
    

    earthDim = bpy.data.objects["EarthSurface"].dimensions * 10000
    earthR = earthDim[1]/2
    dens = 5515 #kg/m^3
    volE = (4/3)*(3.14159)* (earthR)**3 #m^3
    massE = dens * volE #kg
    gravE = ((6.67408 * 10**(-11)) * massE) / (earthR**2)
    
    unitVectR = cube / cubeR
    accel = -(gravE * (earthR**2) / (cubeR ** 2))* unitVectR #meters/s^2
    return accel

def angVel(times, angles):
    #values need to be cycled in and out of these two arrays of arrays based off of a time step. this will probably be done with a series of if else function
    rotations = Rotation.from_euler('XYZ', angles, degrees=True)
    spline = RotationSpline(times, rotations)
    angular_vel = np.rad2deg(spline(times, 1))
    return angular_vel
    



cubePos = bpy.data.objects["cubesat"].rotation_euler
times = [0] #example data without timestep
rotPos = [[cubePos[0], cubePos[1], cubePos[2]]] #rotation positions
dispC = 1

def arManager():
    cubePos = bpy.data.objects["cubesat"].rotation_euler
    global times
    global rotPos
    global dispC
    if (len(times)) < 15: #lists need to dynamically increase in size otherwise the readout from the angular velocity function are incorrect
        times.append(dispC)
        rotPos.append(([cubePos[0], cubePos[1], cubePos[2]]))
        dispC = dispC + 1
    else:
        times.append(dispC) #test value
        times.pop(0)
        rotPos.append(([cubePos[0], cubePos[1], cubePos[2]]))
        rotPos.pop(0)
        dispC = dispC + 1
        
    print(times)
    print(rotPos)
    print(dispC)
    
    
#x = True
#while x == True:
 #   t = Timer(2, arManager)
 #   testRotate = bpy.data.objects["cubesat"]
  #  testRotate.rotation_euler = [dispC, dispC, dispcC]
  #  t.start()
   # t.join()
    #if len(times) == 10:
     #   t.cancel()
     #   print("test over")
      #  x = False 
        
        
    
    


    






