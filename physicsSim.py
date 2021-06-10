import bpy
from math import sqrt
from pyquaternion import Quaternion
import numpy as np
import mathutils as mat

frames = [bpy.data.objects["cubesat"].rotation_quaternion, bpy.data.objects["cubesat"].rotation_quaternion]
satQuat = bpy.data.objects["cubesat"].rotation_quaternion                                                       #initial value needed for qCurrent
qCurrent = Quaternion(satQuat[0], satQuat[1], satQuat[2], satQuat[3]).normalised 

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

    def getAngVar(self):
        
        global frames
        
        initFrame = frames[0]  
        finlFrame = frames[1]  
        qinit = Quaternion(initFrame[0],initFrame[1],initFrame[2],initFrame[3]).normalised
        qfinal = Quaternion(finlFrame[0],finlFrame[1],finlFrame[2],finlFrame[3]).normalised
        
        qrot = qfinal * qinit.conjugate
        
        return qrot

    def setAngVar(self, dx, dy, dz):
            
        global qCurrent
        
        self.dx = dx
        self.dy = dy
        self.dz = dz
        qx = Quaternion(axis=(1.0, 0.0, 0.0), degrees = dx).normalised
        qy = Quaternion(axis=(0.0, 1.0, 0.0), degrees = dy).normalised
        qz = Quaternion(axis=(0.0, 0.0, 1.0), degrees = dz).normalised
        
        qDelta = (qx*qy*qz).normalised                                
        qNew = (qDelta * qCurrent).normalised                                                                  
        bpy.data.objects["cubesat"].rotation_quaternion = mat.Quaternion((qNew[0], qNew[1], qNew[2], qNew[3]))  #Orientation Set
        qCurrent = qNew
        
        return qCurrent

  
        
    
