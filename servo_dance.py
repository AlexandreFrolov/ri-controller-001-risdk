import sys
import time
import traceback
from ctypes import *
from ricontroller import RiController
from rirotateservo import RiRotateServo
from riservo import RiServo
from riled import RiLed

def start_rotate_ds04_nfs(controller, port):
    ds04 = RiRotateServo(controller)
    ds04.add_custom_servo(1050, 2100, 1050, 2100, port)
    ds04.rotate_by_pulse(1050)
    time.sleep(3)
    ds04.rotate_by_pulse(2100)
    time.sleep(3)
    ds04.rotate_by_pulse(1570)
    time.sleep(0.3)
    ds04.cleanup_servo()

def start_mg90s(controller, port):
    mg90s = RiServo(controller)
    mg90s.add("mg90s", port)
    mg90s.set_middle()
    time.sleep(3) 
    mg90s.rotate(0, 200)
    time.sleep(3) 
    mg90s.rotate(1, 200)
    time.sleep(3) 
    mg90s.set_middle()
    time.sleep(0.3) 
    mg90s.cleanup_servo()

def start_sg90(controller, port):
    sg90 = RiServo(controller)
    sg90.add_custom_servo(2350, 365, 200, 180, port)
    sg90.set_middle()
    time.sleep(3) 
    sg90.rotate(0, 200)
    time.sleep(3) 
    sg90.rotate(1, 200)
    time.sleep(3) 
    sg90.set_middle()
    time.sleep(0.3) 
    sg90.cleanup_servo()

def led_pulse(controller):
    led = RiLed(controller)
    led.add(14, 15, 13)
    led.pulse(255, 0, 0, 1500)
    time.sleep(1) 
    led.pulse(0, 255, 0, 1500)
    time.sleep(1) 
    led.pulse(0, 0, 255, 1500)
    time.sleep(1) 
    led.stop()
    led.cleanup()    

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(True))
        print(f"Controller Model: {controller.model_name}")
        controller.init()

        start_rotate_ds04_nfs(controller, 0)
        start_mg90s(controller, 1)
        start_sg90(controller, 4)
        start_sg90(controller, 8)
        led_pulse(controller)

        controller.cleanup()
    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)
