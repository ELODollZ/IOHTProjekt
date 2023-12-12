#!/usr/bin/env python3
#Arthor: Emil

from machine import Pin, PWM
from time import sleep
from ConfigFileForESP32 import ListOfConfig as Conf

def ServoFunc(Conf):
    button1 = Pin(Conf[1], Pin.IN)
    button2 = Pin(Conf[2], Pin.IN)
    servo_motor1 = PWM(Pin(Conf[3]), freq=50)
    servo_motor2 = PWM(Pin(Conf[4]), freq=50)
    while True:
        sleep(0.2)
        var1 = button1.value()
        var2 = button2.value()
        if (var1 == 0):
            servo2.duty(30)
            sleep(2)
            servo2.duty(130)
            print("Pile 1 sendt ud")
        elif (var2 == 0):
            servo1.duty(30)
            sleep(2)
            servo1.duty(130)
            print("Pile 2 sendt ud")

