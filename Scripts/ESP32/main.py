#!/usr/bin/env python3
# Author: NyboMønster

from DHT11Kode import measureFromDHT11
import _thread as Thread
from PilleServoKode import ServoFunc
from ConfigFileForESP32 import ListOfConfig as Conf

def ServoThreadTarget():
    global OutputForServo
    OutputForServo = ServoFunc(Conf)
    return OutputForServo

ThreadServo = Thread.start_new_thread(ServoThreadTarget, ())
ThreadServo.start()

while True:
    try:
        varTemp, varHumi = measureFromDHT11()
        print("Temp is:", varTemp, "Humi is:", varHumi)
        
    except OSError as e:
        print(f"OsError in : {e}")


