import bpy
from math import sqrt
from pyquaternion import Quaternion
import numpy as np
import mathutils as mat
from imu import test_imu

satQuat = bpy.data.objects["cubesat"].rotation_quaternion                                                       #initial value needed for qCurrent
qCurrent = Quaternion(satQuat[0], satQuat[1], satQuat[2], satQuat[3]).normalised 
angVarQuat = Quaternion(1,0,0,0)

class physicSim:
    
    def gravForce(self):
        
        cube = bpy.data.objects["cubesat"].location * 10000
        cubeR = sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2))                                                #in meters
        massC = 1.75                                                                                            #in kg


        earthDim = (bpy.data.objects["EarthSurface"].dimensions * 10000)
        earthR = earthDim[0]/2
        dens = 5515                                                                                             #kg/m^3
        volE = (4/3)*(3.14159)* (earthR)**3                                                                     #m^3
        massE = dens * volE                                                                                     #kg
        gravC = (6.67408 * 10**(-11))
        unitVectR = cube / cubeR

        force = -((gravC * massE *massC) / (cubeR**2)) * unitVectR                                              #newtons
    
        return force

    def gravAccel(self):
        cube = bpy.data.objects["cubesat"].location * 10000
        cubeR = sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2))                                                #in m
        

        earthDim = (bpy.data.objects["EarthSurface"].dimensions * 10000)
        earthR = earthDim[0]/2
        dens = 5515                                                                                             #kg/m^3
        volE = (4/3)*(3.14159)* (earthR)**3                                                                     #m^3
        massE = dens * volE                                                                                     #kg
        unitVectR = cube / cubeR
        gravC = (6.67408 * 10**(-11))
            
        accel = -((gravC * massE) / (cubeR ** 2))* unitVectR                                                    #meters/s^2
        
        return accel

    def AngVar(self, dx, dy, dz):
            
        global qCurrent
        global angVarQuat
        
        self.dx = dx
        self.dy = dy
        self.dz = dz
        qx = Quaternion(axis=(1.0, 0.0, 0.0), degrees = dx).normalised
        qy = Quaternion(axis=(0.0, 1.0, 0.0), degrees = dy).normalised
        qz = Quaternion(axis=(0.0, 0.0, 1.0), degrees = dz).normalised
        
        qDelta = (qx*qy*qz).normalised                                
        qNew = (qDelta * qCurrent).normalised                                                                  
        bpy.data.objects["cubesat"].rotation_quaternion = mat.Quaternion((qNew[0], qNew[1], qNew[2], qNew[3]))  #Orientation Set
        
        angVarQuat = qNew * qCurrent.conjugate #readout of current ang var
        qCurrent = qNew
        test_imu.Update(angVarQuat) # UPDATES IMU AND DISPLAYS VALUES
        return qCurrent

#test indepent of timestep
x = 0
a = physicSim()
while x < 1:
    a.AngVar(10,0,0)
    x = x + 1

   
  
        
    
