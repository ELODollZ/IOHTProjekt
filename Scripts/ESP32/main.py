#!/usr/bin/env python3
# Author: NyboMønster

from machine import Pin, PWM
from DHT11Kode import measureFromDHT11
import _thread as Thread
from ConfigFileForESP32 import ListOfConfig as Conf
from ConfigFileForESP32 import RPIServerAddress, RPIPortNumber
import time
import urequests, ujson

prevTemp = None
prevHumi = None
prevOutputForServo = None
currentOutputForServo = None
OutputForServo = None
prevMSG = None
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
                    time.sleep(2)
                    OutputForServo = None
                elif (var2 == 0):
                    servo1.duty(30)
                    time.sleep(2)
                    servo1.duty(130)
                    OutputForServo = "Pile 2 sendt ud"
                    time.sleep(2)
                    OutputForServo = None
            except Exception as e:
                print(f"Exception caused error, in loop: {e}")
    except Exception as e:
        print(f"Exception caused error: {e}")
try:
    Thread.start_new_thread(ServoThreadTarget, (button1, button2, servo1, servo2))
except Exception as e:
    print(f"Error starting the thread for servo: {e}")

def SendingDataToRPI(DataArray):
    try:
        jsonDataArrayed = ujson.dumps({"Temp": DataArray[1], "Humidity": DataArray[3], "ServoOutput": DataArray[5]})
        print(jsonDataArrayed)
        RPIServerURL = f"http://{RPIServerAddress}:{RPIPortNumber}/ESP32Data"
        response = urequests.post(RPIServerURL, data=jsonDataArrayed)
        successCode = response.status_code
        print("HTTP Status code: ", successCode)
        response.close()
        return successCode
    except Exception as e:
        print("Error in sendingDataToRPI: ", e)
        return None
        

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
        currentOutputForServo = OutputForServo
        ArrayDataToSend = ["Temp: ", str(varTemp), "Humidity: ", str(varHumi), "ServoOutput: ",currentOutputForServo]
        try:
            #print("Should sent: ", ArrayDataToSend)
            if  (varTemp is not None or varHumi is not None or currentOutputForServo is not None) and (ArrayDataToSend != prevMSG or currentOutputForServo != prevOutputForServo):
                print("Data To Sent", ArrayDataToSend)
                SendingDataToRPI(ArrayDataToSend)
                #SendingDataToRPI(290102)
                prevMSG = ArrayDataToSend
                prevOutputForServo = currentOutputForServo
                
        except Exception as e:
            pass      
    except OSError as e:
        print(f"OsError in : {e}")
