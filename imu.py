from pyquaternion import Quaternion
import bpy
import mathutils as mat
import math
import pyIGRF


class IMU:

    def __init__(self):
        # self._satQuat = bpy.data.objects["cubesat"].rotation_quaternion     # initial value needed for qCurrent
        # self._qCurrent = Quaternion(self._satQuat[0], self._satQuat[1], self._satQuat[2], self._satQuat[3]).normalised
        # self._angVarQuat = Quaternion(1,0,0,0)
        self.magnetic = ()
        self.gyro = ()
        self.acceleration = ()


    def Update(self, newQuat):
        # self.UpdateMag()
        self.UpdateGyro(newQuat)
        self.UpdateAcc()
        self.DisplayValues()


    def UpdateGyro(self, newQuat):
        if type(newQuat) == type(Quaternion(1,0,0,0)):
            self.gyro = tuple(newQuat.get_axis())
        else:
            print("IMU.UpdateGyro ERROR: parameter not of Quaternion type.")


    def UpdateAcc(self):
        # comibantion of gravity_calc and new code

        sat_loc = bpy.data.objects["cubesat"].location  # don't need to scale because I'm gonna use a unit vector in the direction from the sat to the earth.
        # earth_loc = bpy.data.objects["EarthSurface"].location


        # # calculate vector for earth's gravity acting on the sat
        # grav_vec = [earth_loc[0] - sat_loc[0], earth_loc[1] - sat_loc[1], earth_loc[2] - sat_loc[2]]
        # grav_vec_mag = sqrt(grav_vec[0]**2 + grav_vec[1]**2 + grav_vec[2]**2)
        # unit_grav_vec = [x / grav_vec_mag for x in grav_vec]

        cube = sat_loc * 10000
        cubeR = math.sqrt((cube[0]**2) + (cube[1]**2) + (cube[2]**2)) #in m
        
        earthDim = (bpy.data.objects["EarthSurface"].dimensions * 10000)
        earthR = earthDim[0]/2
        dens = 5515 #kg/m^3
        volE = (4/3)*(3.14159)* (earthR)**3 #m^3
        massE = dens * volE #kg
        unitVectR = cube / cubeR
        gravC = (6.67408 * 10**(-11))
            
        self.acceleration = -((gravC * massE) / (cubeR ** 2))* unitVectR #meters/s^2
    

    def UpdateMag(self):
        # note this function requires that the earth be centered at the origin and oriented
        # so that geographic north and south are alligned with the z axis
        # altitude in this function is the distance from the earth's surface.
        # returns a vector in NED coordinate system with 3 components and 1 magnitude.

        location = bpy.data.objects['cubesat'].location
        x, y, z = location
        year = 2021
        earth_radius = 635.7  # * 10000 # m

        alt = math.sqrt(x**2 + y**2 + z**2) - earth_radius
        thetaE = math.acos(z/alt)
        psiE = math.atan2(y, x)
        lat = 90 - thetaE * 180 / math.pi
        lon = psiE * 180 / math.pi
        # alt_km = alt / 1000

        md, mi, mh, mx, my, mz, mf = pyIGRF.igrf_value(lat, lon, alt, year)
        # md - declination (+ve east)
        # mi - inclination
        # mh - horizontal intensity
        # mx - north component (parallel to earth's surface in polar direction)
        # my - east component (east parallel to earth's surface along a latitude curve)
        # mz - down component (downward toward the Earth antiparallel to surface outward normal vector)
        # mf - total intensity (nT)

        self.magnetic = (mx, my, mz)


    def DisplayValues(self):
        print("=== SAT IMU VALUES ===")
        print(" magnetic = ", self.magnetic)
        print(" gyro = ", self.gyro)
        print(" acceleration = ", self.acceleration, "\n")

        

test_imu = IMU()
