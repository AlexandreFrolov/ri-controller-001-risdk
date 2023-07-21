import sys
import time
import platform
from ctypes import *

class RiServo:
    def __init__(self, controller):
        self.controller = controller
        self.errTextC = create_string_buffer(1000)
        self.state = c_int()
        self.servo = c_int()

    def err_msg(self):
        return(self.errTextC.raw.decode())

    def add(self, servo_type, channel):
        self.controller.lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
        self.controller.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        errCode = self.controller.lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), servo_type.encode(), self.servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {self.err_msg()}")

        errCode = self.controller.lib.RI_SDK_LinkServodriveToController(self.servo, self.controller.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.err_msg()}")   

    def add_custom_servo(self, MaxDt, MinDt, MaxSpeed, RangeAngle, channel):
        self.controller.lib.RI_SDK_CreateDeviceComponent.argtypes = [c_char_p, c_char_p,  POINTER(c_int), c_char_p]
        self.controller.lib.RI_SDK_exec_ServoDrive_CustomDeviceInit.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
        self.controller.lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

        servo = c_int()
        errCode = self.controller.lib.RI_SDK_CreateDeviceComponent("executor".encode(), "servodrive".encode(),  servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_CreateDeviceComponent failed with error code {errCode}: {self.err_msg()}")

        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_CustomDeviceInit(servo, MaxDt, MinDt, MaxSpeed, RangeAngle, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_CustomDeviceInit failed with error code {errCode}: {self.err_msg()}")

        errCode = self.controller.lib.RI_SDK_LinkServodriveToController(servo, self.controller.pwm, channel, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_LinkServodriveToController failed with error code {errCode}: {self.err_msg()}")     

        self.servo = servo
        return(servo)

    def rotate(self, direction, speed):
        self.controller.lib.RI_SDK_exec_ServoDrive_Rotate.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]

        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_Rotate(self.servo, direction, speed, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_Rotate failed with error code {errCode}: {self.err_msg()}")

    def rotate_min_step(self, direction, speed):
        self.controller.lib.RI_SDK_exec_ServoDrive_MinStepRotate.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]

        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_MinStepRotate(self.servo, direction, speed, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_MinStepRotate failed with error code {errCode}: {self.err_msg()}")

    def set_middle(self):
        self.controller.lib.RI_SDK_exec_ServoDrive_SetPositionToMidWorkingRange.argtypes = [c_int, c_char_p]

        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_SetPositionToMidWorkingRange(self.servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_Rotate failed with error code {errCode}: {self.err_msg()}")

    def turn_by_pulse(self, dt):
        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_TurnByPulse(self.servo, dt, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_TurnByPulse failed with error code {errCode}: {self.err_msg()}")

    def turn_by_angle(self, angle, speed):
        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_Turn(self.servo, angle, speed, self.controller.is_async, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_Turn failed with error code {errCode}: {self.err_msg()}")

    def turn_by_duty(self, steps):
        self.controller.lib.RI_SDK_exec_ServoDrive_TurnByDutyCycle.argtypes = [c_int, c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_TurnByDutyCycle(self.servo, steps, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_TurnByDutyCycle failed with error code {errCode}: {self.err_msg()}")

    def get_angle(self):
        self.controller.lib.RI_SDK_exec_ServoDrive_GetCurrentAngle.argtypes = [c_int, POINTER(c_int), c_char_p]
        angle = c_int()
        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_GetCurrentAngle(self.servo, angle, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_GetCurrentAngle failed with error code {errCode}: {self.err_msg()}")
        return(angle.value) 

    def get_state(self):
        self.controller.lib.RI_SDK_exec_ServoDrive_GetState.argtypes = [c_int, POINTER(c_int), c_char_p]
        errCode = self.controller.lib.RI_SDK_exec_ServoDrive_GetState(self.servo, self.state, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_exec_ServoDrive_GetState failed with error code {errCode}: {self.err_msg()}")
        return self.state

    def cleanup_servo(self):
        self.controller.lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
        errCode = self.controller.lib.RI_SDK_DestroyComponent(self.servo, self.errTextC)
        if errCode != 0:
            raise Exception(f"RI_SDK_DestroyComponent failed with error code {errCode}: {self.err_msg()}")


