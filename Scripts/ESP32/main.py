#!/usr/bin/env python3
# Author: NyboMønster

from DHT11Kode import measureFromDHT11
import _thread as Thread
from PilleServoKode import ServoFunc
from ConfigFileForESP32 import ListOfConfig as Conf
import time
import urequests, ujson

def ServoThreadTarget():
    global OutputForServo
    try:
        OutputForServo = ServoFunc(Conf)
        time.sleep(1)
        return OutputForServo
    except:
        pass
Thread.start_new_thread(ServoThreadTarget, ())

def SendingDataToRPI(DataArray):
    jsonDataArrayed = ujson.dumps({"data": DataArray})
    RPIServerURL = f"http://{Conf.RPIServerAddress}:{Conf.RPIPortNumber}/endpoint"
    response = urequests.post(RPIServerURL, data=jsonDataArrayed)
    response.close()

while True:
    try:
        varTemp, varHumi = measureFromDHT11()
        print("Temp is:", varTemp, "Humi is:", varHumi)
        SendingDataToRPI(OutputForServo)
        time.sleep(2)
        
    except OSError as e:
        print(f"OsError in : {e}")
