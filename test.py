import magnetorquer as magT
import mag_calc as mag
import angular_velocity_cs as aVel
import bpy

testDutyCycle = 1

x = 0
while x < 1:
    
    magf = mag.get_magnetic_force(bpy.data.objects['cubesat'].location)
    torque = magT.calcTorque(magf)
    magT.controlSys(torque, aVel.qCurrent)
    
    x = x + 1
