import magnetorquer as magT
import mag_calc as mag
import angular_velocity_cs as aVel
import bpy

testDutyCycle = 1

x = 0
while x < 1:
    
    magf = mag.get_magnetic_force(bpy.data.objects['cubesat'].location)
    torque = magT.calcTorque(magf)
    #omega = magT.controlSys(torque, aVel.getAngVar)
    aVel.setAngVar(10,10,10)
    print(aVel.getAngVar())
    
    print("UwU", torque)
    #aVel.setAngVar(omega[0], omega[1], omega[2])
    #print("oop", torque)
    #print("test", magT.convertDutyCycle(bpy.data.objects['cubesat'].get("magX")))
    x = x + 1
