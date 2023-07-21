import sys
import time
from ctypes import *
import traceback
from ricontroller import RiController
from rirotateservo import RiRotateServo

def print_rservo_state(rservo):
    print(f"RServo state: : {str(rservo.get_state().value)}")

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(False))
        print(f"Controller Model: {controller.model_name}")
        
        controller.init()
        rservo = RiRotateServo(controller)
        rservo.add("mg996r", 0)

        print_rservo_state(rservo)

        print(1050)
        rservo.rotate_by_pulse_over_time(1050, 2000)
        print_rservo_state(rservo)
        time.sleep(3) 

        print(2100)
        rservo.rotate_by_pulse_over_time(2100, 2000)
        print_rservo_state(rservo)
        time.sleep(3) 

        print(1570)
        rservo.rotate_by_pulse_over_time(1570, 2000)
        print_rservo_state(rservo)
        time.sleep(3) 

        rservo.rotate_at_speed_over_time(0, 50, 2000)
        time.sleep(3) 
        rservo.rotate_at_speed_over_time(1, 100, 2000)
        time.sleep(3) 

        rservo.stop_rservo()
        print_rservo_state(rservo)

        rservo.cleanup_servo()
        controller.cleanup()

    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)