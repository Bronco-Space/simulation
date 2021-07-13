from pyquaternion import Quaternion
import bpy
import mathutils as mat


class IMU:

    def __init__(self):
        self._satQuat = bpy.data.objects["cubesat"].rotation_quaternion     # initial value needed for qCurrent
        self._qCurrent = Quaternion(self._satQuat[0], self._satQuat[1], self._satQuat[2], self._satQuat[3]).normalised
        self._angVarQuat = Quaternion(1,0,0,0)
        self.magnetic = ()
        self.gyro = ()
        self.acceleration = ()

    def UpdateQuat(self, newQuat):
        if type(newQuat) == type(self._qCurrent):
            self._angVarQuat = newQuat
        else:
            print("IMU.UpdateQuat ERROR: parameter not of Quaternion type.")

test_imu = IMU()