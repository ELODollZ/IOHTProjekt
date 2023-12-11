#!/usr/bin/env python3
#Arthor: Emil

from machine import Pin, PWM
from time import sleep

def ServoFunc(Conf):
    button1 = Conf[1]
    button2 = Conf[2]
    servo1 = Conf[3]
    servo2 = Conf[4]
    while True:
        sleep(0.2)
        var1 = button1.value()
        var2 = button2.value()
        if (var1 == 0):
            servo2.duty(30)
            sleep(2)
            servo2.duty(130)
        elif (var2 == 0):
            servo1.duty(30)
            sleep(2)
            servo1.duty(130)

