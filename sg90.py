
import sys
import time
from ctypes import *
import traceback
from ricontroller import RiController
from riservo import RiServo

if __name__ == "__main__":
    try:
        controller = RiController(c_bool(False))
        print(f"Controller Model: {controller.model_name}")
        
        controller.init()

        sg90 = RiServo(controller)

        sg90.add_custom_servo(2350, 365, 200, 180, 0)

        print("\nSG90 поворот в крайние положения")

        sg90.rotate(0, 200)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.rotate(1, 200)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.set_middle()
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))


        print("\nSG90 управление через длительность импульсов")

        sg90.turn_by_pulse(2350)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.turn_by_pulse(365)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))
        
        sg90.turn_by_pulse(1500)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))
        

        print("\nSG90 Минимальный шаг")

        sg90.set_middle()
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))


        sg90.rotate_min_step(1, 100)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.rotate_min_step(0, 100)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        print("\nSG90 управление через Duty")

        sg90.turn_by_duty(75)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.turn_by_duty(278)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.turn_by_duty(481)
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))
     
        print("\nSG90 поворот на заданный угол")

        sg90.set_middle()
        time.sleep(2) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.turn_by_angle(90, 200)
        time.sleep(1) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.turn_by_angle(-90, 200)
        time.sleep(1) 
        print("sg90 angle: " + str(sg90.get_angle()))

        sg90.cleanup_servo()
        controller.cleanup()

    except Exception as e:
        print(traceback.format_exc() + "===> ", str(e))
        sys.exit(2)
