#!/usr/bin/env python3
# Author: NyboMønster

from DHT11Kode import measureFromDHT11
import _thread as Thread
from PilleServoKode import ServoFunc
from ConfigFileForESP32 import ListOfConfig as Conf
import time

def ServoThreadTarget():
    global OutputForServo
    while True:
        try:
            OutputForServo = ServoFunc(Conf)
            time.sleep(1)
            return OutputForServo
        except:
            print("Failed to get Pin's mostlikely for Buttons and Servo")
Thread.start_new_thread(ServoThreadTarget, ())

while True:
    try:
        varTemp, varHumi = measureFromDHT11()
        print("Temp is:", varTemp, "Humi is:", varHumi)
        time.sleep(1)
        
    except OSError as e:
        print(f"OsError in : {e}")
