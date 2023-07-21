
import sys
from ctypes import *

# Подключаем внешнюю библиотеку для работы с SDK
lib = cdll.LoadLibrary("C:\Windows\system32\librisdk.dll")


# Указываем типы аргументов для функций библиотеки RI_SDK
lib.RI_SDK_InitSDK.argtypes = [c_int, c_char_p]
lib.RI_SDK_CreateModelComponent.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_int), c_char_p]
lib.RI_SDK_LinkPWMToController.argtypes = [c_int, c_int, c_uint8, c_char_p]
lib.RI_SDK_LinkLedToController.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p]
lib.RI_SDK_DestroySDK.argtypes = [c_bool, c_char_p]
lib.RI_SDK_exec_RGB_LED_SinglePulse.argtypes = [c_int, c_int, c_int, c_int, c_int, c_bool, c_char_p]

def main():
    errTextC = create_string_buffer(1000)  # Текст ошибки. C type: char*
    i2c = c_int()
    pwm = c_int()
    led = c_int()

    # Инициализация библиотеки RI SDK с уровнем логирования 3
    errCode = lib.RI_SDK_InitSDK(3, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    # Создание компонента i2c адаптера модели ch341
    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "i2c_adapter".encode(), "ch341".encode(), i2c, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    print("i2c: ", i2c.value)

    # Создание компонента ШИМ модели pca9685
    errCode = lib.RI_SDK_CreateModelComponent("connector".encode(), "pwm".encode(), "pca9685".encode(), pwm, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    print("pwm: ", pwm.value)

     # Создание компонента светодиода модели ky016
    errCode = lib.RI_SDK_CreateModelComponent("executor".encode(), "led".encode(), "ky016".encode(), led, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    print("led: ", led.value)

    # Связывание i2c с ШИМ
    errCode = lib.RI_SDK_LinkPWMToController(pwm, i2c, 0x40, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)
    
    # Связывание ШИМ со светодиодом
    errCode = lib.RI_SDK_LinkLedToController(led, pwm, 15, 14, 13, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    # Непрерывное свечение светодиода красным цветом в течение 10 секунд.
    # Яркость красного цвета - 150. Яркость остальных цветов - 0.
    errCode = lib.RI_SDK_exec_RGB_LED_SinglePulse(led, 150, 0, 0, 10000, False, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2) 

    # Удаление библиотеки со всеми компонентами
    errCode = lib.RI_SDK_DestroySDK(True, errTextC)
    if errCode != 0:
        print(errCode, errTextC.raw.decode())
        sys.exit(2)

    print("Success")

main()

 
 
 
 