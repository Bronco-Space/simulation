from pyquaternion import Quaternion
import numpy as np
import bpy

#needs to account for time
frames = [bpy.data.objects["cubesat"].rotation_quaternion, bpy.data.objects["cubesat"].rotation_quaternion]
qCurrent = Quaternion(0.665, 0.467, 0.189, 0.551-).normalised #what quaternion is at current frame in simulation

#angular velocity over one frame's worth of time
def getAngVar():
    global frames
    frames[0] = initframe
    frames[1] = finlframe
    qinit = Quaternion(initFrame[0],initFrame[1],initFrame[2],initFrame[3]).normalised
    qfinal = Quaternion(finlFrame[0],finlFrame[1],finlFrame[2],finlFrame[3]).normalised
    qrot = qfinal * qinit.conjugate
    return qrot


def setAngVar(dx, dy, dz):
        
        global qRef
        global qCurrent
        
        qx = Quaternion(axis=(1.0, 0.0, 0.0), degrees = dx).normalised
        qy = Quaternion(axis=(0.0, 1.0, 0.0), degrees = dy).normalised
        qz = Quaternion(axis=(0.0, 0.0, 1.0), degrees = dz).normalised
        qDelta = (qx*qy*qz).normalised                                 #Equivalent to XYZ Euler?
        
        qNew = (qDelta * qCurrent).normalised                          #New orientation for the next frame.
        qDeltaCheck = (qNew * qCurrent.conjugate).normalised
        #set both qCurrent and satellite rotation to qNew
        
        

