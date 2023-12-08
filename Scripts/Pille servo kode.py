from machine import Pin, PWM
from time import sleep
button1 = Pin(34, Pin.IN)
button2 = Pin(35, Pin.IN)
servo1 = PWM(Pin(27), freq=50)
servo2 = PWM(Pin(26), freq=50)
while True:
    sleep(0.1)
    var1 = button1.value()
    var2 = button2.value()
    if (var1 == 0):
        servo2.duty(30)
        sleep(2)
        servo2.duty(130)
        print("Ipren")
    elif (var2 == 0):
        servo1.duty(30)
        sleep(2)
        servo1.duty(130)
        print("Panodil")
