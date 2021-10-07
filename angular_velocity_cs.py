from pyquaternion import Quaternion
import numpy as np
import bpy
import mathutils as mat

frames = [bpy.data.objects["cubesat"].rotation_quaternion, bpy.data.objects["cubesat"].rotation_quaternion]                            
satQuat = bpy.data.objects["cubesat"].rotation_quaternion          
qCurrent = Quaternion(satQuat[0], satQuat[1], satQuat[2], satQuat[3]).normalised 


#angular velocity over one frame's worth of time
def getAngVar():
        
    global frames
    
    initFrame = frames[0]   
    finlFrame = frames[1]  
    qinit = Quaternion(initFrame[0],initFrame[1],initFrame[2],initFrame[3]).normalised
    qfinal = Quaternion(finlFrame[0],finlFrame[1],finlFrame[2],finlFrame[3]).normalised
    
    qrot = qfinal * qinit.conjugate
    
    return qrot

def setAngVar(velQuat):
            
    global qCurrent
    global frames
    
    qDelta = velQuat.normalised                                
    qNew = (qDelta * qCurrent).normalised                                                                  
    bpy.data.objects["cubesat"].rotation_quaternion = mat.Quaternion((qNew[0], qNew[1], qNew[2], qNew[3]))  #Orientation Set
    qCurrent = qNew
    frames[0] = frames[1]
    frames[1] = qCurrent
    
    return qCurrent

