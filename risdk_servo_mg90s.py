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

def servo_add(lib, pwm, servo, servo_type, channel):
    lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
    lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "servodrive".encode(), servo_type.encode(), servo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_CreateModelComponent failed with error code {errCode}: {err_msg(errTextC)}")

    errCode = lib.RI_SDK_LinkServodriveToController(servo, pwm, channel, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_LinkServodriveToController failed with error code {errCode}: {err_msg(errTextC)}")   

def add_custom_servo(lib, pwm, servo, MaxDt, MinDt, MaxSpeed, RangeAngle, channel):
    lib.RI_SDK_CreateDeviceComponent.argtypes = [c_char_p, c_char_p,  POINTER(c_int), c_char_p]
    lib.RI_SDK_exec_ServoDrive_CustomDeviceInit.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
    lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]

    servo = c_int()
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_CreateDeviceComponent("executor".encode(), "servodrive".encode(),  servo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_CreateDeviceComponent failed with error code {errCode}: {err_msg(errTextC)}")

    errCode = lib.RI_SDK_exec_ServoDrive_CustomDeviceInit(servo, MaxDt, MinDt, MaxSpeed, RangeAngle, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_CustomDeviceInit failed with error code {errCode}: {err_msg(errTextC)}")

    errCode = lib.RI_SDK_LinkServodriveToController(servo, pwm, channel, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_LinkServodriveToController failed with error code {errCode}: {err_msg(errTextC)}")     

    servo = servo
    return(servo)

def servo_rotate(lib, servo, direction, speed, async_mode):
    lib.RI_SDK_exec_ServoDrive_Rotate.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_Rotate(servo, direction, speed, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_Rotate failed with error code {errCode}: {err_msg(errTextC)}")

def servo_rotate_min_step(lib, servo, direction, speed, async_mode):
    lib.RI_SDK_exec_ServoDrive_MinStepRotate.argtypes = [c_int, c_int, c_int, c_bool, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_MinStepRotate(servo, direction, speed, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_MinStepRotate failed with error code {errCode}: {err_msg(errTextC)}")

def servo_set_middle(lib, servo):
    lib.RI_SDK_exec_ServoDrive_SetPositionToMidWorkingRange.argtypes = [c_int, c_char_p]

    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_SetPositionToMidWorkingRange(servo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_Rotate failed with error code {errCode}: {err_msg(errTextC)}")

def servo_turn_by_pulse(lib, servo, dt):
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_TurnByPulse(servo, dt, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_TurnByPulse failed with error code {errCode}: {err_msg(errTextC)}")

def servo_turn_by_angle(lib, servo, angle, speed, async_mode):
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_Turn(servo, angle, speed, async_mode, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_Turn failed with error code {errCode}: {err_msg(errTextC)}")

def servo_turn_by_duty(lib, servo, steps):
    lib.RI_SDK_exec_ServoDrive_TurnByDutyCycle.argtypes = [c_int, c_int, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_TurnByDutyCycle(servo, steps, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_TurnByDutyCycle failed with error code {errCode}: {err_msg(errTextC)}")

def servo_get_angle(lib, servo):
    lib.RI_SDK_exec_ServoDrive_GetCurrentAngle.argtypes = [c_int, POINTER(c_int), c_char_p]
    angle = c_int()
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_exec_ServoDrive_GetCurrentAngle(servo, angle, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_GetCurrentAngle failed with error code {errCode}: {err_msg(errTextC)}")
    return(angle.value) 

def servo_get_state(lib, servo):
    lib.RI_SDK_exec_ServoDrive_GetState.argtypes = [c_int, POINTER(c_int), c_char_p]
    errTextC = create_string_buffer(1000)
    state = c_int()
    errCode = lib.RI_SDK_exec_ServoDrive_GetState(servo, state, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_exec_ServoDrive_GetState failed with error code {errCode}: {err_msg(errTextC)}")
    return state

def cleanup_servo(lib, servo):
    lib.RI_SDK_DestroyComponent.argtypes = [c_int, c_char_p]
    errTextC = create_string_buffer(1000)
    errCode = lib.RI_SDK_DestroyComponent(servo, errTextC)
    if errCode != 0:
        raise Exception(f"RI_SDK_DestroyComponent failed with error code {errCode}: {err_msg(errTextC)}")


def print_servo_state(lib, servo):
    print(f"Servo state: : {str(servo_get_state(lib, servo).value)}")

if __name__ == "__main__":
    try:
        i2c = c_int()
        pwm = c_int()
        mg90s = c_int()

        lib = init(i2c, pwm)

        servo_add(lib, pwm, mg90s, "mg90s", 0)
        print_servo_state(lib, mg90s)

        print("\nMG90S поворот в крайние положения")

        servo_rotate(lib, mg90s, 0, 200, False)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))
        print_servo_state(lib, mg90s)

        servo_rotate(lib, mg90s, 1, 200, False)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_set_middle(lib, mg90s)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))


        print("\nMG90S управление через длительность импульсов")

        servo_turn_by_pulse(lib, mg90s, 2650)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_turn_by_pulse(lib, mg90s, 365)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))
        
        servo_turn_by_pulse(lib, mg90s,1500)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))
        

        print("\nMG90S Минимальный шаг")

        servo_set_middle(lib, mg90s)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_rotate_min_step(lib, mg90s, 1, 100, False)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_rotate_min_step(lib, mg90s, 0, 100, False)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        print("\nMG90S управление через Duty")

        servo_turn_by_duty(lib, mg90s, 75)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_turn_by_duty(lib, mg90s, 300)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_turn_by_duty(lib, mg90s, 540)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))
     
        print("\nMG90S поворот на заданный угол")

        servo_set_middle(lib, mg90s)
        time.sleep(2) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_turn_by_angle(lib, mg90s, 90, 200, False)
        time.sleep(1) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        servo_turn_by_angle(lib, mg90s, -90, 300, False)
        time.sleep(1) 
        print("mg90s angle: " + str(servo_get_angle(lib, mg90s)))

        cleanup_servo(lib, mg90s)
        cleanup(lib)
    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)
 