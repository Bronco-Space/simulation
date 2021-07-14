from pyquaternion import Quaternion
import bpy
import mathutils as mat


class IMU:

    def __init__(self):
        # self._satQuat = bpy.data.objects["cubesat"].rotation_quaternion     # initial value needed for qCurrent
        # self._qCurrent = Quaternion(self._satQuat[0], self._satQuat[1], self._satQuat[2], self._satQuat[3]).normalised
        # self._angVarQuat = Quaternion(1,0,0,0)
        self.magnetic = ()
        self.gyro = ()
        self.acceleration = ()

    def UpdateGyro(self, newQuat):
        if type(newQuat) == type(self._qCurrent):
            self.gyro = tuple(newQuat.get_axis())
        else:
            print("IMU.UpdateGyro ERROR: parameter not of Quaternion type.")

    def UpdateAcc(self):
        self.acceleration = tuple(bpy.data.objects["cubesat"])

test_imu = IMU()