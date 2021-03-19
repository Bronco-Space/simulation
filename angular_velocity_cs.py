import bpy
from math import sqrt
import numpy as np
from scipy.spatial.transform import Rotation, RotationSpline
from threading import Timer

cubePos = bpy.data.objects["cubesat"].rotation_euler
times = [0] #example data without timestep
rotPos = [[cubePos[0], cubePos[1], cubePos[2]]] #rotation positions
dispC = 1



def angVel(times, angles):
    #values need to be cycled in and out of these two arrays of arrays based off of a time step. this will probably be done with a series of if else function
    rotations = Rotation.from_euler('XYZ', angles, degrees=True)
    spline = RotationSpline(times, rotations)
    angular_vel = np.rad2deg(spline(times, 1))
    
    print(angular_vel)
    return angular_vel
    
def arManager():
    cubePos = bpy.data.objects["cubesat"].rotation_euler
    global times
    global rotPos
    global dispC
    if (len(times)) < 15: #lists need to dynamically increase in size otherwise the readout from the angular velocity function are incorrect
        times.append(dispC)
        testRotate = bpy.data.objects["cubesat"]
        testRotate.rotation_euler = [dispC, dispC, dispC] #in for testing purposes
        rotPos.append(([cubePos[0], cubePos[1], cubePos[2]])) #issue with code here will probably woek 
        dispC = dispC + 1
    else:
        times.append(dispC) #test value
        times.pop(0)
        rotPos.append(([cubePos[0], cubePos[1], cubePos[2]]))
        rotPos.pop(0)
        dispC = dispC + 1
     
    #testing   
    print(times)
    print(rotPos)
    print(dispC)
    
    


#Temporary Testing Environmet
x = True
while x == True:
    t = Timer(1, arManager)
    t.start()
    t.join()
   
    AV = Timer(1, angVel, [times, rotPos])
    AV.start()
    AV.join()
   
    
    if len(times) == 10:
        testRotate = bpy.data.objects["cubesat"]
        testRotate.rotation_euler = [0, 0, 0]
        t.cancel()
        AV.cancel()
        print("test over")
        x = False 