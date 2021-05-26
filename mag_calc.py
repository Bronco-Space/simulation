import bpy
import math
import pyIGRF

def get_magnetic_force(location):
    # note this function requires that the earth be centered at the origin and oriented
    # so that geographic north and south are alligned with the z axis
    # altitude in this function is the distance from the earth's surface.
    # returns a vector in NED coordinate system with 3 components and 1 magnitude.
    
    x, y, z = location
    year = 2021
    earth_radius = 635.7 #* 10000 # m
    
    alt = math.sqrt(x**2 + y**2 + z**2) - earth_radius
    thetaE = math.acos(z/alt)
    psiE = math.atan2(y,x)
    lat = 90 - thetaE * 180 / math.pi
    lon = psiE * 180 / math.pi
    alt_km = alt / 1000
    
    md, mi, mh, mx, my, mz, mf = pyIGRF.igrf_value(lat,lon,alt,year)
    # md - declination (+ve east)
    # mi - inclination
    # mh - horizontal intensity
    # mx - north component (parallel to earth's surface in polar direction)
    # my - east component (east parallel to earth's surface along a latitude curve)
    # mz - down component (downward toward the Earth antiparallel to surface outward normal vector)
    # mf - total intensity (nT)
    
    magf = (mx, my, mz, mf)
    
    return magf

# This won't actually execute but I left if for posterity
if __name__ == '__main__':
    print()
    magf = get_magnetic_force(bpy.data.objects['cubesat'].location)
    
    print('North component:                 {:>+10.3f}'.format(magf[0]))
    print('East component:                  {:>+10.3f}'.format(magf[1]))
    print('Vertical component (+ve down):   {:>+10.3f}'.format(magf[2]))
    print('Total intensity:                 {:>+10.3f} nT'.format(magf[3]))