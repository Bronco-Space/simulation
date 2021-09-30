import magnetorquer as mag
import angular_velocity_cs as aVel


testDutyCycle = 1
x = 0
while x < 1:
    mag.controlSys(mag, aVel.qCurrent)
    
    x = x + 1
