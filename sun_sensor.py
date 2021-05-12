import bpy
import pyquaternion as q
import numpy as np

def sunSensorRead():
    
    qw, qx, qy, qz = bpy.data.objects["cubesat"].rotation_quaternion.normalized()
    ref = bpy.data.objects["EarthSurface"]
    cube = bpy.data.objects["cubesat"]
    sun = bpy.data.objects["Point"]
    
    mw = ref.matrix_world
    mwi = mw.inverted()
    
    cubeL =   mwi @ cube.matrix_world.translation                               #origin
    sunL = mwi @ sun.matrix_world.translation                                   #destination
    direction = (sunL-cubeL).normalized()                                       #destination - origin
    result, loc, normal, index = ref.ray_cast(cubeL,direction)
    
    
    #Can observe ray projection with this:
    #bpy.ops.object.empty_add(location = loc)
    
    if (result == True):
        return
    else:
        rotQuat = q.Quaternion(qw,qx,qy,qz)
        defaultPOS = np.array([ [1,0,0],
                                [-1,0,0],
                                [0,1,0],
                                [0,-1,0],
                                [0,0,1],
                                [0,0,-1]
                               ]).T
                            #S2, S3, S1, S0, S4, S5
        faceData = np.array([             
                            [0.0,0.0,0.0,0.0,0.0,0.0],                                      #angle
                            [0.0,0.0,0.0,0.0,0.0,0.0],                                      #voltage
                            [0.0,0.0,0.0,0.0,0.0,0.0],                                      #illuminance lux
                            ])                                                  
        columns = defaultPOS.shape[1]
        
        for i in range(columns):
            face = rotQuat.rotate(defaultPOS[:, i])
            lghtVect = (sun.location - cube.location)
            faceData[0, i] = (180/np.pi) * np.arccos(np.dot(face, lghtVect)/(np.linalg.norm(face) * np.linalg.norm(lghtVect)))
            #Output voltage
            if faceData[0, i] > 90:
                faceData[1, i] = 0.04
                faceData[2, i] = faceData[1,i] * 0.5 #mA
            #Output Lux   
            elif (0 <= faceData[0, i]) and (faceData[0, i] <= 90):
                faceData[1, i] = ((3.16 * (90 - faceData[0, i])) /90) + 0.04
                faceData[2, i] = faceData[1,i] * 0.5 #mA

