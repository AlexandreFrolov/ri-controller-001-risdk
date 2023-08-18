import sys
from ctypes import *
import time
import platform
import traceback

def err_msg(errTextC):
    return(errTextC.raw.decode())

def init(i2c, pwm):
    platform_os = platform.system()
    try:
        if platform_os == "Windows":
            lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")
        if platform_os == "Linux":
            lib = cdll.LoadLibrary("/usr/local/robointellect_sdk/ri_sdk/librisdk.so")
    except OSError as e:
        raise Exception("Failed to load: " + str(e))

    lib.RI_SDK_InitSDK.argtypes = [c_int, c_char_p]
    lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
    lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_InitSDK(3, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_InitSDK failed with error code {errCode}: {err_msg(errTextC)}")        

    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), i2c, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {err_msg(errTextC)}")        

    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), pwm, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {err_msg(errTextC)}")        

    errCode = lib.RI_SDK_LinkPWMToController(pwm, i2c, 0x40, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_LinkPWMToController failed with error code {errCode}: {err_msg(errTextC)}")        

    return lib
    
def cleanup(lib):
    lib.RI_SDK_DestroySDK.argtypes = [c_bool, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_DestroySDK(True, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_DestroySDK failed with error code {errCode}: {err_msg(errTextC)}")        

def rservo_add(lib, pwm, servo, servo_type, channel):
    lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
    lib.RI_SDK_LinkRServodriveToController.argtypes = [c_int, c_int, c_int, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), servo_type.encode(), servo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {err_msg(errTextC)}")

    errCode = lib.RI_SDK_LinkRServodriveToController(servo, pwm, channel, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_LinkRServodriveToController failed with error code {errCode}: {err_msg(errTextC)}")   

def add_custom_rservo(lib, pwm, min_pulse, max_pulse, minPulseCounterClockwise, maxPulseCounterClockwise, channel):
    lib.RI_SDK_CreateDeviceComponent.argtypes = [c_char_p, c_char_p,  POINTER(c_int), c_char_p]
    lib.RI_SDK_exec_RServoDrive_CustomDeviceInit.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
    lib.RI_SDK_LinkRServodriveToController.argtypes = [c_int, c_int, c_int, c_char_p]

    rservo = c_int()
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_CreateDeviceComponent("executor".encode(), "servodrive_rotate".encode(), rservo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_CreateDeviceComponent failed with error code {errCode}: {err_msg(errTextC)}")

    errCode = lib.RI_SDK_exec_RServoDrive_CustomDeviceInit(rservo, min_pulse, max_pulse, minPulseCounterClockwise, maxPulseCounterClockwise, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_CustomDeviceInit failed with error code {errCode}: {err_msg(errTextC)}")

    errCode = lib.RI_SDK_LinkRServodriveToController(rservo, pwm, channel, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_LinkRServodriveToController failed with error code {errCode}: {err_msg(errTextC)}")     

    return(rservo)


def rservo_rotate_by_pulse(lib, rservo, dt, async_mode):
    lib.RI_SDK_exec_RServoDrive_RotateByPulse.argtypes = [c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RServoDrive_RotateByPulse(rservo, dt, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_RotateByPulse failed with error code {errCode}: {err_msg(errTextC)}")

def rservo_rotate_by_pulse_over_time(lib, rservo, dt, timeout, async_mode):
    lib.RI_SDK_exec_RServoDrive_RotateByPulseOverTime.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RServoDrive_RotateByPulseOverTime(rservo, dt, timeout, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_RotateByPulseOverTime failed with error code {errCode}: {err_msg(errTextC)}")

def rservo_rotate_at_speed(lib, rservo, direction, speed, async_mode):
    lib.RI_SDK_exec_RServoDrive_RotateWithRelativeSpeed.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RServoDrive_RotateWithRelativeSpeed(rservo, direction, speed, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_RotateWithRelativeSpeed failed with error code {errCode}: {err_msg(errTextC)}")

def rservo_rotate_at_speed_over_time(lib, rservo, direction, speed, timeout, async_mode):
    lib.RI_SDK_exec_RServoDrive_RotateWithRelativeSpeedOverTime.argtypes = [c_int, c_int, c_int, c_int, c_bool, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RServoDrive_RotateWithRelativeSpeedOverTime(rservo, direction, speed, timeout, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_RotateWithRelativeSpeedOverTime failed with error code {errCode}: {err_msg(errTextC)}")

def stop_rservo(lib, rservo):
    lib.RI_SDK_exec_RServoDrive_Stop.argtypes = [c_int, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RServoDrive_Stop(rservo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_Stop failed with error code {errCode}: {err_msg(errTextC)}")

def rservo_get_state(lib, rservo):
    lib.RI_SDK_exec_RServoDrive_GetState.argtypes = [c_int, POINTER(c_int), c_char_p]
    errTextC = create_string_buffer(1000)
    state = c_int()
    errCode = lib.RI_SDK_exec_RServoDrive_GetState(rservo, state, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_GetState failed with error code {errCode}: {err_msg(errTextC)}")
    return state

def stop_rservo(lib, rservo):
    lib.RI_SDK_exec_RServoDrive_Stop.argtypes = [c_int, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_RServoDrive_Stop(rservo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_RServoDrive_Stop failed with error code {errCode}: {err_msg(errTextC)}")

def cleanup_servo(lib, servo):
    lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_DestroyComponent(servo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_DestroyComponent failed with error code {errCode}: {err_msg(errTextC)}")

def print_rservo_state(lib, servo):
    print(f"Servo state: : {str(rservo_get_state(lib, servo).value)}")


if __name__ == "__main__":
    try:
        i2c = c_int()
        pwm = c_int()
        mg996r = c_int()

        lib = init(i2c, pwm)

        rservo_add(lib, pwm, mg996r,"mg996r", 0)
        print_rservo_state(lib, mg996r)

        rservo_rotate_by_pulse(lib, mg996r, 1050, True)
        print_rservo_state(lib, mg996r)
        time.sleep(3) 

        rservo_rotate_by_pulse(lib, mg996r, 2100, True)
        print_rservo_state(lib, mg996r)
        time.sleep(3) 

        rservo_rotate_by_pulse(lib, mg996r, 1570, True)
        print_rservo_state(lib, mg996r)
        time.sleep(3) 

        rservo_rotate_at_speed(lib, mg996r, 0, 50, True)
        time.sleep(3) 
        rservo_rotate_at_speed(lib, mg996r, 1, 100, True)
        time.sleep(3) 

        stop_rservo(lib, mg996r)
        print_rservo_state(lib, mg996r)

        cleanup_servo(lib, mg996r)
        cleanup(lib)
    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)
 