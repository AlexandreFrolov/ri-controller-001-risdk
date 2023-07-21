import sys
import time
from ctypes import *
import traceback
from ricontroller import RiController
from rirotateservo import RiRotateServo

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(True))
        print(f"Controller Model: {controller.model_name}")
        
        controller.init()
        ds04 = RiRotateServo(controller)

        ds04.add_custom_servo(1050, 2100, 1050, 2100, 0)
        ds04.stop_rservo()

        ds04.rotate_by_pulse(1050)
        time.sleep(3) 

        ds04.rotate_by_pulse(2100)
        time.sleep(3) 

        ds04.rotate_by_pulse(1570)
        time.sleep(3) 

        ds04.cleanup_servo()
        controller.cleanup()

    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)