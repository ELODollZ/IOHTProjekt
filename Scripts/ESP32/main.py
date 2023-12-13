#!/usr/bin/env python3
# Author: NyboMønster

from machine import Pin, PWM
from DHT11Kode import measureFromDHT11
import _thread as Thread
from ConfigFileForESP32 import ListOfConfig as Conf
from ConfigFileForESP32 import RPIServerAddress, RPIPortNumber
import time
import urequests, ujson


OutputForServo = None
prevTemp = None
prevHumi = None
button1 = Pin(Conf[1], Pin.IN)
button2 = Pin(Conf[2], Pin.IN)
servo1 = PWM(Pin(Conf[3]), freq=50)
servo2 = PWM(Pin(Conf[4]), freq=50)

#Arthor: Emil
def ServoThreadTarget(button1, button2, servo1, servo2):
    global OutputForServo
    try:
        while True:
            try:
                time.sleep(0.2)
                var1 = button1.value()
                var2 = button2.value()
                if (var1 == 0):
                    servo2.duty(30)
                    time.sleep(2)
                    servo2.duty(130)
                    OutputForServo = "Pile 1 sendt ud"
                elif (var2 == 0):
                    servo1.duty(30)
                    time.sleep(2)
                    servo1.duty(130)
                    OutputForServo = "Pile 2 sendt ud"
            except Exception as e:
                print(f"Exception in thread loop: {e}")
    except Exception as e:
        print(f"Exception in thread: {e}")
try:
    Thread.start_new_thread(ServoThreadTarget, (button1, button2, servo1, servo2))
except Exception as e:
    print(f"Error starting the thread for servo: {e}")

def SendingDataToRPI(DataArray):
    jsonDataArrayed = ujson.dumps({"data": DataArray})
    RPIServerURL = f"http://{RPIServerAddress}:{RPIPortNumber}/endpoint"
    response = urequests.post(RPIServerURL, data=jsonDataArrayed)
    response.close()

def GetDHT11():
    global prevTemp, prevHumi
    try:
        varTemp, varHumi = measureFromDHT11()
        #print("currentTemp: ", varTemp, "previousTemp: ", prevTemp, "currentHumi: ", varHumi, "previousHumi: ", prevHumi)
        if varTemp is not None and varHumi is not None:
            if varTemp != prevTemp or varHumi != prevHumi:
                prevTemp = varTemp
                prevHumi = varHumi
                return varTemp, varHumi
    except Exception as e:
        pass
    return None, None

while True:
    try:
        varTemp, varHumi = GetDHT11()
        ArrayDataToSend = ["Temp: ", str(varTemp), "Humidity: ", str(varHumi), OutputForServo]
        print(ArrayDataToSend)
        SendingDataToRPI(ArrayDataToSend)
        time.sleep(2)
        
    except OSError as e:
        print(f"OsError in : {e}")
 