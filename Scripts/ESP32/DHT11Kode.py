#!/usr/bin/env python3
# Author: NyboMønster
#IOHT Projekt DHT11

#Liste af imports:
from machine import Pin
import dht
from ConfigFileForESP32 import ListOfConfig as Conf
#Liste af Variables
varTemp = 0
varHumi = 0
dhtsensor = dht.DHT11(Conf[0])

def measureFromDHT11():
    varTemp = dhtsensor.temperature()
    varHumi = dhtsensor.humidity()
    #varTemp = 2
    #varHumi = 15
    return varTemp, varHumi
varTemp, varHumi = measureFromDHT11()
#print("Temp is:", varTemp, "Humi is:", varHumi)
