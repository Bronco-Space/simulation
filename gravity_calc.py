import bpy
from math import sqrt

#gravitational force vector between Earth and Cubesat

def gravForce():
    
    cube = bpy.data.objects["cubesat"].location
    cubeR = sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2)) #in m
    massC = 1.75 # in kg
    
    
    earthDim = bpy.data.objects["EarthSurface"].dimensions
    earthR = earthDim[1]/2
    dens = 5515 #kg/m^3
    volE = (4/3)*(3.14159)* (earthR)**3 #m^3
    massE = dens * volE #kg
    

    gravC = (6.67408 * 10**(-11))
    unitVectR = cube / cubeR
    
    force = -((gravC * massE *massC) / (cubeR**2)) * unitVectR * (10**6) #micronewtons
    
    return force

#gravitational acceleration experienced by satellite
def gravAccel():
    
    cube = bpy.data.objects["cubesat"].location
    cubeR = sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2)) #in m
    

    earthDim = bpy.data.objects["EarthSurface"].dimensions
    earthR = earthDim[1]/2
    dens = 5515 #kg/m^3
    volE = (4/3)*(3.14159)* (earthR)**3 #m^3
    massE = dens * volE #kg
    gravE = ((6.67408 * 10**(-11)) * massE) / (earthR**2)
    
    unitVectR = cube / cubeR
    accel = -(gravE * (earthR**2) / (cubeR ** 2))* unitVectR * 10**6 #micrometers/s^2
    return accel
