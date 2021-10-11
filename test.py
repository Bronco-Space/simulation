import magnetorquer as magT
import mag_calc as mag
import angular_velocity_cs as aVel
import bpy
import csv
import numpy as np
import pyquaternion as q


qtest = q.Quaternion(0.9885986, 0.0869346, 0.0869346, 0.0869346)

x = 0
while x < 1:
   
    print(qtest)
    aVel.setAngVar(qtest) #does this need to be quaternion?
    magf = mag.get_magnetic_force(bpy.data.objects['cubesat'].location)
    torque = magT.calcTorque(magf)
    torqueAR = np.array([torque[0], torque[1], torque[2]])
    
    
    omega = magT.velCtrl(torqueAR)
    #aVel.setAngVar(10,10,10)
    #print(aVel.getAngVar())
    print("uWu", torque)
    print("OwO", omega)
    

#    print("UwU", torque)

    with open('output.csv', mode='w', newline='') as logs:
        logs = csv.writer(logs, delimiter=',')
        logs.writerows('1,2,3')
    #aVel.setAngVar(omega[0], omega[1], omega[2])
    #print("oop", torque)
    #print("test", magT.convertDutyCycle(bpy.data.objects['cubesat'].get("magX")))
    x = x + 1
