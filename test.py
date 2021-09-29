import magnetorquer as mag
import angular_velocity_cs as aVel



x = 0
while x < 1:
    mag.controlSys(mag, aVel.qCurrent)
    
    x = x + 1
