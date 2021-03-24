from pyquaternion import Quaternion
import numpy as np
import bpy

#needs to account for time
frames = [bpy.data.objects["cubesat"].rotation_quaternion, bpy.data.objects["cubesat"].rotation_quaternion]

#angular velocity over one frame's worth of time
def getAngVar():
    global frames
    initFrame = frames[0]  
    finlFrame =  frames[1] 
    qinit = Quaternion(initFrame[0],initFrame[1],initFrame[2],initFrame[3]).normalised
    qfinal = Quaternion(finlFrame[0],finlFrame[1],finlFrame[2],finlFrame[3]).normalised
    qrot = qfinal * qinit.conjugate
    return qrot

