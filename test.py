import magnetorquer as magT
import mag_calc as mag
import angular_velocity_cs as aVel
import bpy
import csv
import numpy as np
import pyquaternion as q
import mathutils


qtest = q.Quaternion(0.9885986, 0.0869346, 0.0869346, 0.0869346)

x = 0
while x < 54000:
   
    print(qtest)
    aVel.setAngVar(qtest) #does this need to be quaternion?
    magf = mag.get_magnetic_force(bpy.data.objects['cubesat'].location)
    torque = magT.calcTorque(magf)
    torqueAR = np.array([torque[0], torque[1], torque[2]])
 
    
    omega = magT.controlSys(torqueAR, qtest)
    #aVel.setAngVar(10,10,10)
    print("ang var", aVel.getAngVar())
    print("torque", torqueAR)
    a =  aVel.getAngVar()[0]
    b =  aVel.getAngVar()[1]
    c =  aVel.getAngVar()[2]
    d =  aVel.getAngVar()[3]
    print("w", a)
    print("x", b)
    print("y", c)
    print("z", d) 

    tempAngVar = aVel.getAngVar()
    #quaternion = mathutils.Quaternion([tempAngVar[0], tempAngVar[1], tempAngVar[2], tempAngVar[3]])
    #euler = quaternion.to_euler('XYZ')
    with open('angVel.csv', mode='a+', newline='\n') as logs:
        writer = csv.writer(logs)
        writer.writerow([f'{tempAngVar[0]:.20f}',f'{tempAngVar[1]:.20f}',f'{tempAngVar[2]:.20f}',f'{tempAngVar[3]:.20f}'])
    
    with open('torque.csv', mode='a+', newline='\n') as logs:
        writer = csv.writer(logs)
        writer.writerow([f'{torqueAR[0]:.20f}', f'{torqueAR[1]:.20f}', f'{torqueAR[2]:.20f}'])
    
    #aVel.setAngVar(omega[0], omega[1], omega[2])

    #print("test", magT.convertDutyCycle(bpy.data.objects['cubesat'].get("magX")))
    x = x + 1

