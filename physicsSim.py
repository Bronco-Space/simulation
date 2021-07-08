import bpy
from math import sqrt
from pyquaternion import Quaternion
import numpy as np
import mathutils as mat
import time

#frames = [bpy.data.objects["cubesat"].rotation_quaternion, bpy.data.objects["cubesat"].rotation_quaternion]
satQuat = bpy.data.objects["cubesat"].rotation_quaternion                                                       #initial value needed for qCurrent
qCurrent = Quaternion(satQuat[0], satQuat[1], satQuat[2], satQuat[3]).normalised 


def getAngVar(self):
        
        global frames
        
        initFrame = frames[0]  
        finlFrame = frames[1]  
        qinit = Quaternion(initFrame[0],initFrame[1],initFrame[2],initFrame[3]).normalised
        qfinal = Quaternion(finlFrame[0],finlFrame[1],finlFrame[2],finlFrame[3]).normalised
        
        qrot = qfinal * qinit.conjugate
        
        return qrot

def setAngVar(dx, dy, dz):
            
        global qCurrent
        
        qx = Quaternion(axis=(1.0, 0.0, 0.0), degrees = dx).normalised
        qy = Quaternion(axis=(0.0, 1.0, 0.0), degrees = dy).normalised
        qz = Quaternion(axis=(0.0, 0.0, 1.0), degrees = dz).normalised
        
        qDelta = (qx*qy*qz).normalised                                
        qNew = (qDelta * qCurrent).normalised                                                                  
        bpy.data.objects["cubesat"].rotation_quaternion = mat.Quaternion((qNew[0], qNew[1], qNew[2], qNew[3]))  #Orientation Set
        qCurrent = qNew
        
        return qCurrent

x = 0
while x < 1:
    setAngVar(10,10,10)
    x = x + 1
   
        
    
